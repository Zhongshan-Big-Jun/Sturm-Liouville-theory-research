# -*- coding: utf-8 -*-
"""Verify symbolic dGxdx and dJdx numerators against finite differences; print dGxdx num."""
import sympy as sp
import numpy as np
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
dGxdx = sp.cancel(Dx(Gx))
num, den = sp.fraction(dGxdx)
num = sp.expand(num)
terms = sp.Add.make_args(num)
print('dGxdx numerator terms:', len(terms))
# lambdify and compare with finite differences
f = sp.lambdify((x,th,s,b,S,C), dGxdx, 'numpy')
fGx = sp.lambdify((x,th,s,b,S,C), Gx, 'numpy')
def eval_at(xv, thv):
    return float(f(xv, thv, np.sin(xv), -np.cos(xv), np.sin(thv), np.cos(thv)))
def eval_Gx(xv, thv):
    return float(fGx(xv, thv, np.sin(xv), -np.cos(xv), np.sin(thv), np.cos(thv)))
h = 1e-6
for (xv, thv) in [(2.15, 1.05), (2.4, 1.0), (2.1, 1.04), (2.3, 1.13)]:
    fd = (eval_Gx(xv+h, thv) - eval_Gx(xv-h, thv))/(2*h)
    print('(%.3f,%.3f): sym=%.6f fd=%.6f' % (xv, thv, eval_at(xv, thv), fd))
# print numerator grouped
print()
print(sp.factor(num))
