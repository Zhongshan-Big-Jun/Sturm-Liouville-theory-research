# -*- coding: utf-8 -*-
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')
x = mppi - gstar
th = 2*x/5
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
print('x=%.10f th=%.10f q=%.10f c=%.10f' % (x, th, q, c))
print('s=%.8f b=%.8f S=%.8f C=%.8f' % (s, b, S, C))
print('Phi=%.8f den=%.8f u=%.8f' % (Phi, den, u))
print('A0=%.8f H=%.8f V=%.8f' % (A0, H, V))
print('u*V = G = %.8f' % (u*V))
