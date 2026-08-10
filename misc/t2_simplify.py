# -*- coding: utf-8 -*-
"""Derive simplified numerators of G, Gc, Gx in (gamma,t) atoms; verify numerically."""
import sympy as sp
import numpy as np

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

qexpr = (sp.sin(t)/sp.cos(t))/(sp.sin(g)/sp.cos(g))
subs = {x: sp.pi - g, c: t/(sp.pi - g), q: qexpr}
G2, Gc2, Gx2 = sp.simplify(G.subs(subs)), sp.simplify(Gc.subs(subs)), sp.simplify(Gx.subs(subs))

sg, cg, st, ct = sp.sin(g), sp.cos(g), sp.sin(t), sp.cos(t)
A = sp.pi - g
P = A*sp.sin(2*t) + t*sp.sin(2*g)  # = 2(A*st*ct + t*sg*cg)

# extract numerators
def get_num(f, expected_factor_den):
    num, den = sp.fraction(sp.together(f))
    return sp.expand_trig(sp.expand(num)), sp.factor(den)

for name, f, denom in [('G', G2, P**2), ('Gc', Gc2, P**3), ('Gx', Gx2, P**3*sg)]:
    num, den = get_num(f, denom)
    # check denominator matches
    ok = sp.simplify(den - denom) == 0
    print('%s: denom matches P^k? %s ; num terms: %d' % (name, ok, len(sp.Add.make_args(num))))
    # factor out constant multiples
    print('  num factorized:', sp.factor(num))
