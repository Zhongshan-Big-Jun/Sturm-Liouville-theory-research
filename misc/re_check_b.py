# -*- coding: utf-8 -*-
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt, acos
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
    Hx = 2*c*(q*q-1)*((s*s - b*b)*den - s*(-b)*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return Gx

def PQ(b):
    P = 2*b**6 + b**5 - 4*b**4 + 4*b**2 - b - 2
    Q = 7*b**5 + 11*b**4 - 6*b**3 - 14*b**2 - b + 3
    return P, Q

b = mpf('0.55')
xv = mppi - acos(b)
print('xv =', xv)
s = sqrt(1-b*b)
P, Q = PQ(b)
print('P,Q =', P, Q)
print('xP+sQ =', xv*P + s*Q)
cf = -2*(xv*P + s*Q)/(s**4*(1+b)**3)
print('closed =', cf)
print('numeric =', comps(xv, xv/2))
