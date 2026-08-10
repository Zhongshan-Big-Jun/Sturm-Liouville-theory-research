# -*- coding: utf-8 -*-
"""t3_debugB3: term-by-term compare."""
import sympy as sp, pickle, math

with open('misc/t3_dNJdt_parity.pkl','rb') as fh: d = pickle.load(fh)
P1b, P2b = d['P1b'], d['P2b']
A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)
Av, cv = math.pi-0.655, 0.4365
tv = cv*Av; gv = math.pi-Av
sgv = math.sin(gv); cgv = math.cos(gv)
wv = math.cos(tv)**2
sub = {A: Av, t: tv, sg: sgv, cg: cgv, w: wv}
print('P1b sympy =', float(P1b.subs(sub).evalf(20)))
print('P2b sympy =', float(P2b.subs(sub).evalf(20)))
# my transcriptions
F2 = (8*Av**2*cgv**4 - 8*Av**2*cgv**2*sgv**2 - 56*Av**2*cgv**2*wv + 58*Av**2*cgv**2 + 16*Av**2*sgv**2*wv - 12*Av**2*sgv**2
      + 48*Av**2*wv**2 - 40*Av**2*wv + 66*Av*cgv**3*sgv + 8*Av*cgv*sgv**3 - 38*Av*cgv*sgv*wv + 15*Av*cgv*sgv + cgv**2*sgv**2)
F3 = (-72*Av**3*cgv**3*wv + 36*Av**3*cgv**3 + 96*Av**3*cgv*wv**2 - 32*Av**3*cgv*wv - 16*Av**3*cgv
      + 8*Av**2*cgv**4*sgv - 8*Av**2*cgv**2*sgv**3 + 140*Av**2*cgv**2*sgv*wv - 68*Av**2*cgv**2*sgv + 8*Av**2*sgv**3*wv
      - 140*Av**2*sgv*wv**2 + 104*Av**2*sgv*wv - 48*Av*cgv**3*sgv**2*tv**2 + 42*Av*cgv**3*sgv**2 - 16*Av*cgv*sgv**4*tv**2
      + 72*Av*cgv*sgv**2*tv**2*wv - 40*Av*cgv*sgv**2*wv + 15*Av*cgv*sgv**2 - 32*cgv**2*sgv**3*tv**2 - 15*cgv**2*sgv**3)
print('F2 =', F2, ' F3 =', F3)
print('my -4A^3 cg sg t sqrt(w) F2 =', -4*Av**3*cgv*sgv*tv*math.sqrt(wv)*F2)
print('my -2A^3 cg F3 =', -2*Av**3*cgv*F3)
# term by term P1b
print('P1b terms:')
for term in sp.Add.make_args(P1b):
    val = float(term.subs(sub).evalf(20))
    print(f'   {val:+.4f}   {term}')
