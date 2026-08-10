# -*- coding: utf-8 -*-
"""derive_J.py -- sympy derivation of G, Gprime, J, H, Fp at c=1/2."""
import sympy as sp

a, c, q = sp.symbols('a c q', positive=True)
s, co = sp.sin(a), sp.cos(a)
Phi = co**2 + q**2*s**2
W = 3 + 2*a*co/s
D = q + c*Phi
G = -Phi*W/D + 2*c*a*Phi*(q**2-1)*s*co/D**2

# partials
Gc = sp.diff(G, c)
Ga = sp.diff(G, a)
ap = -a*Phi/D
Gprime = sp.simplify(sp.expand(Ga*ap + Gc))
J = sp.simplify(sp.expand(G**2 + Gprime))

print('Gprime = ', sp.factor(Gprime))
print()
print('J = ', sp.factor(J))
