# -*- coding: utf-8 -*-
"""Monotonicity of H1=G^2+Gc and uGx over T2."""
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
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    return dict(q=q, G=G, Gx=Gx, Gc=Gc, u=u, H1=G*G+Gc, uGx=u*Gx)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
h = mpf('1e-6')
N = 50
rng = {'dH1dx':[1e30,-1e30],'dH1dt':[1e30,-1e30],'duGxdx':[1e30,-1e30],'duGxdt':[1e30,-1e30]}
loc = {k:[None,None] for k in rng}
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(N+1):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th <= th_lo or th >= th_hi: continue
        r0 = comps(x, th)
        dH1dx = (comps(x+h,th)['H1']-comps(x-h,th)['H1'])/(2*h)
        dH1dt = (comps(x,th+h)['H1']-comps(x,th-h)['H1'])/(2*h)
        duGxdx = (comps(x+h,th)['uGx']-comps(x-h,th)['uGx'])/(2*h)
        duGxdt = (comps(x,th+h)['uGx']-comps(x,th-h)['uGx'])/(2*h)
        for k, v in [('dH1dx',dH1dx),('dH1dt',dH1dt),('duGxdx',duGxdx),('duGxdt',duGxdt)]:
            if v < rng[k][0]: rng[k][0], loc[k][0] = v, (float(x),float(th))
            if v > rng[k][1]: rng[k][1], loc[k][1] = v, (float(x),float(th))
for k in rng:
    print('%s in [%.4f, %.4f] min@%s max@%s' % (k, rng[k][0], rng[k][1], loc[k][0], loc[k][1]))
