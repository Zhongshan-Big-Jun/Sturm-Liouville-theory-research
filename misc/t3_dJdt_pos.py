# -*- coding: utf-8 -*-
"""t3_dJdt_pos.py: locate positive region of dJ/dth on T2."""
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar

def comps_xth(x, th):
    c = th/x
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    den = q + c*Phi
    u = x*Phi/den
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    G = u*V
    du = -x*Phi*Phi/(den*den)
    dH = 2*q*(q*q-1)*s*(-b)/(den*den)
    Gc = du*V + u*dH
    Phix = -2*s*b*(q*q-1)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = (2*c*(q*q-1)*(b*b - s*s)*den - 2*c*(q*q-1)*s*(-b)*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return G*G + Gc - u*Gx, q

h = mpf('1e-7')
pos = []
N=500
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_min = max(mpf('0.4')*x, mppi - x)
    th_max = min(mpf('0.5')*x, atan(-2*tan(x)))
    if th_max <= th_min: continue
    for j in range(N+1):
        th = th_min + mpf(j)*(th_max-th_min)/N
        J0,q0 = comps_xth(x,th)
        if q0 < 1 or q0 > 2: continue
        J1,_ = comps_xth(x,th+h)
        d = (J1-J0)/h
        if d > 0:
            pos.append((float(x),float(th),float(d),float(q0)))
print('positive dJ/dth count:', len(pos), 'of', (N+1)**2)
if pos:
    print('examples (x, th, dJ/dth, q):')
    for r in pos[:12]: print('  x=%.4f th=%.4f d=%.4f q=%.3f' % r)
    xs = [r[0] for r in pos]; ths=[r[1] for r in pos]
    print('x range of positive region: [%.4f, %.4f]' % (min(xs), max(xs)))
    print('th range: [%.4f, %.4f]' % (min(ths), max(ths)))
    qs=[r[3] for r in pos]
    print('q range: [%.3f, %.3f]' % (min(qs), max(qs)))
