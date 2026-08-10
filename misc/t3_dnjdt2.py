# -*- coding: utf-8 -*-
"""t3_dnjdt2: compute dNJ/dt (total t-derivative), explore structure."""
import sympy as sp, json, math, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

# total derivative in t: dNJ/dt = NJ_t + ct*NJ_st - st*NJ_ct
dNJdt = sp.expand(sp.diff(NJ, t) + ct*sp.diff(NJ, st) - st*sp.diff(NJ, ct))
poly = sp.Poly(dNJdt, A, t, sg, cg, st, ct)
print('terms:', poly.total_degree(), len(poly.monoms()))
pos = [(c,m) for m,c in zip(poly.monoms(), poly.coeffs()) if c>0]
neg = [(c,m) for m,c in zip(poly.monoms(), poly.coeffs()) if c<0]
print('pos:', len(pos), 'sum', sum(c for c,_ in pos))
print('neg:', len(neg), 'sum', sum(c for c,_ in neg))

# reduce st^2 -> 1-ct^2 and split E + st*ct*O
w = sp.symbols('w', positive=True)
dNJr = sp.expand(dNJdt)
for _ in range(8):
    dNJr = sp.expand(dNJr.subs(st**2, 1-ct**2))
E = sp.expand(dNJr.subs(st, 0))
Osc = sp.expand((dNJr - E)/(st*ct))
E = sp.expand(E.subs(ct**2, w))
O = sp.expand(Osc.subs(ct**2, w))
print('E terms:', len(sp.Add.make_args(E)), ' O terms:', len(sp.Add.make_args(O)))
# check residual ct odd in O
def check_odd(expr):
    e = sp.expand(expr)
    return e.has(ct)
print('E has odd ct?', check_odd(E), ' O has odd ct?', check_odd(O))
with open('misc/t3_dNJdt_split.pkl','wb') as fh: pickle.dump({'E':E,'O':O,'dNJdt':dNJdt}, fh)
print('saved')
