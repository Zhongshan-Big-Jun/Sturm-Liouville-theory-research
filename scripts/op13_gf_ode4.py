# -*- coding: utf-8 -*-
from sympy import symbols, Rational, expand, Poly, diff, together, factor, Function, cancel, simplify, collect, Derivative
import sympy as sp
j, c, t = symbols('j c t', positive=True)
mu0, mu1, mu2 = symbols('mu0 mu1 mu2')
F = Function('F')
theta = sp.Symbol('theta')

def theta_pow_plus(a, k, H):
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
        return apply_poly(theta_pow_plus(0, k, None), F(t)) - mu1*t*1**k - mu2*t**2*2**k
    if m == 1:
        return t * apply_poly(theta_pow_plus(1, k, None), F(t)) - t*mu0
    if m == 2:
        return t**2 * apply_poly(theta_pow_plus(2, k, None), F(t)) - t**2*mu0 - t**3*3**k*mu1
    if m == 3:
        return t**3 * apply_poly(theta_pow_plus(3, k, None), F(t))

lhs = c*c*(S(1,0) - S(0,0))
rhs = (8*c*S(3,1) - 12*c*S(2,1) + 4*c*S(1,1)) + c*c*S(1,1) \
      - (16*S(5,2) - 64*S(4,2) + (92+8*c)*S(3,2) - (56+20*c)*S(2,2) + (12+12*c)*S(1,2)) \
      + (16*S(5,3) - 112*S(4,3) + 284*S(3,3) - 308*S(2,3) + 120*S(1,3))
ode = sp.expand(lhs - rhs)

# Find min t power: express ode = sum t^m * P_m(F derivs, mu0..) ; do by substituting t->t, count
# simpler: evaluate ode with F(t) replaced by symbolic function H and collect
H = sp.Function('H')
odeH = ode.subs(F(t), H(t))
# expand and collect terms by power of t
expr = sp.expand(odeH)
# monomial powers: iterate over Add args
args = sp.Add.make_args(expr)
minpow = 99
for a_ in args:
    # power of t in a_
    pf = sp.Poly(a_, t)
    deg = pf.degree()
    minpow = min(minpow, deg)
print("min t power:", minpow)
expr2 = sp.expand(expr / t**minpow)
# substitute back F
expr2 = expr2.subs(H(t), F(t))
# collect by derivative order
F0=F(t); F1=sp.diff(F(t),t); F2=sp.diff(F(t),t,2); F3=sp.diff(F(t),t,3); F4=sp.diff(F(t),t,4); F5=sp.diff(F(t),t,5)
cole = sp.collect(sp.expand(expr2), [F5,F4,F3,F2,F1,F0,mu0,mu1,mu2], evaluate=False)
for key in cole:
    print("== ", key)
    print("   ", sp.factor(sp.simplify(cole[key])))
