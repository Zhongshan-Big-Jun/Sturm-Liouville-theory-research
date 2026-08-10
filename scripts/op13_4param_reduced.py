# -*- coding: utf-8 -*-
"""#13(iii): 4-param family with asymptotic reduction a = u + c."""
from sympy import symbols, Rational, together, Poly, expand, solve, cancel, factor
import sympy as sp

j, c = symbols('j c', positive=True)
cc_, b, d = symbols('cc b d')

def a_coeffs(parity, j, c):
    P = 8*c*j*j - 4*c*j + c*c*j/(j-1)
    Q = 4*j*(j-1)*(2*j-1)*(2*j-3) + 4*c*j*(2*j-3)
    R = 4*j*(j-2)*(2*j-3)*(2*j-5)
    lam = Rational(4)/c
    a1 = P/(c*c*j*j*lam)
    a2 = -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3 = R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    return a1, a2, a3

def residual4(parity, u, cval=None):
    a1, a2, a3 = a_coeffs(parity, j, c)
    a = u + cc_
    ej   = (j*j + a*j + b)/(j*j + cc_*j + d)
    ejm1 = ((j-1)**2 + a*(j-1) + b)/((j-1)**2 + cc_*(j-1) + d)
    ejm2 = ((j-2)**2 + a*(j-2) + b)/((j-2)**2 + cc_*(j-2) + d)
    r = together(a1 + a2/ejm1 + a3/(ejm1*ejm2) - ej)
    num, den = r.as_numer_denom()
    if cval is not None:
        num = num.subs(c, cval)
    return num

for parity in ('e','o'):
    usols = [Rational(-1,2), Rational(1,2)] if parity=='e' else [Rational(1,2), Rational(3,2)]
    for u in usols:
        print(f"===== parity={parity} u={u} =====")
        num = residual4(parity, u)
        Pj = Poly(expand(num), j)
        coeffs = Pj.all_coeffs()
        eqs = [cancel(co) for co in coeffs]
        # solve for (cc, b, d) with c symbolic
        try:
            sols = solve(eqs, [cc_, b, d], dict=True)
            print(f"  symbolic solutions: {sols}")
        except Exception as e:
            print(f"  symbolic solve failed: {type(e).__name__}")
            # numeric at c=1
            num1 = num.subs(c, 1)
            Pj1 = Poly(expand(num1), j)
            eqs1 = [cancel(co) for co in Pj1.all_coeffs()]
            sols1 = solve(eqs1, [cc_, b, d], dict=True)
            print(f"  c=1 solutions: {sols1}")
