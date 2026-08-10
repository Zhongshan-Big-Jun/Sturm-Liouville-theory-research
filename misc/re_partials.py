# -*- coding: utf-8 -*-
"""Partial derivative signs of u, V, ux, Hx, A0x, G, Gc, Gx w.r.t. x and theta on T2."""
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
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*(-b)*q/(den*den))
    return dict(q=q, c=c, u=u, ux=ux, V=V, Hx=Hx, A0x=A0x, G=G, Gx=Gx, Gc=Gc, H=H, A0=A0)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
h = mpf('1e-6')
N = 60
fields = ['u','V','ux','Hx','G','Gx','Gc']
res = {f: {'dx': [mpf('1e30'), mpf('-1e30')], 'dt': [mpf('1e30'), mpf('-1e30')]} for f in fields}
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(N+1):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th <= th_lo or th >= th_hi: continue
        r0 = comps(x, th)
        rx = comps(x+h, th); rm = comps(x-h, th)
        rt = comps(x, th+h); rtm = comps(x, th-h)
        for f in fields:
            dx = (rx[f]-rm[f])/(2*h); dt = (rt[f]-rtm[f])/(2*h)
            if dx < res[f]['dx'][0]: res[f]['dx'][0] = dx
            if dx > res[f]['dx'][1]: res[f]['dx'][1] = dx
            if dt < res[f]['dt'][0]: res[f]['dt'][0] = dt
            if dt > res[f]['dt'][1]: res[f]['dt'][1] = dt
for f in fields:
    print('%s: du/dx in [%.4f, %.4f], d/dt in [%.4f, %.4f]' % (f, res[f]['dx'][0], res[f]['dx'][1], res[f]['dt'][0], res[f]['dt'][1]))
