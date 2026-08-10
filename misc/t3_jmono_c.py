# -*- coding: utf-8 -*-
"""t3_jmono_c: check monotonicity of J2_2d (and NJ, P^4) in c on the relaxed region."""
import sympy as sp, math, numpy as np

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_poly.pkl','rb') as fh:
    d = pickle_load = __import__('pickle').load(fh)
G, Gc, Gx, u, P = d['G'], d['Gc'], d['Gx'], d['u'], d['P']
J2 = G**2 + Gc - u*Gx
# J2 as function of (A,c): t=cA, sg=sinA, cg=-cosA, st=sin(cA), ct=cos(cA)
def J(Av, cv):
    tv = cv*Av
    sv = {A: Av, t: tv, sg: math.sin(Av), cg: -math.cos(Av), st: math.sin(tv), ct: math.cos(tv)}
    return float(J2.subs(sv).evalf(20))
Amin, Amax = 2*math.pi/3, math.pi-0.655
worst = (1e9,-1e9); worst_slope_c = (1e9,-1e9)
NA, Nc = 200, 150
dc = 1e-5
for i in range(NA+1):
    Av = Amin + i*(Amax-Amin)/NA
    for j in range(Nc+1):
        cv = 0.4 + j*0.1/Nc
        if Av*(1+cv) < math.pi - 1e-12: continue
        v = J(Av, cv)
        worst = (min(worst[0], v), max(worst[1], v))
        # slope in c
        s = (J(Av, cv+dc) - J(Av, cv-dc))/(2*dc)
        worst_slope_c = (min(worst_slope_c[0], s), max(worst_slope_c[1], s))
print('J2_2d on relaxed region: [%.4f, %.4f]' % worst)
print('dJ2_2d/dc (finite diff): [%.4f, %.4f]' % worst_slope_c)
