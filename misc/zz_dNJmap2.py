# -*- coding: utf-8 -*-
"""Map signs of dNJ/dq and dNJ/dg on the box; check monotonicity regions."""
import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
def NJ(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return fN(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
h = mp.mpf('1e-7')
N = 100
posq = []; negq = []; posg = []; negg = []
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        dq = (NJ(g, q+h)-NJ(g, q-h))/(2*h)
        dg = (NJ(g+h, q)-NJ(g-h, q))/(2*h)
        (posq if dq > 0 else negq).append((float(g), float(q), float(dq)))
        (posg if dg > 0 else negg).append((float(g), float(q), float(dg)))
print('dNJ/dq: positive %d, negative %d' % (len(posq), len(negq)))
if negq:
    gs = [p[0] for p in negq]; qs = [p[1] for p in negq]
    print('  dNJ/dq<0 region: g in [%.3f, %.3f], q in [%.3f, %.3f]' % (min(gs), max(gs), min(qs), max(qs)))
print('dNJ/dg: positive %d, negative %d' % (len(posg), len(negg)))
if negg:
    gs = [p[0] for p in negg]; qs = [p[1] for p in negg]
    print('  dNJ/dg<0 region: g in [%.3f, %.3f], q in [%.3f, %.3f]' % (min(gs), max(gs), min(qs), max(qs)))
