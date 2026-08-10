# -*- coding: utf-8 -*-
"""derive_dG2dq2.py -- dG2/dq closed form, avoid heavy simplification."""
import sympy as sp

q, g = sp.symbols('q g', positive=True)
s, co = sp.sin(g), sp.cos(g)
t = sp.tan(g)
Phi = (co**2 + q**2*s**2)
c = sp.atan(q*t)/(sp.pi - g)
D = q + c*Phi
K = q**2 - 1
W2 = 3 - 2*(sp.pi - g)/t
sc_a = -s*co
G = -Phi*W2/D - 2*c*(sp.pi - g)*Phi*K*sc_a/D**2

G_q_part = sp.diff(G, q)
G_g_part = sp.diff(G, g)
G_a2_part = -G_g_part
da2dq = s*co/D
dG2dq = sp.cancel(G_q_part + G_a2_part*da2dq)

num, den = sp.fraction(dG2dq)
print('num degree q:', sp.degree(num, q), 'g:', sp.degree(num, g))
print('denom =', sp.factor(den))
print()
print('num (expanded, factor of denom removed):')
print(sp.expand(num))
