# -*- coding: utf-8 -*-
"""t3_debugB2: compare sympy P1a/P1b/P2b with my hand transcriptions."""
import sympy as sp, pickle, math

with open('misc/t3_dNJdt_parity.pkl','rb') as fh: d = pickle.load(fh)
P1a, P1b, P2b = d['P1a'], d['P1b'], d['P2b']
A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)
Av, cv = math.pi-0.655, 0.4365
tv = cv*Av; gv = math.pi-Av
sgv = math.sin(gv); cgv = math.cos(gv)
wv = math.cos(tv)**2
sub = {A: Av, t: tv, sg: sgv, cg: cgv, w: wv}
for name, P in [('P1a',P1a),('P1b',P1b),('P2b',P2b)]:
    print(name, '=', float(P.subs(sub).evalf(20)))
# my hand F1 F2 F3
F1 = 8*Av**3*cgv**2 - 8*Av**3*sgv**2 + 16*Av**3 + 16*Av**2*cgv**3*sgv + 16*Av**2*cgv*sgv**3 + 26*Av**2*cgv*sgv - 15*Av*sgv**2 + 15*cgv*sgv**3
F2 = (8*Av**2*cgv**4 - 8*Av**2*cgv**2*sgv**2 - 56*Av**2*cgv**2*wv + 58*Av**2*cgv**2 + 16*Av**2*sgv**2*wv - 12*Av**2*sgv**2
      + 48*Av**2*wv**2 - 40*Av**2*wv + 66*Av*cgv**3*sgv + 8*Av*cgv*sgv**3 - 38*Av*cgv*sgv*wv + 15*Av*cgv*sgv + cgv**2*sgv**2)
F3 = (-72*Av**3*cgv**3*wv + 36*Av**3*cgv**3 + 96*Av**3*cgv*wv**2 - 32*Av**3*cgv*wv - 16*Av**3*cgv
      + 8*Av**2*cgv**4*sgv - 8*Av**2*cgv**2*sgv**3 + 140*Av**2*cgv**2*sgv*wv - 68*Av**2*cgv**2*sgv + 8*Av**2*sgv**3*wv
      - 140*Av**2*sgv*wv**2 + 104*Av**2*sgv*wv - 48*Av*cgv**3*sgv**2*tv**2 + 42*Av*cgv**3*sgv**2 - 16*Av*cgv*sgv**4*tv**2
      + 72*Av*cgv*sgv**2*tv**2*wv - 40*Av*cgv*sgv**2*wv + 15*Av*cgv*sgv**2 - 32*cgv**2*sgv**3*tv**2 - 15*cgv**2*sgv**3)
print('my F1 =', F1, ' F2 =', F2, ' F3 =', F3)
# expected: P1a = 2A^2 cg^3 sg t F1 ; P1b = -4 A^3 cg sg t sqrt(w) F2 ; P2b = -2 A^3 cg F3
print('2A^2 cg^3 sg t F1 =', 2*Av**2*cgv**3*sgv*tv*F1)
print('-4 A^3 cg sg t sqrt(w) F2 =', -4*Av**3*cgv*sgv*tv*math.sqrt(wv)*F2)
print('-2 A^3 cg F3 =', -2*Av**3*cgv*F3)
