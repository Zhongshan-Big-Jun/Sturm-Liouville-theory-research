# -*- coding: utf-8 -*-
"""t3_Bcheck3.py: check whether NJ2 - red is in the ideal."""
import sympy as sp, json
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
NJ2 = sum(int(r['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(r['monoms']))
G = [sg**2 + cg**2 - 1, st**2 + ct**2 - 1]
out = sp.reduced(sp.expand(NJ2), G, [sg, cg, st, ct])
red = sp.expand(out[0][0])
coeffs = out[1]
print('coeffs type:', type(coeffs), len(coeffs) if hasattr(coeffs,'__len__') else '')
# reconstruct: NJ2 - red == coeffs[0]*G[0] + coeffs[1]*G[1]?
if isinstance(coeffs, list) and len(coeffs) == 2:
    lhs = sp.expand(NJ2 - red)
    rhs = sp.expand(coeffs[0]*G[0] + coeffs[1]*G[1])
    print('NJ2 - red == combo?', sp.simplify(lhs - rhs) == 0)
# numeric check of NJ2 = -32 A^2 cg B on variety
B = sp.expand(red/(-32*A**2*cg))
import random
ok = True
for _ in range(5):
    x = 2.1 + random.random()*0.4; th = 0.9 + random.random()*0.3
    sgv = (random.random()); cgv = (1-sgv**2)**0.5
    stv = (random.random()); ctv = (1-stv**2)**0.5
    sub = {A:x, t:th, sg:sgv, cg:cgv, st:stv, ct:ctv}
    v1 = float(NJ2.subs(sub).evalf(12)); v2 = float((-32*A**2*cg*B).subs(sub).evalf(12))
    if abs(v1-v2) > 1e-6: ok=False; print('MISMATCH', v1, v2)
print('numeric identity NJ2 == -32A^2 cg B on variety:', ok)
