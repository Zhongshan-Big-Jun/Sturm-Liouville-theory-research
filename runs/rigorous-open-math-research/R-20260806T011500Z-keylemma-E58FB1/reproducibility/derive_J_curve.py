# -*- coding: utf-8 -*-
"""derive_J_curve.py -- J along even curve parametrized by alpha; c = E(alpha)/alpha."""
import sympy as sp
a, q = sp.symbols('a q', positive=True)
s, co = sp.sin(a), sp.cos(a)
Phi = co**2 + q**2*s**2
W = 3 + 2*a*co/s
Ea = sp.atan(1/(q*sp.tan(a)))
c = Ea/a
D = q + c*Phi
G = -Phi*W/D + 2*c*a*Phi*(q**2-1)*s*co/D**2
# dG/dc along curve, parametrized by alpha: G'(c) = (dG/da)*(da/dc), da/dc = -a*Phi/D
Gda = sp.diff(G, a)
ap = -a*Phi/D
Gprime = sp.cancel(sp.together(Gda*ap))
J = sp.cancel(sp.together(G**2 + Gprime))
num, den = sp.fraction(sp.together(J))
num = sp.factor(num)
print('J_even num factors:')
print(num)
