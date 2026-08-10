# -*- coding: utf-8 -*-
"""#2: extract polynomial P_n(C) whose root C_n = cos(y_n) gives the balanced pair (y_n, y_{n+1})."""
import sympy as sp
w, s = sp.symbols('w s', positive=True)
y = sp.symbols('y')
C, S = sp.cos(y), sp.sin(y)

def T1(phase, rho):
    ww = w*sp.sqrt(rho)
    return sp.Matrix([[sp.cos(phase), sp.sin(phase)/ww], [-ww*sp.sin(phase), sp.cos(phase)]])

def Fn(n):
    Tcell = T1(y, 1)
    Tcell = T1(y, s**2) @ Tcell
    Tfinal = T1(y, 1)
    M = Tfinal * Tcell**n
    D = sp.simplify(sp.together(M[0,1]*w))
    D2 = sp.expand(D).subs({sp.sin(y): S, sp.cos(y): C})
    return sp.trigsimp(D2, method='fu')

for n in (1, 2, 3, 4):
    F = Fn(n)
    # F = sin(y) * Q(C, S^2).  divide by sin y
    Q = sp.simplify(F / S)
    Q = sp.expand(Q).subs({C**2: 1-S**2}).subs(S**2, 1-C**2)
    Q = sp.simplify(sp.expand(Q))
    print(f"n={n}: Q(C) = {sp.factor(Q)}")
    print()
