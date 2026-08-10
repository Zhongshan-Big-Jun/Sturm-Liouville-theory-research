# -*- coding: utf-8 -*-
"""#13(iii) completeness test: rational ratios of general degree.
Q1: e_j = P(j)/Q(j), deg P = deg Q = d, e_j -> 1 (root-1 branch).
    Does the fixed-point identity admit solutions beyond the degree-2 family (E^(tau), E+)?
Q2: e_j -> 0 (root-0 branch), deg Q = deg P + 2, leading c/(4 j^2).  Any rational solution?
"""
from sympy import symbols, Poly, expand, solve, cancel, Rational, factor
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

def solve_rational(parity, d, u=None, cval=None):
    """e_j = P(j)/Q(j), deg d, both monic leading 1 (for e->1), or leading c/4 / 1 (root-0)."""
    a1, a2, a3 = a_coeffs(parity, j, c)
    Pj = sum(p[k]*j**k for k in range(d+1))
    Qj = sum(q[k]*j**k for k in range(d+1))
    if u is None:
        # root-1 branch: leading coeffs both 1
        Pj = Pj.subs(p[d], 1); Qj = Qj.subs(q[d], 1)
    else:
        # root-0 branch: P ~ (c/4) j^{d-2}, Q ~ j^d  (e ~ c/(4 j^2))
        Pj = Pj.subs(p[d], 0).subs(p[d-1], 0)  # will fix below
        Pj = Pj + Rational(1)*0  # placeholder
        # simpler: normalize Q monic, P has no j^d, j^{d-1} terms; set p[d-2] = c/4
        Qj = Qj.subs(q[d], 1)
        Pj = Pj.subs(p[d-2], Rational(c)/4)
    ej   = Pj/Qj
    ejm1 = Pj.subs(j, j-1)/Qj.subs(j, j-1)
    ejm2 = Pj.subs(j, j-2)/Qj.subs(j, j-2)
    r = sp.together(a1 + a2/ejm1 + a3/(ejm1*ejm2) - ej)
    num, den = r.as_numer_denom()
    if cval is not None:
        num = num.subs(c, cval)
    Ppoly = Poly(expand(num), j)
    eqs = [cancel(co) for co in Ppoly.all_coeffs()]
    unknowns = [x for x in list(p)+list(q) if x in num.free_symbols and x is not c]
    try:
        sols = solve(eqs, unknowns, dict=True)
    except Exception as e:
        sols = ('ERR', type(e).__name__)
    return sols

print("=== root-1 branch, degree d, c symbolic: number of free parameters in solution set ===")
for parity in ('e','o'):
    for d in (1, 2, 3):
        sols = solve_rational(parity, d)
        if isinstance(sols, tuple):
            print(parity, "d=", d, sols); continue
        print(parity, "d=", d, ": #solutions =", len(sols), " first:", {k: v for k,v in (sols[0] if sols else {}).items()})
