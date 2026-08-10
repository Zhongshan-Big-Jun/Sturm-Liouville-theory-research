# -*- coding: utf-8 -*-
"""c=2/5 curve: Gx values, monotonicity along curve, Gx-21/5 sign."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt
mp.dps = 40

def comps(x, th):
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
    Phix = 2*s*b*(1-q*q)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return Gx

gstar = mpf('0.65564932893873566325493245529469')
xmax = mppi - gstar
x0 = 5*mppi/7
N = 400
mn = (mpf('1e30'), None); mx = (mpf('-1e30'), None); mn21 = (mpf('1e30'), None)
dmin = (mpf('1e30'), None)
h = mpf('1e-7')
for i in range(N+1):
    x = x0 + mpf(i)*(xmax-x0)/N
    th = 2*x/5
    G = comps(x, th)
    if G < mn[0]: mn = (G, float(x))
    if G > mx[0]: mx = (G, float(x))
    if G - mpf('4.2') < mn21[0]: mn21 = (G-4.2, float(x))
    if i < N:
        d = (comps(x+h, 2*(x+h)/5) - comps(x, 2*x/5))/h
        if d < dmin[0]: dmin = (d, float(x))
print('c=2/5 curve x in [5pi/7, xmax]:')
print('  Gx min=%.6f at x=%.5f ; max=%.6f' % (mn[0], mn[1], mx[0]))
print('  Gx-21/5 min=%.6f at x=%.5f' % (mn21[0], mn21[1]))
print('  min derivative along curve=%.4f at x=%.5f' % (dmin[0], dmin[1]))
# endpoints
print('  Gx(5pi/7)=%.6f  Gx(xmax)=%.6f' % (comps(x0, 2*x0/5), comps(xmax, 2*xmax/5)))
