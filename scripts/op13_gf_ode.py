# -*- coding: utf-8 -*-
"""#13(i): derive ODE for generating function F(t) = sum mu_j t^j from the mu-recurrence."""
from sympy import symbols, Rational, expand, collect, factor, Function, diff, simplify, together
import sympy as sp
j, c, t = symbols('j c t', positive=True)
F = Function('F')

# recurrence (even): c^2 mu_j = P_j mu_{j-1} - Q_j mu_{j-2} + R_j mu_{j-3}
# multiply by (j-1):  c^2 (j-1) mu_j = (j-1)(8cj^2-4cj) mu_{j-1} + c^2 j mu_{j-1} - (j-1) Q_j mu_{j-2} + (j-1) R_j mu_{j-3}
# with Q_j = 4j(j-1)(2j-1)(2j-3) + 4cj(2j-3), R_j = 4j(j-2)(2j-3)(2j-5)

# We'll sum over j>=3; express each term as operator on F.
# Operators: S_mu_k := sum_{j>=3} j^k mu_{j-m} t^j, etc.
# Use: sum_{j>=3} j^k mu_{j-1} t^j = t * sum_{j>=2} (j+1)^k mu_j t^j = t*(theta+1)^k (F - mu_0)
# sum j^k mu_{j-2} t^j = t^2 * (theta+2)^k (F - mu_0 - mu_1 t)
# sum j^k mu_{j-3} t^j = t^3 * (theta+3)^k (F - mu_0 - mu_1 t - mu_2 t^2)
# and sum_{j>=3} (j-1) j^k mu_{j-1} t^j = t*(theta+1)^{k+1}(F - mu_0) - t*(theta+1)^k(F-mu_0)

mu0, mu1, mu2 = symbols('mu0 mu1 mu2')
th = symbols('theta')  # t d/dt acting on F

def opA(k, shift, Fexpr, M):
    # sum_{j>=3} (j)^k mu_{j-shift} t^j, with mu_0..mu_2 handled
    # returns expression in theta applied to Fexpr
    pass

# Instead: do it manually.  Let G = F (theta operates).
# Use sympy: represent theta^k applied to X as (t*d/dt)^k X.
thF = F(t)
# helper: (theta + a)^n applied to function H
def theta_plus(a, n, H):
    # (t d/dt + a)^n H
    from sympy import expand
    # operator via repeated application using symbolic 't' derivative
    pass

# Simpler: define theta acting on a symbolic function H by diff.  We'll build operator polynomials in theta by repeated application.
def apply_theta_plus(theta_poly, H):
    # theta_poly: list of coefficients c_n for (t d/dt)^n
    out = 0
    Hcur = H
    for n, coef in enumerate(theta_poly):
        out += coef * Hcur
        Hcur = sp.diff(Hcur, t)*t
    return out
