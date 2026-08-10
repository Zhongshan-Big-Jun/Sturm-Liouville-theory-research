# -*- coding: utf-8 -*-
"""Factor Psi~'(x;m) numerator to seek an elementary proof for m<=sqrt(1.5)."""
import sympy as sp

x, q = sp.symbols('x q', positive=True)  # q = m^2 - 1, 0<=q<=1/2
W = 1 + q*sp.cos(x)**2
Psi = x*sp.cos(x)/sp.sin(x) + q*x*sp.sin(x)*sp.cos(x)/W
dPsi = sp.simplify(sp.diff(Psi, x))
print("dPsi (q-form):", dPsi)
# multiply by positive factors to clear denominators
expr = sp.simplify(dPsi * sp.sin(x)**2 * W**2)
expr = sp.factor(sp.trigsimp(sp.expand_trig(expr)))
print()
print("dPsi * sin^2 * W^2 =", expr)
