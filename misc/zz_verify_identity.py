# -*- coding: utf-8 -*-
"""Verify NJ2*Phi^3 = 32 A^2 cg^2 sg^2 * M * B identity numerically with TRUE st,ct."""
import json, sympy as sp
import mpmath as mp
mp.mp.dps = 40
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
q = sp.symbols('q')
Phi = cg**2 + q**2*sg**2
# candidate identity: R_true = NJ2(st=q sg/sqrt(Phi), ct=cg/sqrt(Phi)) * Phi^3
# compare with 32 A^2 cg^2 sg^2 M B
# B from the factorization:
M = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B = ( A**2*cg**2*sg**6*q**8 + 2*A*cg**2*sg**6*t*q**7
      + cg**2*sg**4*(3*A**2*cg**2 + sg**2*t**2)*q**6
      + 6*A*cg**4*sg**4*t*q**5
      + 3*cg**4*sg**2*(A**2*cg**2 + sg**2*t**2)*q**4
      + 6*A*cg**6*sg**2*t*q**3
      + cg**6*(A**2*cg**2 + 3*sg**2*t**2)*q**2
      + 2*A*cg**8*t*q
      + cg**8*t**2 )
RHS = 32*A**2*cg**2*sg**2*M*B
fRHS = sp.lambdify((A,t,sg,cg,q), RHS, 'mpmath')
fNJ2 = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
ok = True
for (g, qq) in [(0.7, 1.5), (0.9, 1.2), (1.0, 1.1), (0.65565, 2.0), (mp.pi/3, 1.0), (1.0472, 2.0), (0.8, 1.8)]:
    A_ = mp.pi - g; t_ = mp.atan(qq*mp.tan(g))
    sg_, cg_ = mp.sin(g), mp.cos(g)
    Phi_ = cg_**2 + qq**2*sg_**2
    st_ = qq*sg_/mp.sqrt(Phi_); ct_ = cg_/mp.sqrt(Phi_)
    lhs = fNJ2(A_, t_, sg_, cg_, st_, ct_) * Phi_**3
    rhs = fRHS(A_, t_, sg_, cg_, qq)
    print('g=%.4f q=%.2f: lhs=%.8f rhs=%.8f diff=%.1e' % (g, qq, lhs, rhs, abs(lhs-rhs)))
    if abs(lhs-rhs) > mp.mpf('1e-25'): ok = False
print('identity holds:', ok)
