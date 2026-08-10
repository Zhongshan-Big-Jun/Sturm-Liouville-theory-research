# -*- coding: utf-8 -*-
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
    return dict(q=q, c=c, u=u, ux=ux, V=V, Hx=Hx, A0x=A0x, p1=ux*V, p2=u*Hx, p3=-u*A0x, Gx=Gx, G=G, A0=A0)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
N = 150
R = {k: [mpf('1e30'), mpf('-1e30'), None, None] for k in ['V','ux','Hx','p1','p2','p3','Gx','G','A0']}
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
for k in ['A0','V','ux','Hx','p1','p2','p3','Gx','G']:
    print('%s: min=%.5f at %s ; max=%.5f at %s' % (k, R[k][0], R[k][2], R[k][1], R[k][3]))
