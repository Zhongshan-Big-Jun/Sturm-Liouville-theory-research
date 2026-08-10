# -*- coding: utf-8 -*-
"""t3_NJ2_reduce4.py: reduce NJ2 modulo circle relations."""
import sympy as sp, json
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
NJ2 = sum(int(r['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(r['monoms']))
G = [sg**2 + cg**2 - 1, st**2 + ct**2 - 1]
out = sp.reduced(sp.expand(NJ2), G, [sg, cg, st, ct])
red = out[0] if isinstance(out, tuple) else out[0]
red = sp.expand(red)
print('reduced terms:', len(sp.Add.make_args(red)))
print(red)
print()
print('factor:', sp.factor(red))
