# -*- coding: utf-8 -*-
"""Factor the numerator of composed J2_2d in (gamma,q). Try to detect structure."""
import sympy as sp

x, c, q = sp.symbols('x c q', positive=True)
g = sp.symbols('gamma', positive=True)
sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x*cx/sx
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
Gx = sp.simplify(sp.diff(G, x))
Gc = sp.simplify(sp.diff(G, c))
u = x*Ph/D
J = sp.simplify(G**2 - u*Gx + Gc)

c2 = sp.atan(q*sp.tan(g))/(sp.pi - g)
J2 = sp.simplify(J.subs({x: sp.pi - g, c: c2}))
print('J2 composed:')
num, den = sp.fraction(sp.together(J2))
print('denominator:', sp.factor(den))
print('numerator degree (g):', sp.degree(num, g), ' (q):', sp.degree(num, q))
f = sp.factor(num)
print('factor:', f)
