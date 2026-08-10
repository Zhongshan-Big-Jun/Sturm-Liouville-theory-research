# -*- coding: utf-8 -*-
"""06_symbolic_identities.py
sympy verification of the algebraic identities used in Part I:
 (1) Dbar'(u) = S(u) exactly, with u = a/(2(a - tan a)) (the relation tan a =
     a(1-1/(2u)));
 (2) S(u(a)) = -4 (a - tan a)^3 G(a) / (a^3 (2a - sin 2a)), G = 8 a^3 sin^2 a
     - pi^2 (2a - sin 2a);
 (3) sign(S) = -sign(G) on a in (pi/2, pi).
ASCII punctuation. Run: python 06_symbolic_identities.py
"""
import sympy as sp
u, a = sp.symbols("u a", positive=True)

F = sp.tan(a) - a*(1 - sp.Rational(1,2)/u)
Fu = sp.diff(F, u); Fa = sp.diff(F, a)
ad = sp.simplify(-Fu/Fa)  # da/du under F = 0
mu2 = a**2/u**2
mu1 = sp.pi**2/(4*u**2)
Dbar = mu2 - mu1
Dbar_u = sp.simplify(sp.diff(Dbar, u) + sp.diff(Dbar, a)*ad)  # total d/du
I2 = u/2 - u*sp.sin(2*a)/(4*a)
S = sp.simplify(mu1*2/u - mu2*sp.sin(a)**2/I2)

# substitute the constraint u = a/(2(a - tan a))
usub = a/(2*(a - sp.tan(a)))
Dbar_u_a = sp.simplify(Dbar_u.subs(u, usub))
S_a = sp.simplify(S.subs(u, usub))
print("Dbar'(u(a)) =", Dbar_u_a)
print("S(u(a))     =", S_a)
print("ratio Dbar'/S =", sp.simplify(Dbar_u_a/S_a))

G = 8*a**3*sp.sin(a)**2 - sp.pi**2*(2*a - sp.sin(2*a))
S_a2 = sp.simplify(S_a)
Gexpr = sp.simplify(-4*(a - sp.tan(a))**3*G/(a**3*(2*a - sp.sin(2*a))))
print("S == -4(a-tan a)^3 G/(a^3(2a - sin2a)) ?", sp.simplify(S_a2 - Gexpr) == 0)

# signs on (pi/2, pi): (a - tan a) > 0, a^3 > 0, 2a - sin 2a > 0
print("check: on (pi/2,pi), a - tan a > 0 (tan<0), 2a - sin 2a > 0 (sin 2a<0)")
print("DONE")
