# -*- coding: utf-8 -*-
"""t3_dnj2dt_factor: factor dNJ2dt; also B2 on c=1/2 line."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJ2dt = sp.expand(sp.diff(NJ2, t) + ct*sp.diff(NJ2, st) - st*sp.diff(NJ2, ct))
print('factor dNJ2dt:', sp.factor(dNJ2dt))
