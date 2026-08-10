# -*- coding: utf-8 -*-
"""t3_dnjdt4: normalize w^(k/2) -> w^floor*sqrt(w), split dNJ/dt = Q1(w) + sqrt(w(1-w))*Q2(w), factor."""
import sympy as sp, pickle

with open('misc/t3_dNJdt_split.pkl','rb') as fh: d = pickle.load(fh)
E = sp.expand(d['E'])
A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)
sw = sp.sqrt(w); s1w = sp.sqrt(1-w)
# normalize all half-powers of w
def norm(e):
    e = sp.expand(e)
    for _ in range(20):
        rep = {}
        for p in e.atoms(sp.Pow):
            if p.base == w and sp.Rational(p.exp.denominator) == 2 and sp.Rational(p.exp.numerator) % 2 == 1:
                k = p.exp.numerator
                rep[p] = w**((k-1)//2)*sw
        if not rep: break
        e = sp.expand(e.subs(rep))
    return e
E = norm(E)
pure = sp.Integer(0); sq = sp.Integer(0)
for term in sp.Add.make_args(E):
    if term.has(sw):
        co = sp.expand(term/sw)
        sq += co
    else:
        pure += term
pure = sp.expand(pure); sq = sp.expand(sq)
print('pure has sqrt?', pure.has(sp.sqrt), ' sq has sqrt?', sq.has(sp.sqrt))
print()
print('Q1 =', sp.factor(pure))
print()
print('Q2 =', sp.factor(sq))
