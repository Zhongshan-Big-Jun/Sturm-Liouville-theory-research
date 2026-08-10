# -*- coding: utf-8 -*-
"""t3_feas_ac: partition (A,c) boxes; per-box monomial bounds for NJ<0.
A in [2pi/3, pi-0.655], c in [0.4,0.5], constraint A >= pi/(1+c) (relaxed: drop q<=2 first).
Atoms: sg=sinA, cg=-cosA, t=cA, st=sin t, ct=cos t."""
import json, math
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]

Amin, Amax = 2*math.pi/3, math.pi-0.655
cmin, cmax = 0.4, 0.5

def sgcg_maxmin(Alo, Ahi, p, rr):
    vals = []
    for A in [Alo, Ahi]:
        vals.append((math.sin(A)**p)*(math.cos(A)**rr) * (-1)**rr)
    # careful: cg = -cosA > 0, so cg^r = (-cosA)^r
    def f(A): return (math.sin(A)**p)*((-math.cos(A))**rr)
    vals = [f(Alo), f(Ahi)]
    # monotone on (pi/2,pi) -> endpoints only
    return max(vals), min(vals)

def stct_maxmin(tlo, thi, s, v):
    vals = [math.sin(tlo)**s * math.cos(tlo)**v, math.sin(thi)**s * math.cos(thi)**v]
    if s>0 and v>0:
        tc = math.atan(math.sqrt(s/v))
        if tlo < tc < thi:
            vals.append(math.sin(tc)**s * math.cos(tc)**v)
    return max(vals), min(vals)

def feas(NA, Nc, use_q2=False):
    # boxes: A in [Amin + i*(Amax-Amin)/NA, ...], c similarly
    worst_ratio = 0
    nfail = 0; nbox = 0
    for i in range(NA):
        Alo = Amin + i*(Amax-Amin)/NA; Ahi = Amin + (i+1)*(Amax-Amin)/NA
        for j in range(Nc):
            clo = cmin + j*(cmax-cmin)/Nc; chi = cmin + (j+1)*(cmax-cmin)/Nc
            # q<=2 constraint: tan(cA) <= -2 tan A ; check if box entirely violates -> skip
            if use_q2:
                if math.tan(clo*Ahi) > -2*math.tan(Ahi) + 1e-12:  # conservative: if even the easiest point violates
                    continue
            tlo = clo*Alo; thi = chi*Ahi
            if thi < tlo: continue
            nbox += 1
            Pu = 0.0; Ql = 0.0
            for m, c in zip(monoms, coeffs):
                a, b, p, rr, s, v = m
                if c > 0:
                    Pu += c * Ahi**a * thi**b * sgcg_maxmin(Alo,Ahi,p,rr)[0] * stct_maxmin(tlo,thi,s,v)[0]
                else:
                    Ql += (-c) * Alo**a * tlo**b * sgcg_maxmin(Alo,Ahi,p,rr)[1] * stct_maxmin(tlo,thi,s,v)[1]
            ratio = Pu/Ql if Ql > 0 else float('inf')
            worst_ratio = max(worst_ratio, ratio)
            if Pu >= Ql: nfail += 1
    return nbox, nfail, worst_ratio

for NA, Nc in [(5,2),(10,4),(20,8),(40,16),(60,24),(100,40)]:
    nb, nf, wr = feas(NA, Nc)
    print('NA=%d Nc=%d: boxes=%d fail=%d worst_ratio=%.3f' % (NA, Nc, nb, nf, wr))
