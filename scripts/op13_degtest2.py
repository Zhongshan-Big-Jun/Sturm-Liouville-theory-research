# -*- coding: utf-8 -*-
"""#13(iii) degree test at c=1 (exact rational): root-1 branch, deg d in {1,2,3}."""
from sympy import symbols, Poly, expand, solve, cancel, Rational
import sympy as sp

j, c = symbols('j c', positive=True)
p = symbols('p0:8'); q = symbols('q0:8')

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

def solve_rational_c1(parity, d):
    a1, a2, a3 = a_coeffs(parity, j, 1)
    Pj = sum(p[k]*j**k for k in range(d+1)).subs(p[d], 1)
    Qj = sum(q[k]*j**k for k in range(d+1)).subs(q[d], 1)
    ej = Pj/Qj
    ejm1 = Pj.subs(j, j-1)/Qj.subs(j, j-1)
    ejm2 = Pj.subs(j, j-2)/Qj.subs(j, j-2)
    r = sp.together(a1 + a2/ejm1 + a3/(ejm1*ejm2) - ej)
    num, den = r.as_numer_denom()
    num = num.subs(c, 1)
    Ppoly = Poly(expand(num), j)
    eqs = [cancel(co) for co in Ppoly.all_coeffs()]
    unk = [x for x in list(p)+list(q) if x in num.free_symbols and x is not c and x is not j]
    print(f"  parity={parity} d={d}: {len(eqs)} equations, {len(unk)} unknowns: {unk}")
    sols = solve(eqs, unk, dict=True)
    print(f"    #solution-branches = {len(sols)}")
    for s in sols[:6]:
        print("      ", s)
    return sols

for parity in ('e','o'):
    for d in (1, 2):
        solve_rational_c1(parity, d)
