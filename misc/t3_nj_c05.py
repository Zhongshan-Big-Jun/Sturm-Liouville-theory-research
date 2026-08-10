# -*- coding: utf-8 -*-
"""t3_nj_c05: scan NJ(A, 0.5) for A in [2pi/3, pi-0.655]."""
import sympy as sp, numpy as np, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

def nj_ac(Av, cv):
    tv = cv*Av
    sv = {A: Av, t: tv, sg: math.sin(Av), cg: -math.cos(Av), st: math.sin(tv), ct: math.cos(tv)}
    return float(NJ.subs(sv).evalf(20))

Amin, Amax = 2*math.pi/3, math.pi-0.655
NA = 2000
vals = []; worst = (1e9, None); best = (-1e9, None)
for i in range(NA+1):
    Av = Amin + i*(Amax-Amin)/NA
    v = nj_ac(Av, 0.5)
    vals.append(v)
    if v < worst[0]: worst = (v, Av)
    if v > best[0]: best = (v, Av)
print('NJ(A,0.5): min=%.6f at A=%.6f ; max=%.6f at A=%.6f' % (worst[0], worst[1], best[0], best[1]))
print('endpoints: A=2pi/3 -> %.4f ; A=pi-0.655 -> %.4f' % (vals[0], vals[-1]))
# derivative of NJ(A,0.5)
dA05 = [ (vals[i+1]-vals[i])/((Amax-Amin)/NA) for i in range(NA)]
print('dNJ(A,0.5)/dA: min=%.2f max=%.2f' % (min(dA05), max(dA05)))
# where is max
print('max at A=%.6f (gamma=%.6f)' % (best[1], math.pi-best[1]))
