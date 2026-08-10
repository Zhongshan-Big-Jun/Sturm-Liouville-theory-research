# -*- coding: utf-8 -*-
"""t3_part_feas: partition feasibility for dP05/du<0 (1D) and dNJ/dt>0 (2D box)."""
import sympy as sp, numpy as np, json, math

with open('misc/t3_P05.json') as fh: r = json.load(fh)
u, su, cu = sp.symbols('u su cu', positive=True)
P05 = sum(int(c)*u**m[0]*su**m[1]*cu**m[2] for m,c in zip(r['monoms'], r['coeffs']))
dP05 = sp.expand(sp.diff(P05, u) + cu*sp.diff(P05, su) - su*sp.diff(P05, cu))
pdp = sp.Poly(dP05, u, su, cu)
mo6 = pdp.monoms(); co6 = pdp.coeffs()
pos6 = [(m,c) for m,c in zip(mo6,co6) if c>0]; neg6 = [(m,c) for m,c in zip(mo6,co6) if c<0]
print('dP05/du: %d terms, pos %d, neg %d' % (len(mo6), len(pos6), len(neg6)))

def powmm(lo, hi, p, q):
    vals = [math.sin(lo)**p*math.cos(lo)**q, math.sin(hi)**p*math.cos(hi)**q]
    if p>0 and q>0:
        tc = math.atan(p/q)
        if lo < tc < hi: vals.append(math.sin(tc)**p*math.cos(tc)**q)
    return max(vals), min(vals)

def feas1D(N, poly_pos, poly_neg):
    uL, uR = math.pi/3, (math.pi-0.655)/2
    worst = 0; nf = 0
    for i in range(N):
        lo = uL + i*(uR-uL)/N; hi = uL + (i+1)*(uR-uL)/N
        Pu = sum(c*(hi**m[0])*powmm(lo,hi,m[1],m[2])[0] for m,c in poly_pos)
        Ql = sum((-c)*(lo**m[0])*powmm(lo,hi,m[1],m[2])[1] for m,c in poly_neg)
        ratio = Pu/Ql if Ql>0 else float('inf')
        worst = max(worst, ratio)
        if Pu >= Ql: nf += 1
    return nf, worst

for N in [10,20,40,60,100]:
    nf, wr = feas1D(N, pos6, neg6)
    print('dP05/du<0: N=%d fail=%d worst_ratio=%.3f' % (N, nf, wr))

# dNJ/dt > 0 on (A,c) boxes (relaxed region with A>=pi/(1+c))
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_dNJdt.json') as fh: r2 = json.load(fh)
mo2 = r2['monoms']; co2 = [int(c) for c in r2['coeffs']]
pos2 = [(m,c) for m,c in zip(mo2,co2) if c>0]; neg2 = [(m,c) for m,c in zip(mo2,co2) if c<0]
def sgcg_mm(Alo, Ahi, p, q):
    def f(Av): return math.sin(Av)**p * (-math.cos(Av))**q
    return max(f(Alo), f(Ahi)), min(f(Alo), f(Ahi))
def feas2D(NA, Nc):
    Amin, Amax = 2*math.pi/3, math.pi-0.655
    cmin, cmax = 0.4, 0.5
    nf = 0; nbox = 0; worst = 0
    for i in range(NA):
        Alo = Amin + i*(Amax-Amin)/NA; Ahi = Amin + (i+1)*(Amax-Amin)/NA
        for j in range(Nc):
            clo = cmin + j*(cmax-cmin)/Nc; chi = cmin + (j+1)*(cmax-cmin)/Nc
            # relaxed constraint A(1+c)>=pi; skip boxes entirely violating (conservative: use Ahi*(1+clo)<pi)
            if Ahi*(1+clo) < math.pi - 1e-12: continue
            tlo = clo*Alo; thi = chi*Ahi
            nbox += 1
            Pu = sum(c*(Ahi**m[0])*(thi**m[1])*sgcg_mm(Alo,Ahi,m[2],m[3])[0]*powmm(tlo,thi,m[4],m[5])[0] for m,c in pos2)
            Ql = sum((-c)*(Alo**m[0])*(tlo**m[1])*sgcg_mm(Alo,Ahi,m[2],m[3])[1]*powmm(tlo,thi,m[4],m[5])[1] for m,c in neg2)
            ratio = Pu/Ql if Ql>0 else float('inf')
            worst = max(worst, ratio)
            if Pu >= Ql: nf += 1
    return nbox, nf, worst
for NA, Nc in [(10,4),(20,8),(30,12),(40,16),(60,24)]:
    nb, nf, wr = feas2D(NA, Nc)
    print('dNJ/dt>0: NA=%d Nc=%d boxes=%d fail=%d worst=%.3f' % (NA, Nc, nb, nf, wr))
