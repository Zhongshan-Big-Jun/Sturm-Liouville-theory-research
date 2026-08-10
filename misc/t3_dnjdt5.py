# -*- coding: utf-8 -*-
"""t3_dnjdt5: careful parity structure of dNJdt after st^2 -> 1-ct^2."""
import sympy as sp, json

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJdt = sp.expand(sp.diff(NJ, t) + ct*sp.diff(NJ, st) - st*sp.diff(NJ, ct))
dNJr = sp.expand(dNJdt)
for _ in range(10):
    dNJr = sp.expand(dNJr.subs(st**2, 1-ct**2))
# list terms with st exponent
terms = sp.Add.make_args(dNJr)
from collections import Counter
cnt = Counter()
for term in terms:
    p = sp.Poly(term, st, ct)
    for m, c in zip(p.monoms(), p.coeffs()):
        cnt[m[0]] += 1
print('st exponent histogram:', dict(sorted(cnt.items())))
# terms with st^1: show them
odd = []
for term in terms:
    p = sp.Poly(term, st, ct)
    if any(m[0] == 1 for m in p.monoms()):
        odd.append(term)
print('num st^1 terms:', len(odd))
for term in odd[:12]: print('  ', term)
