# -*- coding: utf-8 -*-
"""derive_dGdc.py -- sympy derivation of total derivative dG/dc along a curve."""
import sympy as sp

a, c, q = sp.symbols('a c q', positive=True)
s, co = sp.sin(a), sp.cos(a)
Phi = co**2 + q**2*s**2
W = 3 + 2*a*co/s
D = q + c*Phi
G = -Phi*W/D + 2*c*a*Phi*(q**2-1)*s*co/D**2

# partial derivative in c
Gc = sp.simplify(sp.diff(G, c))
# partial derivative in a
Ga = sp.simplify(sp.diff(G, a))
ap = -a*Phi/D
dGdc = sp.simplify(sp.expand(Ga*ap + Gc))

print('Gc =', Gc)
print()
print('Ga =', Ga)
print()
print('dGdc =', sp.factor(dGdc))
