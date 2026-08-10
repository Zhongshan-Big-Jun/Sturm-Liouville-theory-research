# -*- coding: utf-8 -*-
"""fp_asym2.py: exact symmetric-config system expanded in eps = 1/sqrt(R).
Unknowns: xi = delta*sqrt(R) (O(1)), c = s1/sqrt(eps) (O(1)), kap = kappa*sqrt(R) (O(1)).
Builds exact n1, n2, y1(a), y2(a) for even/odd modes and expands f(a)=0.
"""
import sympy as sp

eps, xi, c, kap = sp.symbols("eps xi c kap", positive=True)
delta = xi*eps
s1 = c*sp.sqrt(eps)
s2 = 2*sp.pi - kap*eps
a_pt = sp.Rational(1,2) - delta          # left barrier edge
b_pt = sp.Rational(1,2) + delta
mu = sp.Rational(1,2) - delta            # a_pt

# ---- y1: even mode ----
# [0, a]: sin(s1 x) ; [a, b]: A cos(s1 sqrt(R)(x-1/2)) ; [b, 1]: sin(s1 (1-x))
th1 = s1*delta/eps                        # s1 sqrt(R) delta = s1 delta / eps
A1 = sp.cos(s1*(sp.Rational(1,2)-delta))/(sp.sqrt(R:=1/eps**2)*sp.sin(th1))
# pieces of y1 for norm integrals
y1_left = sp.sin(s1*x1) if False else None
x = sp.symbols("x")
# norm1 = int_0^a sin^2(s1 x) dx + R int_a^b (A1 cos(s1/eps (x-1/2)))^2 dx + int_b^1 sin^2(s1 (1-x)) dx
I1L = sp.integrate(sp.sin(s1*x)**2, (x, 0, a_pt))
I1M = sp.Rational(0) if False else None
# barrier: A1 cos(s1 sqrt(R)(x-1/2)); let u = x-1/2, u from -delta to delta
I1M = R*A1**2*sp.integrate(sp.cos(s1/eps*sp.symbols("u"))**2, (sp.symbols("u"), -delta, delta))
I1R = sp.integrate(sp.sin(s1*(1-x))**2, (x, b_pt, 1))
n1 = I1L + I1M + I1R

# y1 at a_pt
y1a = sp.sin(s1*a_pt)

# ---- y2: odd mode ----
# [0,a]: sin(s2 x); [a,b]: B sin(s2 sqrt(R)(x-1/2)); [b,1]: -sin(s2(1-x))
th2 = s2*delta/eps
B2 = -sp.sin(s2*(sp.Rational(1,2)-delta))/sp.sin(th2)
I2L = sp.integrate(sp.sin(s2*x)**2, (x, 0, a_pt))
I2M = R*B2**2*sp.integrate(sp.sin(s2/eps*sp.symbols("u"))**2, (sp.symbols("u"), -delta, delta))
I2R = sp.integrate(sp.sin(s2*(1-x))**2, (x, b_pt, 1))
n2 = I2L + I2M + I2R
y2a = sp.sin(s2*a_pt)

# fp condition: s1^2*y1a^2/n1 - s2^2*y2a^2/n2 = 0
fpcond = s1**2*y1a**2/n1 - s2**2*y2a**2/n2

print("expanding n1...")
n1s = sp.series(sp.expand(sp.simplify(n1)), eps, 0, 8).removeO()
print("n1 =", sp.collect(sp.simplify(n1s), eps))
print("expanding n2...")
n2s = sp.series(sp.expand(sp.simplify(n2)), eps, 0, 8).removeO()
print("n2 =", sp.collect(sp.simplify(n2s), eps))

