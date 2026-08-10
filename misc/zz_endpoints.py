# -*- coding: utf-8 -*-
"""Exact rational enclosures for sin/cos at gamma0=0.655, gamma1=1.0472 via alternating series."""
from fractions import Fraction as F

def sin_cos(x, n=60):
    # x = Fraction; alternating series for sin, cos with error bound
    x2 = x*x
    # sin: sum_{k=0}^{K} (-1)^k x^{2k+1}/(2k+1)!
    sin_lo = F(0); sin_hi = F(0)
    term = x; k = 0; sgn = 1
    lo = F(0); hi = F(0)
    for k in range(0, n):
        term = x ** (2*k+1) / F(__import__('math').factorial(2*k+1))
        if k % 2 == 0: lo += term
        else: hi -= term
    # partial sums alternate; error bounded by next term
    nextterm = x ** (2*n+1) / F(__import__('math').factorial(2*n+1))
    return lo, hi, nextterm

x0 = F(131, 200)  # 0.655
x1 = F(1309, 1250)  # 1.0472
for name, x in [('0.655', x0), ('1.0472', x1)]:
    s_lo = F(0); s_hi = F(0); c_lo = F(0); c_hi = F(0)
    x2 = x*x
    for k in range(0, 40):
        t_sin = x**(2*k+1)/F(__import__('math').factorial(2*k+1))
        t_cos = x**(2*k)/F(__import__('math').factorial(2*k))
        if k % 2 == 0: s_lo += t_sin; c_lo += t_cos
        else: s_hi += t_sin; c_hi += t_cos
    # error bounds (next term)
    e_s = x**(81)/F(__import__('math').factorial(81)); e_c = x**(80)/F(__import__('math').factorial(80))
    print('%s: sin in [%.12f, %.12f] (err %.2e), cos in [%.12f, %.12f] (err %.2e)' % (name, s_lo-e_s, s_hi+e_s, e_s, c_lo-e_c, c_hi+e_c, e_c))
    # also pi bounds
import mpmath as mp
mp.mp.dps = 50
print('pi = %.20f' % mp.pi)
