# -*- coding: utf-8 -*-
"""#13(iii): classify product solutions E_j = prod_{k=1}^j (1 + alpha/(k+gamma))."""
from sympy import symbols, Rational, together, Poly, expand, solve, cancel
import sympy as sp

j, c = symbols('j c', positive=True)
a_, g_ = symbols('alpha gamma')

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

def residual(parity):
    a1, a2, a3 = a_coeffs(parity, j, c)
    e_j   = 1 + a_/(j+g_)
    e_jm1 = 1 + a_/(j-1+g_)
    e_jm2 = 1 + a_/(j-2+g_)
    return together(a1 + a2/e_jm1 + a3/(e_jm1*e_jm2) - e_j)

for parity in ('e','o'):
    print(f"===== parity {parity} =====")
    r = residual(parity)
    num, den = r.as_numer_denom()
    Pj = Poly(expand(num), j)
    coeffs = Pj.all_coeffs()
    print(f"  degree in j: {Pj.degree()}, #coeffs: {len(coeffs)}")
    eqs = [cancel(co) for co in coeffs]
    sols = solve(eqs, [a_, g_], dict=True)
    print(f"  solutions (alpha,gamma): {sols}")
    for s in sols:
        ok = True
        for cv in (1, 3, 10):
            for jv in range(3, 41):
                val = r.subs([(j, jv), (c, cv), (a_, s[a_]), (g_, s[g_])])
                val = cancel(val)
                if val != 0:
                    ok = False; break
            if not ok: break
        print(f"    verify: {s} -> all-zero residual = {ok}")
