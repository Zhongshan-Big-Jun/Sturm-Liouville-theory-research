# -*- coding: utf-8 -*-
"""W with st^2=1-ct^2, sg^2=1-cg^2 substituted; view structure."""
import sympy as sp
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
B1 = A*cg - 2*sg
B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
W = ( -2*A**3*B1*st**2*ct**4 + A**2*cg*B2*st**2*ct**2 - 2*A**3*sg*t*st*ct**5
      + A**2*sg*t*B4*st*ct**3 - A*cg**2*sg*t*B5*st*ct
      + 4*A**2*cg*sg**2*t**2*ct**4 - A*cg*sg**2*t**2*B7*ct**2 + 6*cg**3*sg**4*t**2 )
# substitute sg^2=1-cg^2 (keep sg for odd powers), st^2=1-ct^2
W = sp.expand(W.subs({sg**2: 1-cg**2, st**2: 1-ct**2}))
# collect by ct and cg
W = sp.expand(W)
print('terms:', len(sp.Add.make_args(W)))
Wc = sp.collect(sp.expand(W), [ct, cg])
print(Wc)
