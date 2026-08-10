# -*- coding: utf-8 -*-
"""Correct rationalization: NJ2 * Phi^3 with st^e4 ct^e5 -> (q sg)^e4 cg^e5 Phi^(3-(e4+e5)/2)."""
import json, sympy as sp
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
q = sp.symbols('q')
Phi = cg**2 + q**2*sg**2
K = 3
R = 0
for (mon, coeff) in sp.Poly(NJ2, A, t, sg, cg, st, ct).terms():
    eA, et, e2, e3, e4, e5 = mon
    k = (e4 + e5)//2
    R += coeff * A**eA * t**et * sg**e2 * cg**e3 * (q*sg)**e4 * cg**e5 * Phi**(K - k)
R = sp.expand(R)
print('R terms:', len(sp.Add.make_args(R)))
# try factor
fR = sp.factor(R)
print('factor:', fR)
print()
# collect by q
for (mon, coeff) in sorted(sp.Poly(R, q).terms(), key=lambda kv: kv[0], reverse=True):
    print('  q^%d : %s' % (mon[0], sp.factor(coeff)))
