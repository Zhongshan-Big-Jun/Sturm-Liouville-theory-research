# -*- coding: utf-8 -*-
from mpmath import mp, mpf, cos, sin, tan, pi as mppi, sqrt, acos
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

M_str = "(b**7*s**2*x - 2*b**6*x + 2*b**5*s**4*x + b**5*s**3 - b**5*s**2*x + 3*b**5*s - 2*b**5*x - 2*b**4*s**4*x - 3*b**4*s**3 - 2*b**4*s**2*x + 5*b**4*s + 2*b**4*x + b**3*s**6*x + b**3*s**5 + 2*b**3*s**4*x - 3*b**3*s**3 - 3*b**3*s + 4*b**3*x - 2*b**2*s**6*x - 3*b**2*s**5 + 2*b**2*s**4*x - 3*b**2*s**3 - 2*b**2*s**2*x - 5*b**2*s + 3*b*s**6*x + 2*b*s**5 - 3*b*s**3 - 2*b*s**2*x - 2*b*x - 2*s**6*x + 3*s**3)"
s = mpf('0.835'); b = mpf('0.55'); x = mpf('2.153160564663640061063368982549727810078')
M31 = eval(M_str)
P = 2*b**6 + b**5 - 4*b**4 + 4*b**2 - b - 2
Q = 7*b**5 + 11*b**4 - 6*b**3 - 14*b**2 - b + 3
print('M31      =', M31)
print('xP + sQ  =', x*P + s*Q)
print('ratio    =', M31/(x*P + s*Q))
xv = mppi - acos(b)
print('comps    =', comps(xv, xv/2))
print('closed from M31 =', -2*M31/(s**4*(1+b)**3))
print('M31 at true s:')
s2 = sqrt(1-b*b)
print(' s =', s2)
print(' M31 =', eval(M_str))
print(' xP+sQ =', x*P + s2*Q)
