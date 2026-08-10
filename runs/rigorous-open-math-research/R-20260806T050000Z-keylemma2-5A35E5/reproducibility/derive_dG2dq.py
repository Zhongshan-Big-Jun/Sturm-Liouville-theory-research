# -*- coding: utf-8 -*-
"""derive_dG2dq.py -- closed form of dG2/dq at fixed c in (q, gamma) coordinates."""
import sympy as sp

q, g = sp.symbols('q g', positive=True)
s, co = sp.sin(g), sp.cos(g)
t = sp.tan(g)
Phi = (co**2 + q**2*s**2)
c = sp.atan(q*t)/(sp.pi - g)
D = q + c*Phi
K = q**2 - 1

# G as a function of (g, c, q): alpha2 = pi - g
# W(alpha2) = 3 + 2 (pi-g) cot(pi-g) = 3 - 2 (pi-g) cot(g)
W2 = 3 - 2*(sp.pi - g)/t
sc_a = -s*co   # sin(pi-g)cos(pi-g)
G = -Phi*W2/D - 2*c*(sp.pi - g)*Phi*K*sc_a/D**2

# partial in q at fixed (g, c):
G_q_part = sp.diff(G, q)
# partial in g at fixed (c, q):  dG/dg ; we need dG/da2 = -dG/dg
G_g_part = sp.diff(G, g)
G_a2_part = -G_g_part
# d alpha2/dq at fixed c: sin gamma cos gamma / (q + c Phi) = s*co/D
da2dq = s*co/D
dG2dq = sp.simplify(sp.expand(G_q_part + G_a2_part*da2dq))

print('dG2/dq|c (in q, gamma) = ')
print(sp.factor(dG2dq))
print()
u = sp.symbols('u', positive=True)
expr_u = sp.simplify(sp.expand(dG2dq.subs(g, sp.atan(u/q))))
print('dG2/dq|c in (q,u):')
print(sp.factor(expr_u))
