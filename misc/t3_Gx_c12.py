# -*- coding: utf-8 -*-
"""t3_Gx_c12.py: closed form of Gx on c=1/2 curve + derivative sign."""
import sympy as sp
x = sp.symbols('x', positive=True)
s, b = sp.sin(x), -sp.cos(x)
th = x/2
S, C = sp.sin(th), sp.cos(th)
q = S*b/(C*s)
Phi = b*b/(C*C)
c = sp.Rational(1,2)
den = q + c*Phi
u = x*Phi/den
A0 = sp.Rational(3)/x - 2*b/s
H = 2*c*(q*q-1)*s*(-b)/den
V = H - A0
Phix = -2*s*b*(q*q-1)
ux = (Phi + x*Phix)/den - x*Phi*c*Phix/(den*den)
A0x = -3/(x*x) - 2/(s*s)
Hx = (2*c*(q*q-1)*(b*b - s*s)*den - 2*c*(q*q-1)*s*(-b)*c*Phix)/(den*den)
Gx = ux*V + u*(Hx - A0x)
e = sp.trigsimp(sp.expand(Gx))
print('Gx(x, x/2) =')
print(sp.factor(e))
print()
d = sp.diff(Gx, x)
d2 = sp.trigsimp(sp.expand(d))
print('d/dx Gx(x,x/2) =')
print(sp.factor(d2))
