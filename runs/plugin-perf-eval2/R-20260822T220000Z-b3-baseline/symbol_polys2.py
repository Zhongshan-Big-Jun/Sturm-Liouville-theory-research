# -*- coding: utf-8 -*-
"""Proper Q_n(C) via expand_trig; all multiple angles -> C only."""
import sympy as sp
y,C,s = sp.symbols('y C s', positive=True)
w = sp.symbols('w', positive=True)

def Tm(phase, rho):
    ww = w*sp.sqrt(rho)
    return sp.Matrix([[sp.cos(phase), sp.sin(phase)/ww], [-ww*sp.sin(phase), sp.cos(phase)]])

def Fn_expr(n):
    Tcell = Tm(y,s**2)*Tm(y,1)
    M = Tm(y,1)*Tcell**n
    return sp.expand(sp.together(M[0,1]*w))

def Q(n):
    F=Fn_expr(n)
    # expand all multiple angles to sin(y),cos(y)
    F=sp.expand_trig(sp.expand(F))
    # divide by sin(y); it should be polynomial factor
    Q0=sp.simplify(F/sp.sin(y))
    # substitute cos(y)->C, sin(y)^2->1-C^2
    Q1=sp.expand(Q0).subs({sp.sin(y)**2:1-C**2})
    Q1=sp.expand(Q1).subs({sp.cos(y):C})
    # eliminate any remaining sin(y)^2
    for _ in range(5):
        Q1=sp.expand(Q1.subs({sp.sin(y)**2:1-C**2}))
    Q1=sp.expand(Q1)
    # If any sin(y) remains (shouldn't), simplify*conjugate? but ignore
    return sp.factor(sp.Poly(Q1,C).as_expr())

for n in range(1,7):
    q=Q(n)
    print(f"n={n}:")
    print("   Q_n(C) =", sp.Poly(q,C).as_expr())
    print("   coeffs =", sp.Poly(q,C).all_coeffs())
    print()
