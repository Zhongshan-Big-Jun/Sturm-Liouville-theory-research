# -*- coding: utf-8 -*-
"""t3_split_dbg.py"""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
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
    Phix = -2*s*b*(q*q-1)
    ux = (Phi + x*Phix)/den - x*Phi*c*Phix/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = (2*c*(q*q-1)*(b*b - s*s)*den - 2*c*(q*q-1)*s*(-b)*c*Phix)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return q, ux*V, u*Hx, -u*A0x, Gx, u, den
worst = None
N=400
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    for j in range(N+1):
        th = mpf('0.4')*x + mpf(j)*(mpf('0.5')-mpf('0.4'))*x
        if th < mppi - x: continue
        try:
            q, p1, p2, p3, Gx, u, den = comps(x, th)
        except Exception:
            continue
        if q < 1 or q > 2: continue
        if p3 < mpf('4.5'):
            worst = (float(x), float(th), float(q), float(p3), float(u), float(den))
            print('low p3: x=%.5f th=%.5f q=%.4f p3=%.5f u=%.5f den=%.5f' % worst)
            raise SystemExit
print('no low p3 found')
