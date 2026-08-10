# -*- coding: utf-8 -*-
"""c=2/5 curve: Gx closed form via (s,b,x) reduction (like t3_Gx_c12d)."""
import sympy as sp
x = sp.symbols('x', positive=True)
s, b = sp.sin(x), -sp.cos(x)
th = sp.Rational(2,5)*x
S, C = sp.sin(th), sp.cos(th)
q = S*b/(C*s)
Phi = b*b/(C*C)
c = sp.Rational(2,5)
den = q + c*Phi
u = x*Phi/den
A0 = sp.Rational(3)/x - 2*b/s
H = 2*c*(q*q-1)*s*(-b)/den
V = H - A0
Phix = 2*s*b*(1-q*q)
ux = (Phi + x*Phix)/den - x*Phi*c*Phix/(den*den)
A0x = -3/(x*x) - 2/(s*s)
Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*c*Phix)/(den*den)
Gx = sp.cancel(ux*V + u*(Hx - A0x))
# reduce: multiply by s^4 (1+b)^3 style? just cancel first
e = sp.cancel(Gx)
num, den = sp.fraction(e)
num = sp.expand(num)
den = sp.factor(den)
print('den:', den)
print('num terms:', len(sp.Add.make_args(num)))
print(sp.factor(num))
