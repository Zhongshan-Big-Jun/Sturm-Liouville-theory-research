# -*- coding: utf-8 -*-
"""derive_J2.py -- stepwise sympy derivation, avoiding full simplify."""
import sympy as sp
sp.init_printing()
a, c, q = sp.symbols('a c q', positive=True)
s, co = sp.sin(a), sp.cos(a)
Phi = co**2 + q**2*s**2
W = 3 + 2*a*co/s
D = q + c*Phi
G = -Phi*W/D + 2*c*a*Phi*(q**2-1)*s*co/D**2

Gc = sp.diff(G, c)
Ga = sp.diff(G, a)
ap = -a*Phi/D
Gprime_expr = sp.cancel(sp.together(Ga*ap + Gc))
print('Gprime numerator factors:')
print(sp.factor(sp.together(Gprime_expr).as_numer_denom()[0]))
