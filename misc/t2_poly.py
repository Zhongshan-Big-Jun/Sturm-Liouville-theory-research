# -*- coding: utf-8 -*-
"""Expand J2_2d numerator as polynomial in 6 positive atoms; inspect coefficients."""
import sympy as sp

x, c, q = sp.symbols('x c q', positive=True)
g = sp.symbols('gamma', positive=True)
t = sp.symbols('t', positive=True)
sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x*cx/sx
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
Gx = sp.simplify(sp.diff(G, x))
Gc = sp.simplify(sp.diff(G, c))
u = x*Ph/D
J = sp.simplify(G**2 - u*Gx + Gc)

sg, cg = sp.sin(g), sp.cos(g)
st, ct = sp.sin(t), sp.cos(t)
qexpr = (st/ct)/(sg/cg)
J2 = sp.simplify(J.subs({x: sp.pi - g, c: t/(sp.pi - g), q: qexpr}))
num, den = sp.fraction(sp.together(J2))
print('den:', sp.factor(den))
# expand trig: express sin(2t) etc in terms of single-angle atoms
num_e = sp.expand_trig(sp.expand(num))
print('num expanded terms:', len(sp.Add.make_args(num_e)))
# extract the factor 4*(gamma-pi)^2 = 4*A^2
print('num factor:', sp.factor(num_e)[:400] if False else '')
# polynomial check in the six atoms
atoms = [g, t, sg, cg, st, ct]
p = sp.Poly(sp.expand(num_e), *atoms)
print('OK polynomial. total degree:', p.total_degree())
monoms = p.monoms()
coeffs = p.coeffs()
print('num monomials:', len(monoms))
print('all coeffs integer:', all(sp.Integer(c) == c for c in coeffs))
# summary of coefficient magnitudes
pos = [c for c in coeffs if c > 0]; neg = [c for c in coeffs if c < 0]
print('positive coeffs:', len(pos), ' max:', max(pos) if pos else None)
print('negative coeffs:', len(neg), ' min:', min(neg) if neg else None)
# save poly for later use
import json
data = {'monoms': [list(m) for m in monoms], 'coeffs': [str(c) for c in coeffs]}
io_ = open('misc/t2_numerator_poly.json','w')
json.dump(data, io_); io_.close()
print('saved misc/t2_numerator_poly.json')
