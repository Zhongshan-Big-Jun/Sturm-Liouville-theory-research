# -*- coding: utf-8 -*-
"""fp_asym3.py: closed-form norm integrals for symmetric config, eps-expansion.
xi = delta*sqrt(R), s1 = c*sqrt(eps), s2 = 2pi - kap*eps.  fp condition f(a)=0.
"""
import sympy as sp
eps, xi, c, kap = sp.symbols("eps xi c kap", positive=True)
delta = xi*eps
s1 = c*sp.sqrt(eps)
s2 = 2*sp.pi - kap*eps
a_pt = sp.Rational(1,2) - delta
b_pt = sp.Rational(1,2) + delta

# ---- y1 even ----
th1 = s1*delta/eps
A1 = sp.cos(s1*a_pt)/(sp.sqrt(1/eps**2)*sp.sin(th1))
# int_0^a sin^2(s1 x) dx
I1L = a_pt/2 - sp.sin(2*s1*a_pt)/(4*s1)
# int_{-d}^{d} cos^2(s1/eps u) du = d + sin(2 s1 d/eps)/(2 s1/eps)
I1M_raw = delta + sp.sin(2*th1)/(2*s1/eps)
I1M = (1/eps**2)*A1**2*I1M_raw
I1R = sp.Rational(1,2) - b_pt - sp.sin(2*s1*(1-b_pt))/(4*s1)
# check: int_b^1 sin^2(s1(1-x)) dx, substitute t=1-x: int_0^{1-b} sin^2(s1 t) dt = (1-b)/2 - sin(2 s1 (1-b))/(4 s1)
n1 = sp.expand(I1L + I1M + I1R)

# ---- y2 odd ----
th2 = s2*delta/eps
B2 = -sp.sin(s2*a_pt)/sp.sin(th2)
I2L = a_pt/2 - sp.sin(2*s2*a_pt)/(4*s2)
I2M_raw = delta - sp.sin(2*th2)/(2*s2/eps)
I2M = (1/eps**2)*B2**2*I2M_raw
I2R = sp.Rational(1,2) - b_pt - sp.sin(2*s2*(1-b_pt))/(4*s2)
n2 = sp.expand(I2L + I2M + I2R)

y1a = sp.sin(s1*a_pt)
y2a = sp.sin(s2*a_pt)
fp = s1**2*y1a**2/n1 - s2**2*y2a**2/n2

print("series n1...")
n1s = sp.series(n1, eps, 0, 10).removeO()
print("n1 =", sp.collect(sp.simplify(n1s), eps))
print("series n2...")
n2s = sp.series(n2, eps, 0, 10).removeO()
print("n2 =", sp.collect(sp.simplify(n2s), eps))
print("series fp...")
fps = sp.series(fp, eps, 0, 8).removeO()
print("fp =", sp.collect(sp.simplify(fps), eps))

