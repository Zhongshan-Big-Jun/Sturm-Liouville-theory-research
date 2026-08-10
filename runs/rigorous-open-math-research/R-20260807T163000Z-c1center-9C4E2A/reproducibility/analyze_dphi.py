# -*- coding: utf-8 -*-
"""analyze phi'(b) closed form: reduce to polynomial in u=cos(2pi b), v=sin(2pi b)."""
import sympy as sp
import numpy as np
b, alpha, u, v = sp.symbols("b alpha u v", real=True)
pi = sp.pi
# phi'(b) from the verified closed form (sym_phi_closedform3 output)
dphi = sp.sqrt(15)*(-128*sp.sqrt(15)*pi**2*alpha*sp.cos(2*pi*b) - 1792*sp.sqrt(15)*pi**2*alpha*sp.cos(4*pi*b) + 1920*sp.sqrt(15)*pi**2*alpha - 7680*pi**2*b*sp.sin(2*pi*b)*sp.cos(2*pi*b) + 1920*pi**2*b*sp.sin(2*pi*b) + 7680*pi**2*sp.sin(2*pi*b)*sp.cos(2*pi*b) - 1920*pi**2*sp.sin(2*pi*b) + 1920*pi*sp.cos(2*pi*b)**2 - 2880*pi*sp.cos(2*pi*b) + 1920*pi*sp.cos(4*pi*b) - 960*pi)/(57600*pi**2)
# substitute cos(2pi b)=u, sin(2pi b)=v, cos(4pi b)=2u^2-1, sin(4pi b)=2uv
dphi_uv = dphi.subs({sp.cos(2*pi*b): u, sp.sin(2*pi*b): v, sp.cos(4*pi*b): 2*u**2-1})
dphi_uv = sp.expand(dphi_uv)
print("phi' in (u,v):")
print(sp.factor(dphi_uv))
print()
coef = sp.collect(sp.expand(dphi_uv*(57600*pi**2)/sp.sqrt(15)), [u, v])
print("57600 pi^2 / sqrt(15) * phi' =")
print(coef)
print()
# numeric coefficients with alpha = a0
a0 = float(sp.acos(sp.Rational(1,4))/pi)
def C(expr):
    return float(sp.N(expr.subs(alpha, sp.Float(a0, 30)), 25))
# write as A u^2 + B u + C0 + v*(E b + F u b + G u + H)
poly_part = sp.expand((dphi_uv*(57600*pi**2)/sp.sqrt(15)).subs(alpha, sp.Float(a0,30)))
A = C(sp.diff(dphi_uv*(57600*pi**2)/sp.sqrt(15), u, 2)/2)
Bu = C(sp.diff(dphi_uv*(57600*pi**2)/sp.sqrt(15), u).subs(u,0))
C0 = C((dphi_uv*(57600*pi**2)/sp.sqrt(15)).subs({u:0, v:0}))
print("A =", A, " B =", Bu, " C0 =", C0)
# v-part coefficient: v*(D0 + D1*b + D2*u + D3*b*u)
expr = dphi_uv*(57600*pi**2)/sp.sqrt(15)
vcoef = sp.expand(sp.factor(sp.collect(sp.expand(expr - expr.subs(v,0).subs(u,u)), v))/v)
print("v coefficient =", vcoef)
print("vcoef with alpha=a0 =", sp.N(vcoef.subs(alpha, sp.Float(a0,30)), 25))
# evaluate P(u) = A u^2 + B u + C0 on [-1, 1]
uu = np.linspace(-1, 1, 10001)
P = A*uu**2 + Bu*uu + C0
print("P(u) on [-1,1]: min=%.6f max=%.6f" % (P.min(), P.max()))
print("vertex u* =", -Bu/(2*A), " P(vertex) =", A*(-Bu/(2*A))**2 + Bu*(-Bu/(2*A)) + C0)
print("P(-1) =", A - Bu + C0, " P(1) =", A + Bu + C0)
