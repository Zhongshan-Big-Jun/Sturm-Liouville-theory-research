# -*- coding: utf-8 -*-
"""t3_b2factor: try factoring B2 (as K = dNJ2dt/(32 A^2 cg))."""
import sympy as sp, json, pickle, time

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJ2dt = sp.expand(sp.diff(NJ2, t) + ct*sp.diff(NJ2, st) - st*sp.diff(NJ2, ct))
K = sp.expand(dNJ2dt/(32*A**2*cg))
print('K poly?', K.is_polynomial(A,t,sg,cg,st,ct) if hasattr(K,'is_polynomial') else 'check')
poly = sp.Poly(K, A, t, sg, cg, st, ct)
print('K terms:', len(poly.monoms()))
t0=time.time()
try:
    f = sp.factor(K)
    print('factor:', f)
except Exception as e:
    print('factor failed:', type(e).__name__, str(e)[:200])
print('time', time.time()-t0)
# gcd with candidate factors
for name, cnd in {'st*cg - sg*ct': st*cg - sg*ct, 'st*cg + sg*ct': st*cg + sg*ct, 'A*st*ct + t*sg*cg': A*st*ct + t*sg*cg, 'cg^2-ct^2': cg**2-ct**2, 'sg^2-st^2': sg**2-st**2}.items():
    q, rem = sp.div(K, cnd)
    if rem == 0:
        print('divisible by', name)
print('done')
