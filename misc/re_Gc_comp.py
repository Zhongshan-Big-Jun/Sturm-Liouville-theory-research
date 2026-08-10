# -*- coding: utf-8 -*-
"""Gc = g1 + g2 components over T2; find clean bounds."""
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
    g1 = -x*Phi*Phi*V/(den*den)
    g2 = u*(-2*(q*q-1)*s*b*q/(den*den))
    return dict(q=q, c=c, u=u, V=V, Phi=Phi, den=den, g1=g1, g2=g2, Gc=g1+g2)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
N = 120
R = {k: [mpf('1e30'), mpf('-1e30'), None, None] for k in ['g1','g2','Gc','V','Phi']}
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(-1, N+2):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N if (0 <= j <= N) else (th_lo if j<0 else th_hi)
        if th < th_lo or th > th_hi: continue
        r = comps(x, th)
        for k in R:
            v = r[k]
            if v < R[k][0]: R[k][0], R[k][2] = v, (float(x), float(th), float(r['q']))
            if v > R[k][1]: R[k][1], R[k][3] = v, (float(x), float(th), float(r['q']))
for k in ['g1','g2','Gc','V','Phi']:
    print('%s: min=%.5f at %s ; max=%.5f at %s' % (k, R[k][0], R[k][2], R[k][1], R[k][3]))
