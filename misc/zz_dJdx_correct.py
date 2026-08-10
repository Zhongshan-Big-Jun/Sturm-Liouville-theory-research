# -*- coding: utf-8 -*-
"""Compute dJ/dx|th (fixed theta) for the CORRECT J(x,q,c) and check sign on T2."""
import sympy as sp
x, q, c = sp.symbols('x q c', positive=True)
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
# partials of J3
Jx = sp.cancel(sp.diff(J3, x)); Jq = sp.cancel(sp.diff(J3, q)); Jc = sp.cancel(sp.diff(J3, c))
# dq/dx|th = tan(th)/sin^2(x); dc/dx|th = -th/x^2
th = sp.symbols('th', positive=True)
dJdx = sp.cancel(Jx + Jq*sp.tan(th)/sp.sin(x)**2 + Jc*(-th/x**2))
dJdx = sp.cancel(dJdx.subs({q: -sp.tan(th)/sp.tan(x), c: th/x}))
import mpmath as mp
mp.mp.dps = 40
f = sp.lambdify((x, th), dJdx, 'mpmath')
import math
gstar = mp.mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mp.pi/3, mp.pi-gstar
mn = (mp.mpf('1e30'), None); mx = (mp.mpf('-1e30'), None)
N = 100
for i in range(N+1):
    xv = xmin + mp.mpf(i)*(xmax-xmin)/N
    tlo = max(2*xv/5, mp.pi-xv); thi = min(xv/2, mp.atan(-2*mp.tan(xv)))
    if tlo >= thi: continue
    for j in range(N+1):
        tv = tlo + mp.mpf(j)*(thi-tlo)/N
        if tv <= tlo or tv >= thi: continue
        try:
            v = f(xv, tv)
        except Exception as e:
            print('err', e); continue
        if v < mn[0]: mn = (v, (float(xv), float(tv)))
        if v > mx[0]: mx = (v, (float(xv), float(tv)))
print('dJ/dx|th on T2: min %.6f max %.6f' % (mn[0], mx[0]))
# print a few values
for (xv, tv) in [(2.1, 1.045), (2.2, 1.0), (2.4, 1.1), (2.3, 0.95), (2.44, 1.02)]:
    print('  dJdx(%.3f,%.3f) = %.6f' % (xv, tv, f(mp.mpf(xv), mp.mpf(tv))))
