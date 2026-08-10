# -*- coding: utf-8 -*-
"""Evaluate correct R = NJ2*Phi^3 and H = R/(32 A^2 cg^4 sg^2) on the box; also M(gamma)."""
import json, sympy as sp
import mpmath as mp
mp.mp.dps = 40
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
fNJ2 = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
def NJ(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    sg_, cg_ = mp.sin(g), mp.cos(g)
    Phi = cg_**2 + q*q*sg_**2
    st_ = q*sg_/mp.sqrt(Phi); ct_ = cg_/mp.sqrt(Phi)
    return fNJ2(A_, t_, sg_, cg_, st_, ct_)
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 100
mnH = mp.mpf('1e30'); mxH = mp.mpf('-1e30'); mnM = mp.mpf('1e30'); mxM = mp.mpf('-1e30'); mnNJ = mp.mpf('1e30'); mxNJ = mp.mpf('-1e30')
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A_ = mp.pi - g; sg_, cg_ = mp.sin(g), mp.cos(g)
    M = 2*A_**2*cg_**2 - A_**2 - 8*A_*cg_*sg_ + 6*sg_**2
    mnM = min(mnM, M); mxM = max(mxM, M)
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        v = NJ(g, q)
        mnNJ = min(mnNJ, v); mxNJ = max(mxNJ, v)
        Phi = cg_**2 + q*q*sg_**2
        R = v * Phi**3
        H = R/(32*A_**2*cg_**4*sg_**2)
        mnH = min(mnH, H); mxH = max(mxH, H)
print('M(gamma) on box: [%.6f, %.6f]' % (mnM, mxM))
print('H on box: [%.6f, %.6f]' % (mnH, mxH))
print('NJ2 on box: [%.3f, %.3f]' % (mnNJ, mxNJ))
