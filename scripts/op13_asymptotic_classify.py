# -*- coding: utf-8 -*-
"""#13(iii) FIXED: asymptotic classification of fixed-point trajectories e_j -> 1.
Solve order-by-order: t^2 -> u, then t^3 -> v (given u), then t^4 -> w (given u,v).
"""
from sympy import symbols, Rational, together, Poly, expand, solve, cancel, series, Symbol, simplify, factor
import sympy as sp

j, c = symbols('j c', positive=True)

def a_coeffs(parity, j, c):
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

u, v, w = symbols('u v w')
for parity in ('e','o'):
    print(f"===== parity {parity} =====")
    a1, a2, a3 = a_coeffs(parity, j, c)
    e_j   = 1 + u/j + v/j**2 + w/j**3
    e_jm1 = 1 + u/(j-1) + v/(j-1)**2 + w/(j-1)**3
    e_jm2 = 1 + u/(j-2) + v/(j-2)**2 + w/(j-2)**3
    rhs = a1 + a2/e_jm1 + a3/(e_jm1*e_jm2)
    expr = rhs - e_j
    t = Symbol('t')
    expr_t = expr.subs(j, 1/t)
    ser = sp.series(expr_t, t, 0, 5).removeO()
    # order t^2 gives u
    coef2 = sp.expand(ser.coeff(t,2))
    usols = solve(sp.Eq(coef2, 0), u)
    print(f"  coeff t^2 = {sp.factor(coef2)}  ->  u in {usols}")
    for us in usols:
        ser2 = sp.expand(ser.subs(u, us))
        coef3 = sp.expand(ser2.coeff(t,3))
        vsols = solve(sp.Eq(coef3, 0), v)
        print(f"    u={us}: coeff t^3 = {sp.factor(coef3)} -> v in {vsols}")
        for vs in vsols:
            ser3 = sp.expand(ser2.subs(v, vs))
            coef4 = sp.expand(ser3.coeff(t,4))
            wsols = solve(sp.Eq(coef4, 0), w)
            print(f"      v={vs}: coeff t^4 = {sp.factor(coef4)} -> w in {wsols}")
