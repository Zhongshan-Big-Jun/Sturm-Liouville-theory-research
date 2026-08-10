# -*- coding: utf-8 -*-
"""Cross-check Gc formula vs finite differences at several points."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt
mp.dps = 50

def G_of_xc(x, q, c):
    # G(x;c) with q fixed (doc convention)
    s, b = sin(x), -cos(x)
    Phi = q*q*s*s + b*b
    D = q + c*Phi
    u = x*Phi/D
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*b/D
    return u*(H - A0)

def Gc_formula(x, q, c):
    s, b = sin(x), -cos(x)
    Phi = q*q*s*s + b*b
    D = q + c*Phi
    u = x*Phi/D
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*b/D
    V = H - A0
    g1 = -x*Phi*Phi*V/(D*D)
    g2 = u*(-2*(q*q-1)*s*b*q/(D*D))
    return g1 + g2, g1, g2

# point N: (x,q) = (2.300523983021864, 2), c = 1/2
for (x, q, c) in [(mpf('2.300523983021864'), mpf(2), mpf('0.5')),
                  (mpf('2.0943951023931957'), mpf(1), mpf('0.5')),
                  (mpf('2.2'), mpf('1.5'), mpf('0.45'))]:
    h = mpf('1e-6')
    fd = (G_of_xc(x, q, c+h) - G_of_xc(x, q, c-h))/(2*h)
    gf, g1, g2 = Gc_formula(x, q, c)
    print('(x=%.4f, q=%.3f, c=%.3f): Gc_fd=%.6f Gc_formula=%.6f (g1=%.6f, g2=%.6f)' % (x, q, c, fd, gf, g1, g2))
    # also verify H sign: H = 2c(q^2-1) s b / D with b=-cos x
    s, b = sin(x), -cos(x)
    print('   s=%.5f b=%.5f (b=-cos x): H sign uses b>0' % (s, b))
