# -*- coding: utf-8 -*-
"""t3_mfactor: expand and factor M = cg^2 F1 - 2Aw F2."""
import sympy as sp, pickle

A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)
F1 = 8*A**3*cg**2 - 8*A**3*sg**2 + 16*A**3 + 16*A**2*cg**3*sg + 16*A**2*cg*sg**3 + 26*A**2*cg*sg - 15*A*sg**2 + 15*cg*sg**3
F2 = (8*A**2*cg**4 - 8*A**2*cg**2*sg**2 - 56*A**2*cg**2*w + 58*A**2*cg**2 + 16*A**2*sg**2*w - 12*A**2*sg**2
      + 48*A**2*w**2 - 40*A**2*w + 66*A*cg**3*sg + 8*A*cg*sg**3 - 38*A*cg*sg*w + 15*A*cg*sg + cg**2*sg**2)
M = sp.expand(cg**2*F1 - 2*A*w*F2)
print('M =', M)
print()
try:
    print('factor:', sp.factor(M))
except Exception as e:
    print('factor failed:', e)
# reduce sg^2 = 1-cg^2
Mr = sp.expand(M)
for _ in range(6):
    Mr = sp.expand(Mr.subs(sg**2, 1-cg**2))
Mr = sp.expand(Mr)
print()
print('M reduced (sg^2=1-cg^2):')
for term in sorted(sp.Add.make_args(Mr), key=str): print('   ', term)
