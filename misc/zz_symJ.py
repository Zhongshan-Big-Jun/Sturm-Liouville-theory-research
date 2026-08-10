# -*- coding: utf-8 -*-
"""Symbolic machinery: correct J(x,th) = G^2 + Gc - u*Gx (partials at fixed q,c),
as functions of (x,th); compute dJ/dx|th and check sign on T2."""
import sympy as sp
x, th = sp.symbols('x th', positive=True)
s, b, S, C = sp.symbols('s b S C', positive=True)
Delta = b*s*th + C*S*x          # = W0-tilde
u = b*s*x**2/Delta
A0 = sp.Rational(3)/x - 2*b/s
H = 2*th*(C**2*s**2 - S**2*b**2)/Delta
V = H - A0
G = u*V
# partial derivatives at fixed (q,c) in terms of (x,th): use Dx/Dth then convert?
# Correct Gx, Gc as functions of (x,th):
# Gx_c = dG/dx |_{q,c}; Gc_c = dG/dc |_{q,x}
# On the plane, (q,c) are functions of (x,th): q = -tan(th)/tan(x), c = th/x.
# dG/dx|_{q,c} = dG/dx|th + (dG/dth|x)*(dth/dx)|_{q,c} where dth/dx|_{q,c} is the
#   change in th needed to keep q,c fixed: c fixed => dth = c dx = (th/x)dx; then q fixed
#   automatically? NO: q = -tan(th)/tan(x) depends on both. With c=th/x fixed, dth=(th/x)dx,
#   then dq = -sec^2(th)/tan(x) dth + tan(th)sec^2(x)/tan^2(x) dx = dx*[...].
# Let's just compute the partials directly from the explicit formulas in (x,q,c):
q, c = sp.symbols('q c', positive=True)
Phi = sp.cos(x)**2 + q**2*sp.sin(x)**2
D = q + c*Phi
u3 = x*Phi/D
A03 = sp.Rational(3)/x + 2*sp.cot(x)
H3 = 2*c*(q**2-1)*sp.sin(x)*sp.cos(x)/D
V3 = H3 - A03
G3 = u3*V3
Gx3 = sp.cancel(sp.diff(G3, x))
Gc3 = sp.cancel(sp.diff(G3, c))
J3 = sp.cancel(G3**2 + Gc3 - u3*Gx3)
# substitute q = -tan(th)/tan(x), c = th/x, and trig identities s=sin x, b=-cos x etc.
qsub = -sp.tan(th)/sp.tan(x)
csub = th/x
def to_plane(expr):
    e = expr.subs({q: qsub, c: csub})
    e = sp.simplify(e)   # may be slow; try
    return e
# For numerical checking, lambdify J3 directly (symbolic with x, q, c)
import numpy as np
fJ = sp.lambdify((x, q, c), J3, 'numpy')
def Jval(xv, qv, cv): return fJ(xv, qv, cv)
# compare with comps at sample points
from mpmath import mp, mpf, tan, atan, pi as mppi
mp.dps = 40
def compsJ(xv, thv):
    xv = mpf(xv); thv = mpf(thv)
    q = -tan(thv)/tan(xv); c = thv/xv
    return float(Jval(float(xv), float(q), float(c)))
for (x, th) in [(2.2, 1.0), (2.4, 1.1), (2.1, 1.045), (2.35, 0.98)]:
    print('J symbolic = %.6f' % compsJ(x, th))
