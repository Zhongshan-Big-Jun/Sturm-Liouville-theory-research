# -*- coding: utf-8 -*-
"""t3_q1line: NJ and B on the q=1 line (t=gamma), factor checks."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJdt = sp.expand(sp.diff(NJ, t) + ct*sp.diff(NJ, st) - st*sp.diff(NJ, ct))

# q=1 line: t=gamma=pi-A, st=sg, ct=cg  (sin t = sin g, cos t = cos g)
# substitute t -> pi-A? Better: use gamma variable. t = gamma, A = pi-gamma.
g = sp.symbols('g', positive=True)
sub_q1 = {A: sp.pi-g, t: g, st: sg, ct: cg}
NJ_q1 = sp.expand(NJ.subs(sub_q1))
# also sg=sin g, cg=cos g
NJ_q1b = sp.expand(NJ_q1.subs({sg: sp.sin(g), cg: sp.cos(g)}))
print('NJ on q=1 line (as function of g):')
print(sp.trigsimp(NJ_q1b))
print()
# try factor as polynomial in sin g, cos g
s, c = sp.symbols('s c', positive=True)
NJ_q1p = sp.expand(NJ.subs({A: sp.pi-g, t: g, sg: s, cg: c, st: s, ct: c}))
print('factor (as poly in s,c with pi):')
try:
    print(sp.factor(NJ_q1p))
except Exception as e:
    print('failed:', e)
