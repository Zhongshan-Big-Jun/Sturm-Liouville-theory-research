# -*- coding: utf-8 -*-
"""Compute Q_n(C) = F_n(y)/sin(y) expressed as polynomial in C = cos(y), for n=1..6."""
import sympy as sp

y,C,s = sp.symbols('y C s', positive=True)

def T1(phase, rho):
    ww = sp.symbols('w', positive=True)
    return sp.Matrix([[cos_y(phase), sin_p(phase)/ww], [-ww*sin_p(phase), cos_y(phase)]])

# Use a dummy omega w; it cancels. Since M01*w polynomial in y.
w = sp.symbols('w', positive=True)
def Tm(phase, rho):
    ww = w*sp.sqrt(rho)
    return sp.Matrix([[sp.cos(phase), sp.sin(phase)/ww], [-ww*sp.sin(phase), sp.cos(phase)]])

def Fn_expr(n):
    Tcell = Tm(y,s**2) * Tm(y,1)
    M = Tm(y,1) * Tcell**n
    return sp.expand(sp.together(M[0,1]*w))

def to_C(expr):
    e = sp.expand(sp.expand_trig(expr))
    e = sp.expand(e).subs({sp.cos(y): C, sp.sin(y)**2: 1-C**2})
    e = sp.expand(e).subs({sp.sin(y)*C: sp.sqrt(1-C**2)*C})  # not valid, but avoid
    return e

# Better: replace sin(y)^k * cos(y)^m; keep sin(y)^odd factor out.
def q_poly(n):
    F=Fn_expr(n)
    # factor sin(y) symbolically: divide
    Q=sp.simplify(F / sp.sin(y))
    # Now Q is polynomial in sin^2, cos.
    Q=sp.expand(Q)
    # replace sin(y)^2 -> 1-C^2
    Q=Q.subs({sp.sin(y)**2: 1-C**2})
    Q=sp.expand(Q)
    # There may be sin(y)^4 etc already handled; replace all powers recursively
    for _ in range(6):
        Q=sp.expand(Q.subs({sp.sin(y)**4: (1-C**2)**2}))
        Q=sp.expand(Q.subs({sp.sin(y)**2: 1-C**2}))
    Q=sp.expand(Q)
    # remove any stray sin via expansion
    Q=sp.expand(Q)
    return sp.factor(Q)

for n in range(1,7):
    Q=q_poly(n)
    print(f"n={n}:")
    print("   ", sp.Poly(Q, C).as_expr())
    print("   coeffs", sp.Poly(Q, C).all_coeffs())
    print()
