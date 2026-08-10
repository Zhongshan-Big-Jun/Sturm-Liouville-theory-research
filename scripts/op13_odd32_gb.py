# -*- coding: utf-8 -*-
from sympy import symbols, Rational, together, Poly, expand, solve, cancel, factor, groebner, Symbol
import sympy as sp
j, c = symbols('j c', positive=True)
cc_, b, d = symbols('cc b d')

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

def resid_at(parity, u, cv, jv):
    a1, a2, a3 = a_coeffs(parity, j, c)
    a = u + cc_
    ej   = (j*j + a*j + b)/(j*j + cc_*j + d)
    ejm1 = ((j-1)**2 + a*(j-1) + b)/((j-1)**2 + cc_*(j-1) + d)
    ejm2 = ((j-2)**2 + a*(j-2) + b)/((j-2)**2 + cc_*(j-2) + d)
    r = together(a1 + a2/ejm1 + a3/(ejm1*ejm2) - ej)
    num, den = r.as_numer_denom()
    return num.subs([(j, jv), (c, cv)])

cv = 1
eqs = [sp.factor(resid_at('o', Rational(3,2), cv, jv)) for jv in (3,4,5,6)]
print("eq degrees:", [sp.Poly(sp.expand(e), cc_, b, d).total_degree() for e in eqs])
# Groebner basis over QQ[cc,b,d]
G = groebner(eqs, cc_, b, d, order='lex')
print("groebner size:", len(G))
for g in G:
    print("  ", g)
