# -*- coding: utf-8 -*-
"""#13(iii) part 3: 4-parameter family e_j = (j^2+a j+b)/(j^2+c j+d)."""
from sympy import symbols, Rational, together, Poly, expand, solve, cancel, factor
import sympy as sp
j, c = symbols('j c', positive=True)
a, b, cc, d = symbols('a b cc d')

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

def residual4(parity):
    a1, a2, a3 = a_coeffs(parity, j, c)
    ej   = (j*j + a*j + b)/(j*j + cc*j + d)
    ejm1 = ((j-1)**2 + a*(j-1) + b)/((j-1)**2 + cc*(j-1) + d)
    ejm2 = ((j-2)**2 + a*(j-2) + b)/((j-2)**2 + cc*(j-2) + d)
    return together(a1 + a2/ejm1 + a3/(ejm1*ejm2) - ej)

for parity in ('e',):
    print(f"===== parity {parity}, 4-param family =====")
    r = residual4(parity)
    num, den = r.as_numer_denom()
    Pj = Poly(expand(num), j)
    coeffs = Pj.all_coeffs()
    print(f"  degree in j: {Pj.degree()}, #coeffs: {len(coeffs)}")
    eqs = [cancel(co) for co in coeffs]
    sols = solve(eqs, [a, b, cc, d], dict=True)
    print(f"  #solutions: {len(sols)}")
    for s in sols:
        print(f"    {s}")
