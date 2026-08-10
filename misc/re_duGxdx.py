# -*- coding: utf-8 -*-
"""d(uGx)/dx numerator structure."""
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
Gx = sp.cancel(ux*V + u*(Hx - A0x))
uGx = sp.cancel(u*Gx)
duGxdx = sp.cancel(Dx(uGx))
num, den = sp.fraction(duGxdx)
num = sp.expand(num)
print('d(uGx)/dx numerator terms:', len(sp.Add.make_args(num)))
print('den:', sp.factor(den))
print()
print(sp.factor(num))
