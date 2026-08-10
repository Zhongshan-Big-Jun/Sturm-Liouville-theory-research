# -*- coding: utf-8 -*-
"""Verify identity by reducing diff via s^2=1-b^2, S^2=1-C^2 substitutions."""
import sympy as sp
import json, time
x, th = sp.symbols('x th', positive=True)
s, b, S, C = sp.symbols('s b S C', positive=True)
Delta = b*s*th + C*S*x
q = S*b/(C*s)
Phi = b*b/(C*C)
c = th/x
D = q + c*Phi
u = x*Phi/D
A0 = sp.Rational(3)/x - 2*b/s
H = 2*c*(q*q-1)*s*(-b)/D
V = H - A0
G = u*V
Nsc = -s*b
Phix = 2*(q*q-1)*Nsc
ux_c = (Phi + x*Phix)/D - x*Phi*(c*Phix)/(D*D)
A0x_c = -sp.Rational(3)/(x*x) - 2/(s*s)
Hx_c = 2*c*(q*q-1)*((b*b - s*s)*D - s*(-b)*(c*Phix))/(D*D)
Gx_c = sp.cancel(ux_c*V + u*(Hx_c - A0x_c))
Gc_c = sp.cancel((-x*Phi*Phi/(D*D))*V + u*(2*(q*q-1)*Nsc*q/(D*D)))
J = sp.cancel(G*G + Gc_c - u*Gx_c)
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2sub = NJ2.subs({A: x, t: th, sg: s, cg: b, st: S, ct: C})
diff = sp.expand(16*Delta**4*J - NJ2sub)
# reduce: s^2 -> 1-b^2, S^2 -> 1-C^2 repeatedly
def reduce_trig(expr, var, other):
    poly = sp.Poly(expr, var)
    deg = poly.degree()
    if deg < 2: return expr
    e = sp.expand(expr)
    # express as polynomial in var: e = q2*var^2 + r(var<2) -> q2*(1-other) + r
    p = sp.Poly(e, var)
    q2 = p.coeff_monomial(var**2); rest = p - q2*var**2
    return sp.expand(rest + q2*(1-other))
for _ in range(3):
    diff = reduce_trig(diff, s, b*b)
    diff = reduce_trig(diff, S, C*C)
diff = sp.expand(diff)
print('reduced diff:', diff)
print('identity holds:', diff == 0)
