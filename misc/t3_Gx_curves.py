# -*- coding: utf-8 -*-
"""t3_Gx_curves.py: Gx on q=1 and c=1/2 curves, monotonicity along curves."""
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar

def comps_xth(x, th):
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    c = th/x
    den = q + c*Phi
    u = x*Phi/den
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    Phix = -2*s*b*(q*q-1)
    ux = (Phi + x*Phix)/den - x*Phi*c*Phix/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = (2*c*(q*q-1)*(b*b - s*s)*den - 2*c*(q*q-1)*s*(-b)*c*Phix)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return q, Gx

h = mpf('1e-6')
# q=1 curve: th = pi - x, x in [2pi/3, pi/1.4]
print('q=1 curve:')
lo1 = (mpf('1e30'), None); fmin1 = (mpf('1e30'), None)
for i in range(400):
    x = xmin + mpf(i)*((mppi/mpf('1.4'))-xmin)/400
    th = mppi - x
    q, Gx = comps_xth(x, th)
    q2, Gx2 = comps_xth(x+h, th-h)  # along curve derivative (dx, -dx)
    d = (Gx2 - Gx)/(2*h)
    if Gx < lo1[0]: lo1 = (Gx, float(x))
    if d < fmin1[0]: fmin1 = (d, float(x))
print('  min Gx: %.6f at x=%.4f ; min derivative along curve: %.4f at x=%.4f' % (lo1[0], lo1[1], fmin1[0], fmin1[1]))
# closed form check: Gx = (2x/pi)(x - sinx cosx)/sin^2 x
for x in [xmin, mpf('2.1'), mpf('2.2'), mpf('2.24')]:
    q, Gx = comps_xth(x, mppi-x)
    cf = (2*x/mppi)*(x - sin(x)*cos(x))/sin(x)**2
    print('  x=%.4f: Gx=%.8f closed=%.8f' % (x, Gx, cf))

# c=1/2 curve: th = x/2, x in [2pi/3, x*]
print('c=1/2 curve:')
lo2 = (mpf('1e30'), None); fmin2 = (mpf('1e30'), None)
for i in range(400):
    x = xmin + mpf(i)*(xmax-xmin)/400
    th = x/2
    q, Gx = comps_xth(x, th)
    q2, Gx2 = comps_xth(x+h, (x+h)/2)
    d = (Gx2 - Gx)/h
    if Gx < lo2[0]: lo2 = (Gx, float(x))
    if d < fmin2[0]: fmin2 = (d, float(x))
print('  min Gx: %.6f at x=%.4f ; min derivative along curve: %.4f at x=%.4f' % (lo2[0], lo2[1], fmin2[0], fmin2[1]))
# dGx/dx and dGx/dth at the corner
x0, th0 = xmin, mppi/3
q0, Gx0 = comps_xth(x0, th0)
Gx1 = comps_xth(x0+h, th0)[1]; Gx2 = comps_xth(x0, th0+h)[1]
print('at corner: dGx/dx = %.4f, dGx/dth = %.4f' % ((Gx1-Gx0)/h, (Gx2-Gx0)/h))
