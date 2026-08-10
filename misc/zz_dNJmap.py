# -*- coding: utf-8 -*-
"""Map where dJ/dq|g > 0 on the box."""
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
def Delta(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return A_*mp.sin(t_)*mp.cos(t_) + t_*mp.sin(g)*mp.cos(g)
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
h = mp.mpf('1e-7')
N = 80
pos = []
mn = (mp.mpf('1e30'), None); mx = (mp.mpf('-1e30'), None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        dq = (NJ(g, q+h)-NJ(g, q-h))/(2*h)
        if dq > 0: pos.append((float(g), float(q), float(dq)))
        if dq < mn[0]: mn = (dq, (float(g), float(q)))
        if dq > mx[0]: mx = (dq, (float(g), float(q)))
print('dNJ/dq range [%.3f, %.3f]; #positive samples %d / %d' % (mn[0], mx[0], len(pos), (N+1)**2))
if pos:
    gs = [p[0] for p in pos]; qs = [p[1] for p in pos]
    print('positive region: g in [%.3f, %.3f], q in [%.3f, %.3f]' % (min(gs), max(gs), min(qs), max(qs)))
    # show a few
    for p in pos[:10]: print('  g=%.4f q=%.3f dNJ/dq=%.3f' % p)
