# -*- coding: utf-8 -*-
"""t3_mono_nj: check monotonicity of NJ in c and A on the relaxed (A,c) region."""
import sympy as sp, numpy as np, json

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

# NJ as function of (A,c): t=cA, sg=sinA, cg=-cosA, st=sin(cA), ct=cos(cA)
def NJ_ac(Av, cv):
    tv = cv*Av
    sv = {A: Av, t: tv, sg: np.sin(Av), cg: -np.cos(Av), st: np.sin(tv), ct: np.cos(tv)}
    return float(NJ.subs(sv).evalf(20))

# derivative dNJ/dc = A*dNJ/dt (t=cA, partials of st,ct included)
dNJ_dt = sp.diff(NJ, t) + ct*sp.diff(NJ, st) - st*sp.diff(NJ, ct)
dNJ_dc = A*dNJ_dt
# dNJ/dA = dNJ/dA_direct + (dNJ/dt)*(dt/dA=dNJ_dc/A...) + chain on sg,cg
dNJ_dA = sp.diff(NJ, A) + sp.diff(NJ, sg)*cg + sp.diff(NJ, cg)*(-sg) + (t/A)*dNJ_dt
f_dc = sp.lambdify((A,t,sg,cg,st,ct), dNJ_dc, 'numpy')
f_dA = sp.lambdify((A,t,sg,cg,st,ct), dNJ_dA, 'numpy')

Amin, Amax = 2*math.pi/3, math.pi-0.655
import math
cmin, cmax = 0.4, 0.5
NA, Nc = 300, 200
worst_c = (1e9, -1e9); worst_A = (1e9, -1e9)
for i in range(NA+1):
    Av = Amin + i*(Amax-Amin)/NA
    for j in range(Nc+1):
        cv = cmin + j*(cmax-cmin)/Nc
        if Av*(1+cv) < math.pi - 1e-12:  # constraint A>=pi/(1+c)
            continue
        tv = cv*Av
        sv = (Av, tv, math.sin(Av), -math.cos(Av), math.sin(tv), math.cos(tv))
        dc = float(f_dc(*sv)); dA = float(f_dA(*sv))
        worst_c = (min(worst_c[0], dc), max(worst_c[1], dc))
        worst_A = (min(worst_A[0], dA), max(worst_A[1], dA))
print('dNJ/dc range on relaxed region: [%.4f, %.4f]' % worst_c)
print('dNJ/dA range on relaxed region: [%.4f, %.4f]' % worst_A)
