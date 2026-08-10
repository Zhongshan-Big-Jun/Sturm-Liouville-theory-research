# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'misc')
from fractions import Fraction as F
from rigid1d import I, D2, d2_sin, d2_cos, d2_atan, PI, der_sign2
import mpmath as mp
mp.mp.dps = 30
# sanity: f = gamma^2 sin(gamma) second derivative at point
g = D2(I(F(7,10), F(7,10)), I(1), I(0))
f = g*g*d2_sin(g)
print('f = g^2 sin g at 0.7: v,d1,d2 =', float(f.v.lo), float(f.d1.lo), float(f.d2.lo))
# true: f=g^2 sin g, f'=2g sin g + g^2 cos g, f''=2 sin g + 4g cos g - g^2 sin g
gg = mp.mpf('0.7')
print('true:', float(gg**2*mp.sin(gg)), float(2*gg*mp.sin(gg)+gg**2*mp.cos(gg)), float(2*mp.sin(gg)+4*gg*mp.cos(gg)-gg**2*mp.sin(gg)))
# test der_sign2 on a simple function: f = -gamma, derivative < 0 on [0,1]
r, n = der_sign2(lambda x: -x, F(0), F(1), False)
print('der_sign2(-x, want<0):', r, n)
