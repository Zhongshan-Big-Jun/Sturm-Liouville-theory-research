# -*- coding: utf-8 -*-
"""t3_b2_q1_Q: analyze Q(g) on q=1 line (40-term bracket)."""
import sympy as sp, math

g = sp.symbols('g', positive=True)
s, c = sp.symbols('s c', positive=True)
# Q from the earlier factorization: B2q1 = 2 c^2 s Q
Q = (-5*c**4*g**4 + 13*sp.pi*c**4*g**3 - 9*sp.pi**2*c**4*g**2 - sp.pi**3*c**4*g + 2*sp.pi**4*c**4
     - 8*c**3*g**3*s + 6*sp.pi*c**3*g**2*s + 12*sp.pi**2*c**3*g*s - 10*sp.pi**3*c**3*s
     - 4*c**2*g**4*s**2 + 5*c**2*g**4 + 7*sp.pi*c**2*g**3*s**2 - 13*sp.pi*c**2*g**3
     - 2*sp.pi**2*c**2*g**2*s**2 + 9*sp.pi**2*c**2*g**2 - sp.pi**3*c**2*g*s**2 - 4*sp.pi*c**2*g*s**2
     + sp.pi**3*c**2*g + 4*sp.pi**2*c**2*s**2 - 2*sp.pi**4*c**2
     - 8*c*g**3*s**3 + 8*c*g**3*s + 8*sp.pi*c*g**2*s**3 - 13*sp.pi*c*g**2*s + 2*sp.pi**2*c*g*s
     + 6*sp.pi*c*s**3 + 3*sp.pi**3*c*s
     + g**4*s**4 - g**4*s**2 - 2*sp.pi*g**3*s**4 + 3*sp.pi*g**3*s**2 - sp.pi*g**3
     + sp.pi**2*g**2*s**4 - 3*sp.pi**2*g**2*s**2 + 3*sp.pi**2*g**2 + 6*sp.pi*g*s**2
     + sp.pi**3*g*s**2 - 3*sp.pi**3*g - 6*sp.pi**2*s**2 + sp.pi**4)
# substitute s^2 = 1 - c^2
Q2 = sp.expand(Q.subs(s**2, 1-c**2))
for _ in range(6):
    Q2 = sp.expand(Q2.subs(s**2, 1-c**2))
print('Q2 terms:', len(sp.Add.make_args(Q2)))
# express as polynomial in g
poly = sp.Poly(Q2, g)
print('deg in g:', poly.degree())
# factor
try:
    print('factor:', sp.factor(Q2))
except Exception as e:
    print('factor failed:', e)
# numeric check: Q/(2c^2 s) at endpoints
for gv in [2*math.pi/7, math.pi/3]:
    sv, cv = math.sin(gv), math.cos(gv)
    val = float(Q.subs({g: gv, s: sv, c: cv}).evalf(20))
    print('Q(%.4f) = %.6f' % (gv, val))
