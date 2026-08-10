# -*- coding: utf-8 -*-
"""t3_dnj: extract dNJ/dt polynomial; box feasibility; also P05(u)=NJ(2u,1/2) polynomial."""
import sympy as sp, numpy as np, json, math, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

dNJ_dt = sp.expand(sp.diff(NJ, t) + ct*sp.diff(NJ, st) - st*sp.diff(NJ, ct))
atoms = [A,t,sg,cg,st,ct]
poly = sp.Poly(dNJ_dt, *atoms)
print('dNJ/dt: %d terms, deg %d' % (len(poly.monoms()), poly.total_degree()))
co = poly.coeffs(); mo = poly.monoms()
pos = [(m,c) for m,c in zip(mo,co) if c>0]; neg = [(m,c) for m,c in zip(mo,co) if c<0]
print('pos:', len(pos), 'sum:', sum(c for _,c in pos), ' max:', max(c for _,c in pos))
print('neg:', len(neg), 'sum:', sum(c for _,c in neg), ' min:', min(c for _,c in neg))
# save
res = {'nterms': len(mo), 'deg': poly.total_degree(), 'monoms': [list(m) for m in mo], 'coeffs': [str(c) for c in co]}
with open('misc/t3_dNJdt.json','w') as fh: json.dump(res, fh)

# box feasibility for dNJ/dt > 0 on relaxed region
gL, gR = 0.655, math.pi/3
tL, tR = 0.8976, 1.1503
Amin, Amax = 2*math.pi/3, math.pi-0.655
def powmaxmin(lo, hi, p, r, sinfirst=True):
    vals = [math.sin(lo)**p * math.cos(lo)**r, math.sin(hi)**p * math.cos(hi)**r]
    if p>0 and r>0:
        xc = math.atan(p/r)
        if lo < xc < hi: vals.append(math.sin(xc)**p*math.cos(xc)**r)
    return max(vals), min(vals)
def ub(m):
    a,b,p,rr,s,v = m
    return Amax**a * tR**b * powmaxmin(gL,gR,p,rr)[0] * powmaxmin(tL,tR,s,v)[0]
def lb(m):
    a,b,p,rr,s,v = m
    return Amin**a * tL**b * powmaxmin(gL,gR,p,rr)[1] * powmaxmin(tL,tR,s,v)[1]
Pu = sum(c*ub(m) for m,c in pos); Ql = sum((-c)*lb(m) for m,c in neg)
print('dNJ/dt box: pos_ub=%.3e negmag_lb=%.3e %s' % (Pu, Ql, 'OK(>0)' if Ql>Pu else 'FAIL'))

# P05: NJ at c=1/2 -> u=A/2: A=2u, t=u, sg=sin2u=2st ct, cg=-cos2u=2st^2-1
u = sp.symbols('u', positive=True)
su, cu = sp.sin(u), sp.cos(u)
P05 = sp.expand(NJ.subs({A: 2*u, t: u, sg: 2*su*cu, cg: 2*su**2-1, st: su, ct: cu}))
P05 = sp.expand(P05)
p05 = sp.Poly(P05, u, su, cu)
print('P05(u,su,cu): %d terms, deg %d' % (len(p05.monoms()), p05.total_degree()))
co5 = p05.coeffs(); mo5 = p05.monoms()
pos5 = [(m,c) for m,c in zip(mo5,co5) if c>0]; neg5 = [(m,c) for m,c in zip(mo5,co5) if c<0]
print('pos:', len(pos5), 'sum:', sum(c for _,c in pos5), 'neg:', len(neg5), 'sum:', sum(c for _,c in neg5))
res5 = {'nterms': len(mo5), 'deg': p05.total_degree(), 'monoms': [list(m) for m in mo5], 'coeffs': [str(c) for c in co5]}
with open('misc/t3_P05.json','w') as fh: json.dump(res5, fh)

# box feasibility for P05 < 0 on u in [pi/3, (pi-0.655)/2]
uL, uR = math.pi/3, (math.pi-0.655)/2
def ub5(m):
    a, s, v = m
    return uR**a * powmaxmin(uL, uR, s, v)[0]
def lb5(m):
    a, s, v = m
    return uL**a * powmaxmin(uL, uR, s, v)[1]
Pu5 = sum(c*ub5(m) for m,c in pos5); Ql5 = sum((-c)*lb5(m) for m,c in neg5)
print('P05 box: pos_ub=%.3e negmag_lb=%.3e %s' % (Pu5, Ql5, 'OK(<0)' if Pu5<Ql5 else 'FAIL'))
# dP05/du
dP05 = sp.expand(sp.diff(P05, u) + cu*sp.diff(P05, su) - su*sp.diff(P05, cu))
pdp = sp.Poly(dP05, u, su, cu)
co6 = pdp.coeffs(); mo6 = pdp.monoms()
pos6 = [(m,c) for m,c in zip(mo6,co6) if c>0]; neg6 = [(m,c) for m,c in zip(mo6,co6) if c<0]
Pu6 = sum(c*ub5(m) for m,c in pos6); Ql6 = sum((-c)*lb5(m) for m,c in neg6)
print('dP05/du: %d terms; box: pos_ub=%.3e negmag_lb=%.3e %s' % (len(mo6), Pu6, Ql6, 'OK(<0)' if Pu6<Ql6 else 'FAIL'))
