# -*- coding: utf-8 -*-
"""t3_njcheck: verify JSON NJ matches true NJ from NumJ/den_extra."""
import sympy as sp, json, pickle, math

with open('misc/t3_poly.pkl','rb') as fh: d = pickle.load(fh)
NumJ, den_extra = d['NumJ'], d['den_extra']
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
NJ_true = sp.expand(NumJ/den_extra)
print('NJ_true poly?', sp.Poly(NJ_true, A,t,sg,cg,st,ct).is_polynomial if False else 'check')
try:
    p = sp.Poly(NJ_true, A,t,sg,cg,st,ct)
    print('NJ_true terms:', len(p.monoms()))
except Exception as e:
    print('not poly:', e)
# evaluate true NJ at corner
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ_json = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
Av, cv = 2*math.pi/3, 0.5
tv = cv*Av; gv = math.pi-Av
sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
print('NJ_json at corner:', float(NJ_json.subs(sv).evalf(20)))
print('NJ_true at corner:', float(NJ_true.subs(sv).evalf(20)))
print('diff:', float(sp.N(sp.expand(NJ_json - NJ_true).subs(sv))))
print('equal symbolic?', sp.expand(NJ_json - NJ_true) == 0)
