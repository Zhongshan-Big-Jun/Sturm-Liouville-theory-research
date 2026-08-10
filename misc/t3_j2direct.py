# -*- coding: utf-8 -*-
"""t3_j2direct: evaluate G, Gc, u, Gx directly at corner, compare J2_2d variants."""
import sympy as sp, math, pickle

with open('misc/t3_poly.pkl','rb') as fh: d = pickle.load(fh)
G, Gc, Gx, u, P, numGx, den_extra = d['G'], d['Gc'], d['Gx'], d['u'], d['P'], d['numGx'], d['den_extra']
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
Av, cv = 2*math.pi/3, 0.5
tv = cv*Av; gv = math.pi-Av
sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
for name, expr in [('G',G),('Gc',Gc),('u',u),('Gx',Gx),('P',P)]:
    print(name, '=', float(expr.subs(sv).evalf(20)))
J2 = float((G**2 + Gc - u*Gx).subs(sv).evalf(20))
print('J2_2d = G^2+Gc-u*Gx =', J2)
# document formula at (gamma, q) = (pi/3, 1): x = pi-gamma = 2pi/3
x = 2*math.pi/3
import math as m
N = 12 + 16*x/m.tan(x) + 2*x**2/m.tan(x)**2 - 2*x**2
print('doc x^2 N/pi^2 =', x**2*N/m.pi**2)
