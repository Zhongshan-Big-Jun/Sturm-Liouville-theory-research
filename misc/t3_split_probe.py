# -*- coding: utf-8 -*-
"""t3_split_probe.py: joint ranges of p1+p2 and p3 on x-slices of T2."""
import math
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
    p1 = ux*V; p2 = u*Hx; p3 = -u*A0x
    return q, p1, p2, p3, Gx

for xcut in [mpf('2.20'), mpf('2.25'), mpf('2.28'), mpf('2.30')]:
    res = {}
    N=400
    for i in range(N+1):
        x = xmin + mpf(i)*(xmax-xmin)/N
        for j in range(N+1):
            th = mpf('0.4')*x + mpf(j)*(mpf('0.5')-mpf('0.4'))*x
            if th < mppi - x: continue
            q, p1, p2, p3, Gx = comps(x, th)
            if q < 1 or q > 2: continue
            region = 'S1' if x <= xcut else 'S2'
            for k, v in [('p1p2', p1+p2), ('p3', p3), ('Gx', Gx)]:
                key = (region, k)
                if key not in res: res[key] = [mpf(1e30), mpf(-1e30)]
                res[key][0] = min(res[key][0], v); res[key][1] = max(res[key][1], v)
    print('xcut=%.2f:' % xcut)
    for r in ['S1','S2']:
        print('  %s: p1+p2 in [%.4f, %.4f]; p3 in [%.4f, %.4f]; Gx in [%.4f, %.4f]' % (
            r, res[(r,'p1p2')][0], res[(r,'p1p2')][1], res[(r,'p3')][0], res[(r,'p3')][1], res[(r,'Gx')][0], res[(r,'Gx')][1]))
