# -*- coding: utf-8 -*-
"""Compute composed Gx and its partial derivative wrt x (fixed theta), numerator structure."""
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
def Dth(f):
    return sp.expand(sp.diff(f, th) + sp.diff(f, S)*C + sp.diff(f, C)*(-S))

ux = Dx(u)
Hx = Dx(H)
A0x = Dx(A0)
Gx = ux*V + u*(Hx - A0x)
print('Gx as single fraction...')
num, den = sp.fraction(sp.cancel(Gx))
print('num terms (unreduced):', len(sp.Add.make_args(sp.expand(num))))
print('den:', sp.factor(den))
