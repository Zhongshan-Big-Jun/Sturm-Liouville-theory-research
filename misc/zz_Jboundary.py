# -*- coding: utf-8 -*-
"""J along boundary curves of T2 (q=1, c=1/2, c=2/5) properly, and dJ/dx|th margin."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 50

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
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    J = G*G + Gc - u*Gx
    return J, q, G, Gc, u, Gx

gstar = mpf('0.65564932893873566325493245529469')
xmax = mppi - gstar
print('c=1/2 curve, x in [2pi/3, xB]:  (xB solves b=2/3 => cos x = -2/3)')
xB = mppi - mp.acos(mpf(2)/3)
print('  xB = %.6f' % xB)
N = 400
lo = (mpf('1e30'), None)
for i in range(N+1):
    x = 2*mppi/3 + mpf(i)*(xB-2*mppi/3)/N
    J, q, G, Gc, u, Gx = comps(x, x/2)
    if J < lo[0]: lo = (J, (float(x), float(q)))
print('  J min %.6f at %s' % (lo[0], lo[1]))
print('  J endpoints: x=2pi/3: %.6f ; x=xB: %.6f' % (comps(2*mppi/3, mppi/3)[0], comps(xB, xB/2)[0]))
print()
print('c=2/5 curve, x in [5pi/7, xmax]:')
lo = (mpf('1e30'), None)
for i in range(N+1):
    x = 5*mppi/7 + mpf(i)*(xmax-5*mppi/7)/N
    J, q, G, Gc, u, Gx = comps(x, 2*x/5)
    if J < lo[0]: lo = (J, (float(x), float(q)))
print('  J min %.6f at %s' % (lo[0], lo[1]))
print('  J endpoints: x=5pi/7: %.6f ; x=xmax: %.6f' % (comps(5*mppi/7, 2*mppi/7)[0], comps(xmax, 2*xmax/5)[0]))
print()
print('q=2 curve, x in [xB, xmax]:')
lo = (mpf('1e30'), None)
for i in range(N+1):
    x = xB + mpf(i)*(xmax-xB)/N
    th = atan(-2*tan(x))
    J, q, G, Gc, u, Gx = comps(x, th)
    if J < lo[0]: lo = (J, (float(x), float(q)))
print('  J min %.6f at %s' % (lo[0], lo[1]))
