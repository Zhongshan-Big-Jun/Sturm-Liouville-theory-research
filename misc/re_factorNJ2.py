# -*- coding: utf-8 -*-
"""Factor NJ2, try reductions."""
import sympy as sp, json
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
print('factor:', sp.factor(NJ2))
# group by powers of ct
p = sp.Poly(NJ2, ct)
print('as poly in ct:')
print(sp.factor(p.as_expr()))
print()
# group by st
p2 = sp.Poly(NJ2, st)
print('as poly in st:')
print(sp.factor(p2.as_expr()))
