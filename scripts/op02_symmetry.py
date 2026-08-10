# -*- coding: utf-8 -*-
"""#2: (a) verify F_n(pi - y) = F_n(y) symbolically; (b) clean polynomials in C=cos(x)."""
import sympy as sp
w, s = sp.symbols('w s', positive=True)
y = sp.symbols('y')

def T1(phase, rho):
    ww = w*sp.sqrt(rho)
    return sp.Matrix([[sp.cos(phase), sp.sin(phase)/ww], [-ww*sp.sin(phase), sp.cos(phase)]])

def Fn(n):
    Tcell = T1(y, s**2) @ T1(y, 1)
    M = T1(y, 1) * Tcell**n
    return sp.simplify(sp.together(M[0,1]*w))

print("=== (a) F_n(pi-y) vs F_n(y) ===")
for n in (1, 2, 3, 4):
    F = Fn(n)
    Fp = F.subs(y, sp.pi - y)
    diff = sp.simplify(sp.expand_trig(sp.expand(F - Fp)))
    diff = sp.trigsimp(diff, method='fu')
    print(f"n={n}: F(pi-y) - F(y) = {diff}")

print()
print("=== (b) clean polynomials P_n(C), C = cos(x), x = y/2 ===")
x = sp.symbols('x')
C = sp.symbols('C')
for n in (1, 2, 3):
    F = Fn(n)
    # substitute y = 2x, divide by sin(2x)
    Fx = sp.expand(sp.expand_trig(F.subs(y, 2*x)))
    Fx = sp.simplify(Fx / sp.sin(2*x))
    Fx = sp.expand(Fx)
    for k in (1, 2, 3):
        Fx = sp.expand(Fx.subs({sp.cos(k*x): sp.expand_trig(sp.cos(k*x)).subs({sp.cos(x): C})}))
    Fx = sp.expand(Fx.subs({sp.cos(x): C}))
    Fx = sp.expand(Fx.subs({sp.sin(x)**2: 1-C**2}))
    Fx = sp.factor(sp.expand(Fx))
    print(f"n={n}: P_n(C) = {Fx}")
