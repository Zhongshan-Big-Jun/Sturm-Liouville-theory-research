# -*- coding: utf-8 -*-
"""Eliminate q via tan t = q tan g: NJ2 as polynomial in (A,t,sg,cg,st,ct) with q=(st*cg)/(sg*ct)."""
import json, sympy as sp
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
q = sp.symbols('q')
# NJ2 is polynomial in the trig variables; substituting q = st*cg/(sg*ct) won't change NJ2 since q not present.
# Instead: work with W = NJ2/(32 A^2 cg)
W = sp.expand(NJ2/(32*A*A*cg))
print('W terms:', len(sp.Add.make_args(sp.expand(W))))
# collect W by powers of st*ct and st^2, ct^2
Wc = sp.collect(sp.expand(W), [st, ct])
print('W collected (by st,ct):')
for (mon, coeff) in sorted(sp.Poly(sp.expand(W), st, ct).terms(), key=lambda kv: kv[0], reverse=True):
    print('  st^%d ct^%d : %s' % (mon[0], mon[1], sp.factor(coeff)))
