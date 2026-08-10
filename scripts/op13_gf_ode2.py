# -*- coding: utf-8 -*-
"""#13(i): derive ODE for F(t)=sum mu_j t^j.  Operator S(k,m) = sum_{j>=3} j^k mu_{j-m} t^j."""
from sympy import symbols, Rational, expand, Poly, diff, together, factor, Function, cancel
import sympy as sp
j, c, t = symbols('j c t', positive=True)
mu0, mu1, mu2 = symbols('mu0 mu1 mu2')
F = Function('F')
theta = sp.Symbol('theta')

# We'll work symbolically: represent expressions in theta applied to F(t).
# Build S(k,m): operator polynomial in theta (list of coeffs), applied to F,
# minus constant terms depending on m and mu0..mu2.
# (theta + a)^k applied to F minus initials.
# S(k,0) = theta^k (F - mu0 - mu1 t - mu2 t^2):  constants: -mu1 t*1^k - mu2 t^2*2^k
# S(k,1) = t*(theta+1)^k (F - mu0):              constants: -t mu0
# S(k,2) = t^2*(theta+2)^k (F - mu0 - mu1 t):     constants: -t^2 mu0 - t^3 3^k mu1
# S(k,3) = t^3*(theta+3)^k F:                     constants: none
# and theta applied to constants of the form t^m * const gives m*const*t^m.

def theta_pow_plus(a, k, H):
    # (theta + a)^k H  as list of coeffs for theta^0..theta^k applied to H
    # expand symbolically
    p = sp.Poly(sp.expand((sp.Symbol('T') + a)**k), sp.Symbol('T'))
    return [sp.expand(coef) for coef in p.all_coeffs()][::-1]

def apply_poly(coeffs, H):
    # sum_n coeffs[n] * theta^n H  (theta = t d/dt)
    out = 0
    Hcur = H
    for n, co in enumerate(coeffs):
        out += co * Hcur
        Hcur = sp.diff(Hcur, t) * t
    return sp.expand(out)

def S(k, m):
    # returns expression for sum_{j>=3} j^k mu_{j-m} t^j  (k >= 1; m in 0..3)
    assert m in (0,1,2,3)
    if m == 0:
        expr = apply_poly(theta_pow_plus(0, k, None), F(t))
        # subtract mu1 t * 1^k + mu2 t^2 * 2^k  (from j=1,2 terms)
        expr = expr - mu1*t*1**k - mu2*t**2*2**k
        return expr
    if m == 1:
        expr = t * apply_poly(theta_pow_plus(1, k, None), F(t))
        expr = expr - t*mu0
        return expr
    if m == 2:
        expr = t**2 * apply_poly(theta_pow_plus(2, k, None), F(t))
        expr = expr - t**2*mu0 - t**3*3**k*mu1
        return expr
    if m == 3:
        expr = t**3 * apply_poly(theta_pow_plus(3, k, None), F(t))
        return expr

lhs = c*c*(S(1,0) - S(0,0))
rhs = (8*c*S(3,1) - 12*c*S(2,1) + 4*c*S(1,1)) + c*c*S(1,1) \
      - (16*S(5,2) - 64*S(4,2) + (92+8*c)*S(3,2) - (56+20*c)*S(2,2) + (12+12*c)*S(1,2)) \
      + (16*S(5,3) - 112*S(4,3) + 284*S(3,3) - 308*S(2,3) + 120*S(1,3))
ode = sp.expand(lhs - rhs)
# ode should be an expression in t, F(t), derivatives of F(t), and mu0..mu2 constants
# Write as differential equation.  Check structure:
print("ODE expression terms count:", len(sp.Add.make_args(ode)))
# group: all terms have some power of t and derivatives. Divide by common t power?
print(sp.factor(ode)[:200] if isinstance(sp.factor(ode), str) else "factor ok")
