# -*- coding: utf-8 -*-
"""dH1/dx, dH1/dth over T2; also find max H1 location; check H1 vs Gc interplay."""
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
    return dict(q=q, c=c, G=G, Gx=Gx, Gc=Gc, H1=G*G+Gc)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
h = mpf('1e-6')
N = 50
rng = {'dH1dx': [mpf('1e30'), mpf('-1e30')], 'dH1dt': [mpf('1e30'), mpf('-1e30')], 'dGcdx': [mpf('1e30'), mpf('-1e30')]}
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(N+1):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th <= th_lo or th >= th_hi: continue
        r0 = comps(x, th); rp = comps(x+h, th); rm = comps(x-h, th)
        rt = comps(x, th+h); rtm = comps(x, th-h)
        dH1dx = (rp['H1']-rm['H1'])/(2*h); dH1dt = (rt['H1']-rtm['H1'])/(2*h)
        dGcdx = (rp['Gc']-rm['Gc'])/(2*h)
        if dH1dx < rng['dH1dx'][0]: rng['dH1dx'][0] = dH1dx
        if dH1dx > rng['dH1dx'][1]: rng['dH1dx'][1] = dH1dx
        if dH1dt < rng['dH1dt'][0]: rng['dH1dt'][0] = dH1dt
        if dH1dt > rng['dH1dt'][1]: rng['dH1dt'][1] = dH1dt
        if dGcdx < rng['dGcdx'][0]: rng['dGcdx'][0] = dGcdx
        if dGcdx > rng['dGcdx'][1]: rng['dGcdx'][1] = dGcdx
for k in rng:
    print('%s in [%.4f, %.4f]' % (k, rng[k][0], rng[k][1]))
