# -*- coding: utf-8 -*-
"""t3_NJ2_reduce.py: reduce NJ2 with circle relations."""
import sympy as sp, json
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
NJ2 = sum(int(r['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(r['monoms']))
# substitute cg^2 = 1 - sg^2, ct^2 = 1 - st^2 via remainder
from sympy import Poly
sgsym, stsym = sp.symbols('sg2 st2')
expr = NJ2
for _ in range(8):
    expr = sp.expand(expr)
    expr = expr.subs(cg**2, 1-sg**2)
    expr = expr.subs(ct**2, 1-st**2)
    expr = sp.expand(expr)
expr = sp.expand(expr)
print('terms:', len(sp.Add.make_args(expr)))
# group by (A,t) powers
p = sp.Poly(expr, sg, st)
print('sg/st structure:')
print(p.as_expr())
# factor?
print('factor attempt:')
f = sp.factor(expr)
print(f)
