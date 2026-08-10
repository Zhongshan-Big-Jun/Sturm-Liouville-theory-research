# -*- coding: utf-8 -*-
"""t3_debugB: compare B formula vs sympy at the claimed negative point."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJdt = sp.expand(sp.diff(NJ, t) + ct*sp.diff(NJ, st) - st*sp.diff(NJ, ct))
dNJdt_l = sp.lambdify((A,t,sg,cg,st,ct), dNJdt, 'numpy')

Av, cv = math.pi-0.655, 0.4365
tv = cv*Av; gv = math.pi-Av
sgv = math.sin(gv); cgv = math.cos(gv); stv = math.sin(tv); ctv = math.cos(tv)
w = ctv**2
d_exact = float(dNJdt_l(Av, tv, sgv, cgv, stv, ctv))
print('dNJ/dt exact:', d_exact)
F1 = 8*Av**3*cgv**2 - 8*Av**3*sgv**2 + 16*Av**3 + 16*Av**2*cgv**3*sgv + 16*Av**2*cgv*sgv**3 + 26*Av**2*cgv*sgv - 15*Av*sgv**2 + 15*cgv*sgv**3
F2 = (8*Av**2*cgv**4 - 8*Av**2*cgv**2*sgv**2 - 56*Av**2*cgv**2*w + 58*Av**2*cgv**2 + 16*Av**2*sgv**2*w - 12*Av**2*sgv**2
      + 48*Av**2*w**2 - 40*Av**2*w + 66*Av*cgv**3*sgv + 8*Av*cgv*sgv**3 - 38*Av*cgv*sgv*w + 15*Av*cgv*sgv + cgv**2*sgv**2)
F3 = (-72*Av**3*cgv**3*w + 36*Av**3*cgv**3 + 96*Av**3*cgv*w**2 - 32*Av**3*cgv*w - 16*Av**3*cgv
      + 8*Av**2*cgv**4*sgv - 8*Av**2*cgv**2*sgv**3 + 140*Av**2*cgv**2*sgv*w - 68*Av**2*cgv**2*sgv + 8*Av**2*sgv**3*w
      - 140*Av**2*sgv*w**2 + 104*Av**2*sgv*w - 48*Av*cgv**3*sgv**2*tv**2 + 42*Av*cgv**3*sgv**2 - 16*Av*cgv*sgv**4*tv**2
      + 72*Av*cgv*sgv**2*tv**2*w - 40*Av*cgv*sgv**2*w + 15*Av*cgv*sgv**2 - 32*cgv**2*sgv**3*tv**2 - 15*cgv**2*sgv**3)
print('F1,F2,F3 =', F1, F2, F3)
B = cgv**2*sgv*tv*F1 - 2*Av*sgv*tv*math.sqrt(w)*F2 - Av*math.sqrt(w*(1-w))*F3
print('B formula:', B)
print('2A^2 cg B:', 2*Av**2*cgv*B)
