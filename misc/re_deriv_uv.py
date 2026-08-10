# -*- coding: utf-8 -*-
"""Lighter: partials for u, V, ux only; then Gx, J via numeric+structured checks."""
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

for nm, f in [('u', u), ('V', V)]:
    for lbl, d in [('dx', Dx(f)), ('dth', Dth(f))]:
        num, den = sp.fraction(d)
        num = sp.expand(num)
        print('== d%s/%s: num=%d terms ==' % (nm, lbl, len(sp.Add.make_args(num))))
        print(sp.factor(num))
        print()
