# -*- coding: utf-8 -*-
"""#13(i): matched asymptotics of the minimal ratio trajectory rho_j ~ A/j^2 (1 + B/j + C/j^2 + ...)."""
from sympy import symbols, Rational, series, expand, solve, factor, Symbol
import sympy as sp

j, c = symbols('j c', positive=True)
t = Symbol('t')

def a_exp(parity, order=8):
    if parity == 'e':
        P = 8*c*j*j - 4*c*j + c*c*j/(j-1)
        Q = 4*j*(j-1)*(2*j-1)*(2*j-3) + 4*c*j*(2*j-3)
        R = 4*j*(j-2)*(2*j-3)*(2*j-5)
    else:
        P = 8*c*j*j + 4*c*j + c*c*j/(j-1)
        Q = 4*j*(j-1)*(2*j-1)*(2*j+1) + 4*c*j*(2*j-1)
        R = 4*j*(j-2)*(2*j-1)*(2*j-3)
    lam = Rational(4)/c
    a1 = P/(c*c*j*j*lam)
    a2 = -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3 = R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    return a1, a2, a3

A, B, C, D = symbols('A B C D')
for parity in ('e','o'):
    print(f"===== parity {parity} =====")
    a1, a2, a3 = a_exp(parity)
    # rho_j = A/j^2 (1 + B/j + C/j^2 + D/j^3)
    rho_j   = A/j**2*(1 + B/j + C/j**2 + D/j**3)
    rho_jm1 = rho_j.subs(j, j-1)
    rho_jm2 = rho_j.subs(j, j-2)
    expr = rho_j - (a1 + a2/rho_jm1 + a3/(rho_jm1*rho_jm2))
    expr_t = sp.series(expr.subs(j, 1/t), t, 0, 5).removeO()
    # t^0: leading balance
    c0 = sp.factor(sp.expand(expr_t.coeff(t,0)))
    print(f"  t^0: {c0}")
    solA = solve(sp.Eq(c0, 0), A)
    print(f"  A = {solA}")
    A0 = [s for s in solA if s != 0][0]
    sub = {A: A0}
    c1 = sp.factor(sp.expand(expr_t.coeff(t,1).subs(sub)))
    print(f"  t^1: {c1}")
    solB = solve(sp.Eq(c1, 0), B)
    print(f"  B = {solB}")
    sub[B] = solB[0]
    c2 = sp.factor(sp.expand(expr_t.coeff(t,2).subs(sub)))
    print(f"  t^2: {c2}")
    solC = solve(sp.Eq(c2, 0), C)
    print(f"  C = {solC}")
