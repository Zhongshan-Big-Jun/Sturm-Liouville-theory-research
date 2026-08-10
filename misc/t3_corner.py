# -*- coding: utf-8 -*-
"""t3_corner: verify J2_2d = NJ/P^4 at corners."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
P = 2*(A*st*ct + t*sg*cg)
for (Av,cv,name) in [(2*math.pi/3, 0.5, 'corner A=2pi/3,c=1/2'), (math.pi-0.655, 0.4, 'corner A=pi-0.655,c=0.4'), (math.pi/1.4, 0.4, 'minB corner')]:
    tv = cv*Av; gv = math.pi-Av
    sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
    nj = float(NJ.subs(sv).evalf(20))
    pv = float(P.subs(sv).evalf(20))
    print(f'{name}: NJ={nj:.4f} P={pv:.4f} J2_2d={nj/pv**4:.4f}')
