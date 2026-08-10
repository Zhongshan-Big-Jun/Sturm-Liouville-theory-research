# -*- coding: utf-8 -*-
from sympy import symbols, Rational, expand, Poly, diff, together, factor, Function, cancel, simplify, collect
import sympy as sp
j, c, t = symbols('j c t', positive=True)
mu0, mu1, mu2 = symbols('mu0 mu1 mu2')
F = Function('F')

def theta_pow_plus(a, k):
    p = sp.Poly(sp.expand((sp.Symbol('T') + a)**k), sp.Symbol('T'))
    return [sp.expand(coef) for coef in p.all_coeffs()][::-1]

def apply_poly(coeffs, H):
    out = 0
    Hcur = H
    for n, co in enumerate(coeffs):
        out += co * Hcur
        Hcur = sp.diff(Hcur, t) * t
    return sp.expand(out)

def S(k, m):
    assert m in (0,1,2,3)
    if m == 0:
        return apply_poly(theta_pow_plus(0, k), F(t)) - mu1*t - mu2*t**2*2**k
    if m == 1:
        return t * apply_poly(theta_pow_plus(1, k), F(t)) - t*mu0
    if m == 2:
        return t**2 * apply_poly(theta_pow_plus(2, k), F(t)) - t**2*mu0 - t**3*3**k*mu1
    if m == 3:
        return t**3 * apply_poly(theta_pow_plus(3, k), F(t))

lhs = c*c*(S(1,0) - S(0,0))
rhs = (8*c*S(3,1) - 12*c*S(2,1) + 4*c*S(1,1)) + c*c*S(1,1) \
      - (16*S(5,2) - 64*S(4,2) + (92+8*c)*S(3,2) - (56+20*c)*S(2,2) + (12+12*c)*S(1,2)) \
      + (16*S(5,3) - 112*S(4,3) + 284*S(3,3) - 308*S(2,3) + 120*S(1,3))
ode = sp.expand(lhs - rhs)

# print ode with F derivatives kept, factored by t powers: substitute F(t)=X (symbol), derivatives = Xn
X = symbols('X'); X1 = symbols('X1'); X2 = symbols('X2'); X3 = symbols('X3'); X4 = symbols('X4'); X5 = symbols('X5')
subsmap = {F(t): X, sp.diff(F(t),t): X1, sp.diff(F(t),t,2): X2, sp.diff(F(t),t,3): X3, sp.diff(F(t),t,4): X4, sp.diff(F(t),t,5): X5}
odeX = sp.expand(ode.subs(subsmap))
poly = sp.Poly(odeX, t)
print("degree in t:", poly.degree())
for n in range(poly.degree()+1):
    co = poly.coeff_monomial(t**n)
    if co != 0:
        print(f"t^{n}: {sp.factor(co)}")
