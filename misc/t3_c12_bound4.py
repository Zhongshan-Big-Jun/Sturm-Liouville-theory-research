# -*- coding: utf-8 -*-
"""t3_c12_bound4.py: F'(b) sign and F(1/2) exact-ish."""
import sympy as sp
from mpmath import mp, mpf, sqrt, pi as mppi
mp.dps = 40
b = sp.symbols('b')
P = 2*b**6 + b**5 - 4*b**4 + 4*b**2 - b - 2
Q = 7*b**5 + 11*b**4 - 6*b**3 - 14*b**2 - b + 3
F = sp.Rational(2,3)*sp.pi*P + sp.Rational(1,3)*sp.sqrt(5)*Q + sp.Rational(21,10)*(1-b**2)**2*(1+b)**3
Fp = sp.diff(F, b)
print('Fp =', sp.expand(Fp))
print()
# numeric check of Fp sign on [1/2, 2/3]
Fp_f = sp.lambdify(b, Fp, 'mpmath')
lo, hi = mpf('1e30'), mpf('-1e30')
for i in range(2001):
    bv = mpf('0.5') + mpf(i)*mpf('1')/6000
    if bv > mpf('2')/3: break
    v = Fp_f(bv)
    lo = min(lo, v); hi = max(hi, v)
print('Fp on [1/2,2/3]: [%.4f, %.4f]' % (lo, hi))
# F(1/2) and F(2/3) exact
Fv = sp.lambdify(b, F, 'mpmath')
print('F(1/2) =', Fv(mpf('0.5')))
print('F(2/3) =', Fv(mpf('2')/3))
# where does Fp change sign? find roots
roots = sp.nroots(sp.expand(Fp), maxsteps=100)
print('roots of Fp:', roots)
