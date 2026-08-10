# -*- coding: utf-8 -*-
"""#13(i): sequential matching with B = -3 fixed."""
from sympy import symbols, Rational, series, expand, solve, factor, Symbol
import sympy as sp

j, c = symbols('j c', positive=True)
t = Symbol('t')
C, D, E, F, G = symbols('C D E F G')

def a_exp(parity):
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
    print(f"===== parity {parity} =====")
    a1, a2, a3 = a_exp(parity)
    rho = (c/4)/j**2*(1 + (-3)/j + C/j**2 + D/j**3 + E/j**4 + F/j**5 + G/j**6)
    rho1 = rho.subs(j, j-1)
    rho2 = rho.subs(j, j-2)
    expr = rho - (a1 + a2/rho1 + a3/(rho1*rho2))
    expr_t = sp.series(expr.subs(j, 1/t), t, 0, 7).removeO()
    sub = {}
    names = [C, D, E, F, G]
    for k in range(0, 5):
        coeff = sp.factor(sp.expand(expr_t.coeff(t, k).subs(sub)))
        if coeff == 0:
            print(f"  t^{k}: 0 automatically")
            continue
        sol = solve(sp.Eq(coeff, 0), names[k])
        print(f"  t^{k}: {names[k]} = {sol}")
        if not sol:
            print("  *** no solution; stop"); break
        sub[names[k]] = sol[0]
    print("  full:", sub)
