# -*- coding: utf-8 -*-
"""Rationalize W via st = q sg/sqrt(Phi), ct = cg/sqrt(Phi), Phi = cg^2+q^2 sg^2."""
import json, sympy as sp
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
q = sp.symbols('q')
Phi = cg**2 + q**2*sg**2
# st = q sg/sqrt(Phi), ct = cg/sqrt(Phi). Multiply by Phi^(total trig degree/2).
# total degree in trig vars of each monomial: e2+e3+e4+e5 (even)
poly = sp.Poly(NJ2, A, t, sg, cg, st, ct)
R = 0
for (mon, coeff) in poly.terms():
    eA, et, e2, e3, e4, e5 = mon
    k = (e2+e3+e4+e5)//2
    R += coeff * A**eA * t**et * sg**e2 * cg**e3 * (q*sg)**e4 * cg**e5 * Phi**(0)
    # wait: st^e4 ct^e5 = (q sg)^e4 cg^e5 / Phi^((e4+e5)/2); multiply whole NJ2 by Phi^K to clear all.
# Instead: multiply NJ2 by Phi^K where K = max over monomials of (e4+e5)/2
K = max((m[4]+m[5])//2 for m in poly.monoms())
R = sp.expand(NJ2 * Phi**K)
R = R.subs({st: q*sg, ct: cg})   # st*Phi^(1/2) -> q sg etc: after multiplying by Phi^K, replace st^e4 ct^e5 Phi^((e4+e5)/2) -> (q sg)^e4 cg^e5 * Phi^(K-(e4+e5)/2)
print('K =', K)
print('R terms:', len(sp.Add.make_args(sp.expand(R))))
R = sp.expand(R)
# collect by powers of q
Rc = sp.collect(sp.expand(R), q)
print('R collected by q:')
for (mon, coeff) in sorted(sp.Poly(R, q).terms(), key=lambda kv: kv[0], reverse=True):
    print('  q^%d : %s' % (mon[0], sp.factor(coeff)))
