# -*- coding: utf-8 -*-
"""Closed forms of G, Gc, Gx, u composed on the true curve (2nd phase), in (gamma,q)."""
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

c2 = sp.atan(q*sp.tan(g))/(sp.pi - g)
subs = {x: sp.pi - g, c: c2}

for name, f in [('G',G),('Gc',Gc),('Gx',Gx),('u',u)]:
    comp = sp.simplify(f.subs(subs))
    print('===== %s composed =====' % name)
    print(sp.pretty(comp)[:2500])
    print()
