# -*- coding: utf-8 -*-
"""Gx numerator (22 terms) and dGx/dx|th numerator."""
import sympy as sp
x, th = sp.symbols('x th', positive=True)
s, b, S, C = sp.symbols('s b S C', positive=True)
Delta = b*s*th + C*S*x
u = b*s*x**2/Delta
A0 = sp.Rational(3)/x - 2*b/s
H = 2*th*(C**2*s**2 - S**2*b**2)/Delta
V = H - A0

def Dx(f):
    return sp.expand(sp.diff(f, x) + sp.diff(f, s)*(-b) + sp.diff(f, b)*s)

ux = Dx(u); Hx = Dx(H); A0x = Dx(A0)
Gx = ux*V + u*(Hx - A0x)
num, den = sp.fraction(sp.cancel(Gx))
num = sp.expand(num)
print('Gx numerator (%d terms):' % len(sp.Add.make_args(num)))
print(sp.factor(num))
print()
# Now dGx/dx|th = Dx(Gx as rational function in x,s,b,S,C,th)
dGxdx = sp.cancel(Dx(sp.cancel(Gx)))
dnum, dden = sp.fraction(dGxdx)
dnum = sp.expand(dnum)
print('dGxdx numerator (%d terms):' % len(sp.Add.make_args(dnum)))
print('den:', sp.factor(dden))
