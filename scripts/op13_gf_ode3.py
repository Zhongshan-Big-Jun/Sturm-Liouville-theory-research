# -*- coding: utf-8 -*-
"""#13(i): inspect the ODE."""
from sympy import symbols, Rational, expand, Poly, diff, together, factor, Function, cancel, simplify, collect
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
# factor out t?  Find min power of t
terms = sp.Add.make_args(ode)
tpow = []
for tm in terms:
    tp = sp.Poly(tm, t).degree() if sp.Poly(tm, t).degree() >= 0 else 0
    tpow.append(sp.Poly(tm, t).degree())
print("t-powers:", sorted(set(tpow)))
# divide by t^2 (guessing)
ode2 = sp.expand(ode/t**2)
# write as sum of terms: A_n(t) F^{(n)}(t) etc. Collect by derivative order
F0 = F(t); F1 = sp.diff(F(t), t); F2 = sp.diff(F(t), t, 2); F3 = sp.diff(F(t), t, 3); F4 = sp.diff(F(t), t, 4); F5 = sp.diff(F(t), t, 5)
cole = sp.collect(ode2, [F5, F4, F3, F2, F1, F0, mu0, mu1, mu2], evaluate=False)
for key in cole:
    print("== ", key, " : ", sp.factor(sp.simplify(cole[key])))
