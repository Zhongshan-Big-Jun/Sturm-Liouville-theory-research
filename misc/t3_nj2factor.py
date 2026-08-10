# -*- coding: utf-8 -*-
"""t3_nj2factor: try factoring NJ2 directly."""
import sympy as sp, json

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
import time
t0 = time.time()
try:
    fac = sp.factor(NJ2)
    print('factor:', fac)
except Exception as e:
    print('factor failed:', type(e).__name__, e)
print('time:', time.time()-t0)
# check divisibility by candidate factors
cands = {'A*st*ct + t*sg*cg': A*st*ct + t*sg*cg,
         'st*ct': st*ct, 'sg*cg': sg*cg, 'st*cg - sg*ct': st*cg - sg*ct}
for name, cnd in cands.items():
    q, rem = sp.div(NJ2, cnd)
    print(f'divisible by {name}?', rem == 0)
