# -*- coding: utf-8 -*-
import sympy as sp
w, s = sp.symbols('w s', positive=True)
y = sp.symbols('y')

def shoot(blocks):
    u, up = sp.Integer(0), sp.Integer(1)
    for phi, rho in blocks:
        ww = w*sp.sqrt(rho)
        u, up = u*sp.cos(phi) + up*sp.sin(phi)/ww, -u*ww*sp.sin(phi) + up*sp.cos(phi)
    return sp.simplify(u), sp.simplify(up)

C = sp.symbols('C')
for n in (1, 2, 3, 4):
    rho_last = 1 if (n+1) % 2 == 1 else s**2
    blocks = [(y, 1 if k % 2 == 0 else s**2) for k in range(n)] + [(y/2, rho_last)]
    uL, upL = shoot(blocks)
    print(f"===== n={n} (half-string, {n+1} blocks) =====")
    for name, expr in (("Dirichlet", uL), ("mixed", upL)):
        e = sp.simplify(sp.expand(expr*w))
        e = sp.expand(sp.expand_trig(e))
        # substitute sin(y)^2 -> 1-C^2, sin(y) -> sqrt(1-C^2)
        eC = sp.expand(e.subs({sp.sin(y)**2: 1-C**2}))
        eC = sp.expand(eC.subs({sp.sin(y): sp.sqrt(1-C**2)}))
        eC = sp.expand(eC).subs(sp.cos(y), C)
        eC = sp.simplify(sp.expand(eC))
        eC = sp.factor(sp.together(eC))
        print(f"  {name}: {eC}")
