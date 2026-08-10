# -*- coding: utf-8 -*-
"""t3_verify_cross.py: verify comps_xth vs t3_J2_components Gx."""
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')

def comps_xth(x, th):
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
    G = u*V
    Phix = -2*s*b*(q*q-1)
    ux = (Phi + x*Phix)/den - x*Phi*c*Phix/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = (2*c*(q*q-1)*(b*b - s*s)*den - 2*c*(q*q-1)*s*(-b)*c*Phix)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return q, Gx

def comps_gq(g, q):
    A = mppi-g; t = atan(q*tan(g)); c = t/A
    sx, cx = sin(g), -cos(g)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    u = A*Phi/den
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    V = H - A0
    G = u*V
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/(sx*sx)
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return Gx

for (g,q) in [(0.7,1.5),(0.9,1.2),(1.0,1.1),(mppi/3,1.0),(gstar,2.0),(0.85,1.8)]:
    x = mppi - g
    th = atan(q*tan(g))
    qx, Gx1 = comps_xth(x, th)
    Gx2 = comps_gq(g, q)
    print('g=%.4f q=%.2f: qx=%.5f Gx_xth=%.8f Gx_gq=%.8f diff=%.2e' % (g,q,qx,Gx1,Gx2,abs(Gx1-Gx2)))
