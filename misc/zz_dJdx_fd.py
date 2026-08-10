# -*- coding: utf-8 -*-
"""dJ/dx|th for the CORRECT J via finite differences of comps (fixed theta)."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 60

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
    return J

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
h = mpf('1e-7')
N = 150
mn = (mpf('1e30'), None); mx = (mpf('-1e30'), None)
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    tlo = max(2*x/5, mppi-x); thi = min(x/2, atan(-2*tan(x)))
    if tlo >= thi: continue
    for j in range(N+1):
        t = tlo + mpf(j)*(thi-tlo)/N
        if t <= tlo or t >= thi: continue
        v = (comps(x+h, t) - comps(x-h, t))/(2*h)
        if v < mn[0]: mn = (v, (float(x), float(t)))
        if v > mx[0]: mx = (v, (float(x), float(t)))
print('dJ/dx|th on T2 (correct J): min %.5f at %s ; max %.5f at %s' % (mn[0], mn[1], mx[0], mx[1]))
