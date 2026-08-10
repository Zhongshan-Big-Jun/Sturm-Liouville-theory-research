# -*- coding: utf-8 -*-
"""Gx - 21/5: combined numerator, look for factorization/structure."""
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
num, den = sp.fraction(Gx)
# Gx - 21/5 = (num - (21/5)*den)/den
combo = sp.expand(num - sp.Rational(21,5)*den)
print('combined numerator terms:', len(sp.Add.make_args(combo)))
print('factor:', sp.factor(combo))
print()
# try u*Gx - 11/2
ugx = sp.cancel(u*Gx)
n2, d2 = sp.fraction(ugx)
combo2 = sp.expand(n2 - sp.Rational(11,2)*d2)
print('uGx-11/2 numerator terms:', len(sp.Add.make_args(combo2)))
print('factor:', sp.factor(combo2))
