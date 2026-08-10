# -*- coding: utf-8 -*-
"""t3_bexpand: fully expand B in (A,t,sg,cg,w) form and group."""
import sympy as sp, pickle

A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)
F1 = 8*A**3*cg**2 - 8*A**3*sg**2 + 16*A**3 + 16*A**2*cg**3*sg + 16*A**2*cg*sg**3 + 26*A**2*cg*sg - 15*A*sg**2 + 15*cg*sg**3
F2 = (8*A**2*cg**4 - 8*A**2*cg**2*sg**2 - 56*A**2*cg**2*w + 58*A**2*cg**2 + 16*A**2*sg**2*w - 12*A**2*sg**2
      + 48*A**2*w**2 - 40*A**2*w + 66*A*cg**3*sg + 8*A*cg*sg**3 - 38*A*cg*sg*w + 15*A*cg*sg + cg**2*sg**2)
F3 = (-72*A**3*cg**3*w + 36*A**3*cg**3 + 96*A**3*cg*w**2 - 32*A**3*cg*w - 16*A**3*cg
      + 8*A**2*cg**4*sg - 8*A**2*cg**2*sg**3 + 140*A**2*cg**2*sg*w - 68*A**2*cg**2*sg + 8*A**2*sg**3*w
      - 140*A**2*sg*w**2 + 104*A**2*sg*w - 48*A*cg**3*sg**2*t**2 + 42*A*cg**3*sg**2 - 16*A*cg*sg**4*t**2
      + 72*A*cg*sg**2*t**2*w - 40*A*cg*sg**2*w + 15*A*cg*sg**2 - 32*cg**2*sg**3*t**2 - 15*cg**2*sg**3)
B = sp.expand(cg**2*sg*t*F1 - 2*A*sg*t*w*F2 - A*sp.sqrt(w*(1-w))*F3)
# split B into pure-w part and sqrt(w(1-w)) part
Bp = sp.Integer(0); Bs = sp.Integer(0)
for term in sp.Add.make_args(B):
    if term.has(sp.sqrt):
        co = sp.expand(term/sp.sqrt(w*(1-w)))
        Bs += co
    else:
        Bp += term
print('Bp =', sp.factor(Bp))
print()
print('Bs =', sp.factor(Bs))
print()
print('Bp terms:', len(sp.Add.make_args(Bp)), ' Bs terms:', len(sp.Add.make_args(Bs)))
