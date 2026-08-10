# -*- coding: utf-8 -*-
"""Check dJ2/dq at fixed gamma and dJ2/dgamma at fixed q over T2."""
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
    J = G*G + Gc - u*Gx
    return dict(q=q, G=G, Gx=Gx, Gc=Gc, J=J)

def at_gq(g, q):
    x = mppi - g
    th = atan(q*tan(g))
    return comps(x, th)

h = mpf('1e-6')
gstar = mpf('0.65564932893873566325493245529469')
N = 60
dJq_min = mpf('1e30'); dJq_max = mpf('-1e30'); dJg_min = mpf('1e30'); dJg_max = mpf('-1e30')
loc = {}
cnt = 0
for i in range(N+1):
    g = gstar + mpf(i)*(mppi/3 - gstar)/N
    for j in range(N+1):
        q = mpf(1) + mpf(j)/N
        x, th = mppi-g, atan(q*tan(g))
        c = th/x
        if not (mpf('0.4') < c < mpf('0.5')): continue
        cnt += 1
        Jp = at_gq(g, q+h)['J']; Jm = at_gq(g, q-h)['J']
        Jgp = at_gq(g+h, q)['J']; Jgm = at_gq(g-h, q)['J']
        dJq = (Jp-Jm)/(2*h); dJg = (Jgp-Jgm)/(2*h)
        if dJq < dJq_min: dJq_min, loc['qmin'] = dJq, (float(g), float(q))
        if dJq > dJq_max: dJq_max, loc['qmax'] = dJq, (float(g), float(q))
        if dJg < dJg_min: dJg_min, loc['gmin'] = dJg, (float(g), float(q))
        if dJg > dJg_max: dJg_max, loc['gmax'] = dJg, (float(g), float(q))
print('samples:', cnt)
print('dJ/dq|g in [%.4f, %.4f], min at %s, max at %s' % (dJq_min, dJq_max, loc['qmin'], loc['qmax']))
print('dJ/dg|q in [%.4f, %.4f], min at %s, max at %s' % (dJg_min, dJg_max, loc['gmin'], loc['gmax']))
