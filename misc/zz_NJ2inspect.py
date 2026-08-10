# -*- coding: utf-8 -*-
"""Inspect NJ2 terms."""
import json, sympy as sp
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
terms = sp.Add.make_args(NJ2)
print('number of terms:', len(terms))
neg = 0; pos = 0; zero_cg = 0
for tm in terms:
    coeff, mon = sp.factor_terms(tm).as_coeff_Mul()
    exps = [sp.degree(mon, v) for v in [A,t,sg,cg,st,ct]]
    sign = '-' if coeff < 0 else '+'
    if exps[3] % 2 == 1: neg += 1; kind='NEG(cg odd)'
    elif exps[3] == 0: zero_cg += 1; kind='cg-free'
    else: pos += 1; kind='POS(cg even)'
    print('%s  coeff=%+d  exps(A,t,sg,cg,st,ct)=%s  %s' % (sign, coeff, exps, kind))
print()
print('neg:', neg, 'pos:', pos, 'cg-free:', zero_cg)
f = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'numpy')
import numpy as np, math
for (x, th) in [(2*math.pi/3, math.pi/3), (2.2, 1.0), (2.4, 1.1), (2.1, 1.045), (2.35,0.98)]:
    v = f(x, th, math.sin(x), math.cos(x), math.sin(th), math.cos(th))
    print('NJ2 at (%.3f,%.3f) = %.4e' % (x, th, v))
