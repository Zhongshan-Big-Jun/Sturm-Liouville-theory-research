# -*- coding: utf-8 -*-
"""t3_J2mono4.py: monotonicity of J2 on larger regions."""
import math, random
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
    return G*G + Gc - u*Gx, q, c

h = mpf('1e-6')
random.seed(23)
def scan(name, ok):
    rows=[]
    for _ in range(900):
        x = xmin + mpf(random.random())*(xmax-xmin)
        th = mpf('0.4')*x + mpf(random.random())*(mpf('0.5')-mpf('0.4'))*x
        if not ok(x,th): continue
        J0,q0,c0 = comps_xth(x,th)
        J1,_,_ = comps_xth(x+h,th); J2,_,_ = comps_xth(x,th+h)
        rows.append((float((J1-J0)/h), float((J2-J0)/h)))
    if not rows: print(name, 'no samples'); return
    d1=[r[0] for r in rows]; d2=[r[1] for r in rows]
    print('%s: dJ/dx [%.3f, %.3f], dJ/dth [%.3f, %.3f]' % (name, min(d1), max(d1), min(d2), max(d2)))

scan('R1: c in [0.4,0.5], q>=1', lambda x,th: th>=mppi-x)
scan('R2: c in [0.4,0.5], q>=0.9', lambda x,th: -tan(th)/tan(x)>=mpf('0.9'))
scan('R3: c in [0.3,0.5], q>=1', lambda x,th: th>=mppi-x and th/x>=mpf('0.3'))
scan('R4: c in [0.4,0.6], q>=1', lambda x,th: th>=mppi-x and th/x<=mpf('0.6'))
