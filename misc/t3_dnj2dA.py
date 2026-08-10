# -*- coding: utf-8 -*-
"""t3_dnj2dA: decompose dNJ2/dA."""
import sympy as sp, json

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
c = sp.symbols('c', positive=True)
# chain rule: gamma = pi-A, sg=sin(pi-A), cg=cos(pi-A), t=cA, st=sin(cA), ct=cos(cA)
# dNJ2/dA = NJ2_A + c*NJ2_t + (dsg/dA)NJ2_sg + (dcg/dA)NJ2_cg + c*ct*NJ2_st - c*st*NJ2_ct
# dsg/dA = -cg, dcg/dA = sg
dA_expr = sp.expand(sp.diff(NJ2, A) + c*sp.diff(NJ2, t) - cg*sp.diff(NJ2, sg) + sg*sp.diff(NJ2, cg)
                    + c*ct*sp.diff(NJ2, st) - c*st*sp.diff(NJ2, ct))
dA_expr = sp.expand(dA_expr.subs(t, c*A))
poly = sp.Poly(dA_expr, A, c, sg, cg, st, ct)
print('terms:', len(poly.monoms()))
pos = [(int(cc), m) for m, cc in zip(poly.monoms(), poly.coeffs()) if cc > 0]
neg = [(int(cc), m) for m, cc in zip(poly.monoms(), poly.coeffs()) if cc < 0]
print('pos:', len(pos), 'sum', sum(x for x,_ in pos), ' neg:', len(neg), 'sum', sum(x for x,_ in neg))
# factor
try:
    print('factor:', sp.factor(dA_expr))
except Exception as e:
    print('factor failed:', e)
