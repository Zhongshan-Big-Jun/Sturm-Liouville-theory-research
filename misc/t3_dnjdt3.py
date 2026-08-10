# -*- coding: utf-8 -*-
"""t3_dnjdt3: split dNJ/dt = P1(A,t,sg,cg,w) + sqrt(w(1-w))*P2(A,t,sg,cg,w), factor parts."""
import sympy as sp, pickle, math

with open('misc/t3_dNJdt_split.pkl','rb') as fh: d = pickle.load(fh)
E = d['E']   # contains sqrt(w), sqrt(1-w) surds
A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)
sw = sp.sqrt(w); s1w = sp.sqrt(1-w)
# collect terms with sw*s1w vs pure
E = sp.expand(E)
pure = sp.Integer(0); sq = sp.Integer(0)
for term in sp.Add.make_args(E):
    if term.has(sw) and term.has(s1w):
        # factor out sw*s1w
        co = sp.expand(term/(sw*s1w))
        sq += co
    else:
        pure += term
# sq should now be polynomial in w (integer powers). Check
sq = sp.expand(sq)
print('pure terms:', len(sp.Add.make_args(pure)))
print('sq terms:', len(sp.Add.make_args(sq)))
print('sq has sqrt?', sq.has(sp.sqrt))
print('P2 =', sp.factor(sq))
print()
print('P1 =', sp.factor(pure))
