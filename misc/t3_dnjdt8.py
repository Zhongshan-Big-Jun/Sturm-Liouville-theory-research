# -*- coding: utf-8 -*-
"""t3_dnjdt8: recompute parity split and save."""
import sympy as sp, pickle

with open('misc/t3_dNJdt_split.pkl','rb') as fh: d = pickle.load(fh)
E = sp.expand(d['E'])
A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)
v, u = sp.symbols('v u', positive=True)
E2 = sp.expand(E.subs({w: v**2, sp.sqrt(w): v, sp.sqrt(1-w): u}))
E0 = sp.expand(E2.subs(u, 0))
E1 = sp.expand((E2 - E0)/u)
E0e = sp.expand(E0.subs(v, 0)); E0o = sp.expand((E0-E0e)/v)
E1e = sp.expand(E1.subs(v, 0)); E1o = sp.expand((E1-E1e)/v)
def to_w(expr):
    e = sp.expand(expr)
    return sp.expand(e.subs(v**2, w))
P1a = to_w(E0e); P1b = to_w(E0o); P2a = to_w(E1e); P2b = to_w(E1o)
print('P2a =', P2a)
print('P1a =', P1a)
print('P1b =', P1b)
print('P2b =', P2b)
with open('misc/t3_dNJdt_parity.pkl','wb') as fh: pickle.dump({'P1a':P1a,'P1b':P1b,'P2a':P2a,'P2b':P2b}, fh)
