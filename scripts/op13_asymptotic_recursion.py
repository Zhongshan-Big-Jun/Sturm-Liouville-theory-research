# -*- coding: utf-8 -*-
"""#13(iii): asymptotic recursion for u,v,w with u fixed; compare with closed forms."""
from sympy import symbols, Rational, solve, factor, expand, series, Symbol
import sympy as sp

j, c = symbols('j c', positive=True)
u, v, w = symbols('u v w')
t = Symbol('t')

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

for parity in ('e','o'):
    a1, a2, a3 = a_coeffs(parity, j, c)
    e_j   = 1 + u/j + v/j**2 + w/j**3
    e_jm1 = 1 + u/(j-1) + v/(j-1)**2 + w/(j-1)**3
    e_jm2 = 1 + u/(j-2) + v/(j-2)**2 + w/(j-2)**3
    expr = (a1 + a2/e_jm1 + a3/(e_jm1*e_jm2)) - e_j
    expr_t = expr.subs(j, 1/t)
    ser = sp.series(expr_t, t, 0, 6).removeO()
    t2 = sp.expand(ser.coeff(t,2))
    usols = solve(sp.Eq(t2,0), u)
    print(f"===== parity {parity}: u in {usols} =====")
    for us in usols:
        s2 = sp.expand(ser.subs(u, us))
        # t^3 coefficient -> equation in v (and c). NOTE: may depend on w through t^4 only.
        c3 = sp.factor(sp.expand(s2.coeff(t,3)))
        print(f"  u={us}: t^3 coeff = {c3}")
        vsols = solve(sp.Eq(c3,0), v)
        print(f"      v = {vsols}")
        for vs in vsols:
            s3 = sp.expand(s2.subs(v, vs))
            c4 = sp.factor(sp.expand(s3.coeff(t,4)))
            wsols = solve(sp.Eq(c4,0), w)
            print(f"      v={vs}: t^4 coeff = {sp.expand(s3.coeff(t,4))} -> w = {wsols}")
    # closed-form expansions for comparison
    print("  closed-form e_j (even/odd):")
    # E+ even: e=1+1/(2j); E- even: e=1-1/(2j)
    if parity=='e':
        for name, e in (("E+", 1+sp.Rational(1,2)/j), ("E-", 1-sp.Rational(1,2)/j)):
            ex = sp.series(e, t, 0, 5).removeO().subs(j, 1/t) if False else None
            print(f"    {name}: u={sp.diff(e,j) is not None and -1/sp.series(e,j,sp.oo,2).removeO()}") 
