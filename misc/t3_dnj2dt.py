# -*- coding: utf-8 -*-
"""t3_dnj2dt: recompute dNJ2/dt and parity structure."""
import sympy as sp, json, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJ2dt = sp.expand(sp.diff(NJ2, t) + ct*sp.diff(NJ2, st) - st*sp.diff(NJ2, ct))
poly = sp.Poly(dNJ2dt, A, t, sg, cg, st, ct)
print('dNJ2dt terms:', len(poly.monoms()), 'deg', poly.total_degree())
pos = [(c,m) for m,c in zip(poly.monoms(), poly.coeffs()) if c>0]
neg = [(c,m) for m,c in zip(poly.monoms(), poly.coeffs()) if c<0]
print('pos:', len(pos), 'sum', sum(c for c,_ in pos), ' neg:', len(neg), 'sum', sum(c for c,_ in neg))
# parity split
dNJ2r = sp.expand(dNJ2dt)
for _ in range(10):
    dNJ2r = sp.expand(dNJ2r.subs(st**2, 1-ct**2))
d0 = sp.expand(dNJ2r.subs(st, 0))
d1 = sp.expand((dNJ2r - d0)/st)
E0e = sp.expand(d0.subs(ct, 0)); E0o = sp.expand((d0-E0e)/ct)
E1e = sp.expand(d1.subs(ct, 0)); E1o = sp.expand((d1-E1e)/ct)
w = sp.symbols('w', positive=True)
def to_w(e): return sp.expand(sp.expand(e).subs(ct**2, w))
E0e, E0o, E1e, E1o = to_w(E0e), to_w(E0o), to_w(E1e), to_w(E1o)
print('E0e terms:', len(sp.Add.make_args(E0e)))
print('E0o terms:', len(sp.Add.make_args(E0o)))
print('E1e terms:', len(sp.Add.make_args(E1e)))
print('E1o terms:', len(sp.Add.make_args(E1o)))
with open('misc/t3_dNJ2dt_parity.pkl','wb') as fh: pickle.dump({'E0e':E0e,'E0o':E0o,'E1e':E1e,'E1o':E1o}, fh)
print('E1e =', E1e)
print('E1o =', E1o)
print('E0o =', sp.factor(E0o))
