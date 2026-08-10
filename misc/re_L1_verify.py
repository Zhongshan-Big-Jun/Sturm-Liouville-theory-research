# -*- coding: utf-8 -*-
"""Verify Lemma u<=2 chain: u = x*r/(1+c*r), r = (-cot x)(cot th); constants."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, cot, sqrt
mp.dps = 50
gstar = mpf('0.65564932893873566325493245529469')
xmax = mppi - gstar
thmin = 2*mppi/7
print('xmax = %.8f' % xmax)
print('-cot(xmax) = cot(gamma*) = %.6f ; tan(gamma*) = %.6f' % (cot(gstar), tan(gstar)))
print('cot(2pi/7) = %.6f' % cot(thmin))
# constants
xmax_u = mpf('2.49')
cotg_u = mpf('1.31')
cot27 = mpf('0.8')
r_max = cotg_u*cot27
print('r_max = %.4f' % r_max)
u_bound = xmax_u*r_max/(1+mpf('0.4')*r_max)
print('u <= %.4f < 2' % u_bound)
# check: max u over T2
import numpy as np
# verify identity u = x*r/(1+c*r) at sample points
for (x, th) in [(2.1, 1.0), (2.3, 1.1), (2.4, 1.0)]:
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    c = th/x
    den = q + c*Phi
    u = x*Phi/den
    r = (-cot(x))*cot(th)
    u2 = x*r/(1+c*r)
    print('x=%.2f th=%.2f: u=%.6f xr/(1+cr)=%.6f r=%.5f' % (x, th, u, u2, r))
# tan(gamma*) lower bound via sin/cos: tan(t) >= (t - t^3/6)/(1 - t^2/2 + t^4/24)
t = mpf('0.655')
sinb = t - t**3/6
cosu = mpf(1) - t**2/2 + t**4/24
print('tan(0.655) >= %.6f ; 1/1.31 = %.6f' % (sinb/cosu, 1/mpf('1.31')))
print('need tan(gamma*) > 1/1.31 = %.6f: %.6f > %.6f ?' % (1/mpf('1.31'), sinb/cosu, 1/mpf('1.31')))
# cot(2pi/7) < 0.8: arctan(0.8) >= 0.8-0.8^3/3+0.8^5/5-0.8^7/7
z = mpf('0.8')
atlb = z - z**3/3 + z**5/5 - z**7/7
print('arctan(0.8) >= %.6f ; 3pi/14 = %.6f ; need 3pi/14 < arctan(0.8)' % (atlb, 3*mppi/14))
print('3pi/14 < atan(0.8):', 3*mppi/14 < atlb)
