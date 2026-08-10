# -*- coding: utf-8 -*-
"""t3_Gx_c12d.py: verify closed form, reduce M, structure analysis."""
import sympy as sp, math
from mpmath import mp, mpf, cos, sin, pi as mppi
mp.dps = 30
s, b, x = sp.symbols('s b x', positive=True)
M = (b**7*s**2*x - 2*b**6*x + 2*b**5*s**4*x + b**5*s**3 - b**5*s**2*x + 3*b**5*s - 2*b**5*x - 2*b**4*s**4*x - 3*b**4*s**3 - 2*b**4*s**2*x + 5*b**4*s + 2*b**4*x + b**3*s**6*x + b**3*s**5 + 2*b**3*s**4*x - 3*b**3*s**3 - 3*b**3*s + 4*b**3*x - 2*b**2*s**6*x - 3*b**2*s**5 + 2*b**2*s**4*x - 3*b**2*s**3 - 2*b**2*s**2*x - 5*b**2*s + 3*b*s**6*x + 2*b*s**5 - 3*b*s**3 - 2*b*s**2*x - 2*b*x - 2*s**6*x + 3*s**3)
Gx = -2*M/(s**4*(1+b)**3)
# verify numerically at a few x values on c=1/2
def comps_xth(xv, th):
    q = -mp.tan(th)/mp.tan(xv)
    sx, bx = sin(xv), -cos(xv)
    S, C = sin(th), cos(th)
    Phi = bx*bx/(C*C)
    c = th/xv
    den = q + c*Phi
    u = xv*Phi/den
    A0 = mpf(3)/xv - 2*bx/sx
    H = 2*c*(q*q-1)*sx*(-bx)/den
    V = H - A0
    Phix = -2*sx*bx*(q*q-1)
    ux = (Phi + xv*Phix)/den - xv*Phi*c*Phix/(den*den)
    A0x = -3/(xv*xv) - 2/(sx*sx)
    Hx = (2*c*(q*q-1)*(bx*bx - sx*sx)*den - 2*c*(q*q-1)*sx*(-bx)*c*Phix)/(den*den)
    return ux*V + u*(Hx - A0x)
for xv in [mpf(2)*mppi/3, mpf('2.15'), mpf('2.25'), mpf('2.3')]:
    bv = -cos(xv); sv = sin(xv)
    cf = float(Gx.subs({s:sv, b:bv, x:xv}).evalf(20))
    nc = float(comps_xth(xv, xv/2))
    print('x=%.4f: closed=%.6f numeric=%.6f diff=%.1e' % (xv, cf, nc, abs(cf-nc)))
# reduce M with s^2 = 1 - b^2
Mr = sp.expand(M.subs(s**2, 1-b**2))
# iterative reduction
for _ in range(4):
    Mr = sp.expand(Mr)
    Mr = Mr.subs(s**2, 1-b**2)
Mr = sp.expand(Mr)
print()
print('M reduced (in b, x, s):')
print(Mr)
print('terms:', len(sp.Add.make_args(Mr)))
# group by power of s
p = sp.Poly(Mr, s)
print('as poly in s:', p.as_expr())
