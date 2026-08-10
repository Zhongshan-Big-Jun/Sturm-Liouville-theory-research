# -*- coding: utf-8 -*-
"""t3_njsplit_debug"""
import sympy as sp, json

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
NJr = sp.expand(NJ)
for _ in range(8):
    NJr = sp.expand(NJr.subs(st**2, 1-ct**2))
print('NJr has st**2?', NJr.has(st**2))
E = sp.expand(NJr.subs(st, 0))
print('E has st?', E.has(st))
Osc = sp.expand((NJr - E)/(st*ct))
print('Osc has st?', Osc.has(st), ' has 1/ct?', Osc.has(1/ct), ' has ct**odd?', Osc.has(ct**3))
# reconstruct
rec = sp.expand(E + st*ct*Osc)
print('reconstruction == NJr?', sp.simplify(rec - NJr) == 0)
