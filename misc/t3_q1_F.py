# -*- coding: utf-8 -*-
"""t3_q1_F: analyze F(gamma) on [2pi/7, pi/3]."""
import math
from mpmath import mp, mpf, cos, sin, pi as mppi
mp.dps = 40

def F(g):
    s = sin(g); c = cos(g)
    return (2*c**2*g**2 - 4*mppi*c**2*g + 2*mppi**2*c**2 + 8*c*s*g - 8*mppi*c*s - g**2 + 2*mppi*g + 6*s**2 - mppi**2)

glo, ghi = mpf(2)*mppi/7, mppi/3
lo, hi, arglo, arghi = mpf(1e30), mpf(-1e30), None, None
for i in range(4001):
    g = glo + mpf(i)*(ghi-glo)/4000
    v = F(g)
    if v < lo: lo = v; arglo = (g, i)
    if v > hi: hi = v; arghi = (g, i)
print("F on [2pi/7, pi/3]: min %.6f at g=%.6f ; max %.6f at g=%.6f" % (lo, arglo[0], hi, arghi[0]))
def dF(g, h=mpf('1e-6')):
    return (F(g+h)-F(g-h))/(2*h)
loD, hiD = mpf(1e30), mpf(-1e30)
for i in range(1001):
    g = glo + mpf(i)*(ghi-glo)/1000
    v = dF(g)
    loD = min(loD, v); hiD = max(hiD, v)
print("dF in [%.4f, %.4f]" % (loD, hiD))
def d2F(g, h=mpf('1e-4')):
    return (F(g+h)-2*F(g)+F(g-h))/(h*h)
lo2, hi2 = mpf(1e30), mpf(-1e30)
for i in range(1001):
    g = glo + mpf(i)*(ghi-glo)/1000
    v = d2F(g)
    lo2 = min(lo2, v); hi2 = max(hi2, v)
print("d2F in [%.4f, %.4f]" % (lo2, hi2))
print("F at endpoints: F(2pi/7) =", F(glo), " F(pi/3) =", F(ghi))
