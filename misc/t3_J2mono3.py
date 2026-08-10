# -*- coding: utf-8 -*-
"""t3_J2mono3.py: J2_2d monotonicity in (x,th)."""
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar

def comps_xth(x, th):
    c = th/x
    t = th
    q = -tan(t)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(t), cos(t)
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

h = mpf('1e-6')
random.seed(17)
rows=[]
for _ in range(600):
    x = xmin + mpf(random.random())*(xmax-xmin)
    th_min = max(mpf('0.4')*x, mppi - x)
    th_max = min(mpf('0.5')*x, atan(-2*tan(x)))
    if th_max <= th_min: continue
    th = th_min + mpf(random.random())*(th_max-th_min)
    J0,q0 = comps_xth(x,th)
    if q0 < 1 or q0 > 2: continue
    J1,_ = comps_xth(x+h,th); J2,_ = comps_xth(x,th+h)
    rows.append((float(x),float(th),float((J1-J0)/h),float((J2-J0)/h)))
for k, idx in [('dJ/dx|th',2),('dJ/dth|x',3)]:
    v = [r[idx] for r in rows]
    print('%s: [%.3f, %.3f]' % (k, min(v), max(v)))
