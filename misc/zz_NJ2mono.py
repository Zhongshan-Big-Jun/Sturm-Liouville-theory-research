# -*- coding: utf-8 -*-
"""NJ2 as 2D function: monotonicity in q and gamma over the box."""
import json, sympy as sp
import mpmath as mp
mp.mp.dps = 40
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')

def NJ(g, q):
    A = mp.pi - g; t = mp.atan(q*mp.tan(g))
    return fN(A, t, mp.sin(g), mp.cos(g), mp.sin(t), mp.cos(t))

glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
h = mp.mpf('1e-7')
N = 100
dqd = []; dgd = []
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        v0 = NJ(g, q)
        dq = (NJ(g, q+h)-v0)/h
        dg = (NJ(g+h, q)-v0)/h
        dqd.append(float(dq)); dgd.append(float(dg))
print('dNJ2/dq over box: [%.3f, %.3f]' % (min(dqd), max(dqd)))
print('dNJ2/dg over box: [%.3f, %.3f]' % (min(dgd), max(dgd)))
# NJ2 on q=1 and q=2 and gamma=0.655, gamma=1.0472 edges
print()
print('q=1 line: NJ2 at g=0.655: %.3f ; g=1.0472: %.3f' % (NJ(mp.mpf('0.655'), 1), NJ(mp.pi/3, 1)))
print('q=2 line: NJ2 at g=0.655: %.3f ; g=1.0472: %.3f' % (NJ(mp.mpf('0.655'), 2), NJ(mp.pi/3, 2)))
