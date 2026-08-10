# -*- coding: utf-8 -*-
"""t3_njsplit: NJ = E(A,t,sg,cg,w) + st*ct*O(A,t,sg,cg,w), w=ct^2 (so st^2=1-w)."""
import sympy as sp, json, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
w = sp.symbols('w', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
# reduce st^2 -> 1-ct^2
NJr = sp.expand(NJ)
for _ in range(8):
    NJr = sp.expand(NJr.subs(st**2, 1-ct**2))
# split: E = terms with st^0; O = (NJr - E)/(st*ct)  (after reducing ct^2 -> w)
E = sp.expand(NJr.subs(st, 0))
Osc = sp.expand((NJr - E)/(st*ct))
E = sp.expand(E.subs(ct**2, w))
O = sp.expand(Osc.subs(ct**2, w))
print('E terms:', len(sp.Add.make_args(E)))
print('O terms:', len(sp.Add.make_args(O)))
print('E has sqrt?', E.has(sp.sqrt), ' O has sqrt?', O.has(sp.sqrt))
# numeric check
import math
def ev_NJ(Av, cv):
    tv = cv*Av
    wv = math.cos(tv)**2
    E_v = float(E.subs({A: Av, t: tv, sg: math.sin(math.pi-Av), cg: -math.cos(math.pi-Av), w: wv}).evalf(20))
    O_v = float(O.subs({A: Av, t: tv, sg: math.sin(math.pi-Av), cg: -math.cos(math.pi-Av), w: wv}).evalf(20))
    stc = math.sin(tv)*math.cos(tv)
    return E_v + stc*O_v
def ev_direct(Av, cv):
    tv = cv*Av; gv = math.pi-Av
    sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
    return float(NJ.subs(sv).evalf(20))
for Av, cv in [(2.1,0.45),(2.3,0.42),(2.45,0.48),(2*math.pi/3,0.5)]:
    print('A=%.4f c=%.4f: split=%.4f direct=%.4f' % (Av, cv, ev_NJ(Av,cv), ev_direct(Av,cv)))
with open('misc/t3_E0.pkl','wb') as fh: pickle.dump({'E':E,'O':O}, fh)
print('saved')
