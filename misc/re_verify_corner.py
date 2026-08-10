# -*- coding: utf-8 -*-
"""Corner value + curve closed forms check."""
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
    Hx = 2*c*(q*q-1)*((s*s - b*b)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*(-b)*q/(den*den))
    return dict(q=q, s=s, b=b, S=S, C=C, Phi=Phi, c=c, u=u, A0=A0, H=H, V=V, G=G, Gx=Gx, Gc=Gc)

# corner (x,th)=(2pi/3, pi/3): q=1, c=1/2
x0, th0 = 2*mppi/3, mppi/3
r = comps(x0, th0)
print('corner: q=%.10f c=%.10f' % (r['q'], r['c']))
print('Gx corner = %.12f' % r['Gx'])
print('G corner  = %.12f' % r['G'])
print('Gc corner = %.12f' % r['Gc'])
print('u corner  = %.12f  (4pi/9=%.12f)' % (r['u'], 4*mppi/9))
J = r['G']**2 + r['Gc'] - r['u']*r['Gx']
print('J2 corner = %.12f' % J)

# q=1 curve closed form: Gx = (2x/pi)(x - sinx cosx)/sin^2 x
for x in [x0, mpf('2.1'), mpf('2.2'), mpf('2.24399')]:
    rr = comps(x, mppi-x)
    cf = (2*x/mppi)*(x - sin(x)*cos(x))/sin(x)**2
    print('q=1 x=%.5f: Gx=%.10f closed=%.10f' % (x, rr['Gx'], cf))

# c=1/2 curve closed form: Gx = -2[xP(b)+sQ(b)]/(s^4(1+b)^3)
def PQ(b):
    P = 2*b**6 + b**5 - 4*b**4 + 4*b**2 - b - 2
    Q = 7*b**5 + 11*b**4 - 6*b**3 - 14*b**2 - b + 3
    return P, Q
for b in [mpf('0.5'), mpf('0.55'), mpf('0.6'), mpf('0.65'), mpf('2')/3]:
    x = mppi - acos(b) if False else None
    import math
    xv = mppi - mp.acos(b)
    s = sqrt(1-b*b)
    rr = comps(xv, xv/2)
    P, Q = PQ(b)
    cf = -2*(xv*P + s*Q)/(s**4*(1+b)**3)
    print('c=1/2 b=%.4f: Gx=%.10f closed=%.10f' % (b, rr['Gx'], cf))
