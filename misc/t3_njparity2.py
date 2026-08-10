# -*- coding: utf-8 -*-
"""t3_njparity2: clean step-by-step parity decomposition of NJ."""
import sympy as sp, json, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
NJr = sp.expand(NJ)
for _ in range(10):
    NJr = sp.expand(NJr.subs(st**2, 1-ct**2))
# split by st power (only 0 or 1 remain)
NJr0 = sp.expand(NJr.subs(st, 0))
NJr1 = sp.expand((NJr - NJr0)/st)
print('NJr1 has st?', NJr1.has(st))
# split each by ct parity
E0e = sp.expand(NJr0.subs(ct, 0))
E0o = sp.expand((NJr0 - E0e)/ct)
E1e = sp.expand(NJr1.subs(ct, 0))
E1o = sp.expand((NJr1 - E1e)/ct)
# check each is polynomial in ct^2
for name, P in [('E0e',E0e),('E0o',E0o),('E1e',E1e),('E1o',E1o)]:
    print(name, 'has odd ct?', P.has(ct), ' terms:', len(sp.Add.make_args(P)))
w = sp.symbols('w', positive=True)
def to_w(expr):
    e = sp.expand(expr)
    return sp.expand(e.subs(ct**2, w))
E0e, E0o, E1e, E1o = to_w(E0e), to_w(E0o), to_w(E1e), to_w(E1o)
recon = E0e + sp.sqrt(w)*E0o + sp.sqrt(1-w)*E1e + sp.sqrt(w*(1-w))*E1o
# verify numerically instead of symbolically
import math
def ev_recon(Av, cv):
    tv = cv*Av; gv = math.pi-Av; wv = math.cos(tv)**2
    sub = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), w: wv}
    return float((E0e + math.sqrt(wv)*E0o + math.sqrt(1-wv)*E1e + math.sqrt(wv*(1-wv))*E1o).subs(sub).evalf(20))
def ev_direct(Av, cv):
    tv = cv*Av; gv = math.pi-Av
    sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
    return float(NJ.subs(sv).evalf(20))
for Av, cv in [(2.1,0.45),(2.3,0.42),(2.45,0.48),(2*math.pi/3,0.5),(math.pi-0.655,0.4365)]:
    print(f'A={Av:.4f} c={cv:.4f}: recon={ev_recon(Av,cv):.6f} direct={ev_direct(Av,cv):.6f}')
with open('misc/t3_NJ_parity.pkl','wb') as fh: pickle.dump({'E0e':E0e,'E0o':E0o,'E1e':E1e,'E1o':E1o}, fh)
print('N1 (=E0o) =', sp.factor(E0o))
print('N3 (=E1o) =', sp.factor(E1o))
print('N2 (=E1e) =', sp.factor(E1e))
