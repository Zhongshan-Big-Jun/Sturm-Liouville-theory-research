# -*- coding: utf-8 -*-
"""Independent check of dGc/dq at fixed gamma via two methods."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt
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
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*(-b)*q/(den*den))
    return dict(q=q, G=G, Gx=Gx, Gc=Gc)

def at_gq(g, q):
    x = mppi - g
    th = atan(q*tan(g))
    return comps(x, th)

h = mpf('1e-6')
for (g, q0) in [(mpf('0.9'), mpf('1.0')), (mpf('0.9'), mpf('1.5')), (mpf('0.75'), mpf('1.5')), (mpf('0.7'), mpf('1.2'))]:
    Gc_p = at_gq(g, q0+h)['Gc']; Gc_m = at_gq(g, q0-h)['Gc']
    fd = (Gc_p - Gc_m)/(2*h)
    r = at_gq(g, q0)
    print('(g=%.3f, q=%.3f): Gc=%.8f, dGc/dq|g(fd)=%.6f' % (g, q0, r['Gc'], fd))
    # also Gc at q0+h/2 to see the trend
    print('    Gc(q+h/2)=%.8f Gc(q-h/2)=%.8f' % (at_gq(g, q0+h/2)['Gc'], at_gq(g, q0-h/2)['Gc']))
