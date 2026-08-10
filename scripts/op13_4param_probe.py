# -*- coding: utf-8 -*-
"""#13(iii) part 4: numeric probe of 4-param family at fixed c."""
from sympy import symbols, Rational, together, Poly, expand, solve, cancel, nsimplify, groebner, Matrix
import sympy as sp
j, c = symbols('j c', positive=True)
a, b, cc, d = symbols('a b cc d')

def a_coeffs(parity, j, c):
    P = 8*c*j*j - 4*c*j + c*c*j/(j-1)
    Q = 4*j*(j-1)*(2*j-1)*(2*j-3) + 4*c*j*(2*j-3)
    R = 4*j*(j-2)*(2*j-3)*(2*j-5)
    lam = Rational(4)/c
    a1 = P/(c*c*j*j*lam)
    a2 = -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3 = R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    return a1, a2, a3

def eval_residual(jv, cv):
    a1, a2, a3 = a_coeffs('e', j, c)
    ej   = (j*j + a*j + b)/(j*j + cc*j + d)
    ejm1 = ((j-1)**2 + a*(j-1) + b)/((j-1)**2 + cc*(j-1) + d)
    ejm2 = ((j-2)**2 + a*(j-2) + b)/((j-2)**2 + cc*(j-2) + d)
    r = together(a1 + a2/ejm1 + a3/(ejm1*ejm2) - ej)
    num, den = r.as_numer_denom()
    val = num.subs([(j, jv), (c, cv)])
    return sp.factor(val)

for cv in (1, 3):
    print(f"===== c = {cv} =====")
    eqs = [eval_residual(jv, cv) for jv in (3,4,5,6,7)]
    # solve system numerically via sympy (rational coeffs)
    sols = solve(eqs, [a, b, cc, d], dict=True)
    print(f"  exact solutions: {sols}")
    # also try numeric roots via groebner->roots is hard; try nsolve from random starts
