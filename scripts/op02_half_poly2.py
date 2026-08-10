# -*- coding: utf-8 -*-
"""#2: half-string shooting with x = y/2.  Blocks phases (2x,...,2x,x), densities (1,R,1,...).
Dirichlet polynomial P^D_n(cos x) and mixed P^M_n(cos x)."""
import sympy as sp
w, s, x = sp.symbols('w s x', positive=True)

def shoot(blocks):
    u, up = sp.Integer(0), sp.Integer(1)
    for phi, rho in blocks:
        ww = w*sp.sqrt(rho)
        u, up = u*sp.cos(phi) + up*sp.sin(phi)/ww, -u*ww*sp.sin(phi) + up*sp.cos(phi)
    return sp.simplify(u), sp.simplify(up)

C = sp.symbols('C')
for n in (1, 2, 3, 4, 5):
    rho_last = 1 if (n+1) % 2 == 1 else s**2
    blocks = [(2*x, 1 if k % 2 == 0 else s**2) for k in range(n)] + [(x, rho_last)]
    uL, upL = shoot(blocks)
    out = []
    for name, expr in (("D", uL), ("M", upL)):
        e = sp.simplify(sp.expand(sp.expand_trig(expr*w)))
        # substitute cos(x)->C, sin(x)^2->1-C^2, sin(x)->sqrt(1-C^2)
        e = sp.expand(e.subs({sp.sin(x)**2: 1-C**2}))
        e = sp.expand(e.subs({sp.sin(x): sp.sqrt(1-C**2)}))
        e = sp.expand(e.subs({sp.cos(x): C}))
        e = sp.factor(sp.together(sp.expand(e)))
        out.append((name, e))
    print(f"n={n}:")
    for name, e in out:
        print(f"   {name}: {e}")
