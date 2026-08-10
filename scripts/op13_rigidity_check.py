# -*- coding: utf-8 -*-
"""#13(iii): verify rigidity induction: at u=-1/2 (even) / u=1/2 (odd), the t^{k+2}
coefficient is (k+1)*x_k + 0*(earlier), forcing all higher coefficients to vanish."""
from sympy import symbols, Rational, solve, factor, expand, series, Symbol, Poly
import sympy as sp

j, c = symbols('j c', positive=True)
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

# generic e_j = 1 + x1/j + x2/j^2 + ... + x6/j^6
xs = symbols('x1:7')
e_j = 1 + sum(xs[k] / j**(k+1) for k in range(6))
e_jm1 = e_j.subs(j, j-1)
e_jm2 = e_j.subs(j, j-2)

for parity in ('e','o'):
    print(f"===== parity {parity} =====")
    a1, a2, a3 = a_coeffs(parity, j, c)
    expr = (a1 + a2/e_jm1 + a3/(e_jm1*e_jm2)) - e_j
    expr_t = sp.series(expr.subs(j, 1/t), t, 0, 8).removeO()
    # t^2 condition -> x1
    t2 = sp.factor(sp.expand(expr_t.coeff(t,2)))
    uu = solve(sp.Eq(t2, 0), xs[0])
    print(f"  x1 = {uu}")
    u = uu[0]  # take rigid branch for each parity
    # set x1, then recursively: coefficient t^{k+2} should be (k+1)*x_k + c-independent*earlier(0)
    sub = {xs[0]: u}
    for k in range(1, 6):
        ck = sp.factor(sp.expand(expr_t.coeff(t, k+2).subs(sub)))
        # linear part in x_{k+1}? No: coefficient t^{k+2} involves x_{k+1}? Let's see: x_m appears at order t^{m+1}.
        # So t^{k+2} involves x_{k+1}. Solve for x_{k+1}:
        xk1 = xs[k]
        sol = solve(sp.Eq(ck, 0), xk1)
        print(f"  k={k}: t^{k+2} coeff = {ck}")
        print(f"      -> x{k+1} = {sol}")
        if sol:
            sub[xk1] = sol[0]
