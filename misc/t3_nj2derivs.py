# -*- coding: utf-8 -*-
"""t3_nj2derivs: signs of dNJ2/dA, dNJ2/dc on region."""
import sympy as sp, json, math, numpy as np
from mpmath import mp, mpf, cos, sin, sqrt, pi as mppi
mp.dps = 30

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
# dNJ2/dA (with c fixed): A appears in A itself, in t=cA, and in gamma=pi-A (sg,cg)
# dNJ2/dc: A * dNJ2/dt
dNJ2dc = sp.expand(A*(sp.diff(NJ2, t) + ct*sp.diff(NJ2, st) - st*sp.diff(NJ2, ct)))
dNJ2dA = sp.diff(NJ2, A) + cg*0  # placeholder; do full chain below
# full d/dA at fixed c: gamma = pi - A, d sg/dA = -cos(pi-A) = cg... wait: sg=sin(gamma)=sin(pi-A), d sg/dA = -cos(pi-A) = -cg; cg=cos(pi-A), d cg/dA = sin(pi-A) = sg; t = cA, dt/dA = c; st=sin(t), dst/dA = c*ct; ct=cos(t), dct/dA = -c*st
g, c_ = sp.symbols('g c_')
sgA, cgA, stA, ctA = sp.sin(g), sp.cos(g), sp.sin(c_*A), sp.cos(c_*A)
NJ2A = NJ2.subs({sg: sgA, cg: cgA, st: stA, ct: ctA}).subs(g, sp.pi-A).subs(t, c_*A)
dA = sp.diff(NJ2A, A)
dc = sp.diff(NJ2A, c_)
fA = sp.lambdify((A, c_), dA, 'numpy')
fC = sp.lambdify((A, c_), dc, 'numpy')
Amin, Amax = 2*math.pi/3, math.pi-0.655
loA, hiA = 1e9, -1e9; loC, hiC = 1e9, -1e9
argA = argC = None
for i in range(120):
    Av = Amin + i*(Amax-Amin)/120
    for j in range(120):
        cv = 0.4 + j*0.1/120
        if Av*(1+cv) < math.pi: continue
        vA = float(fA(Av, cv)); vC = float(fC(Av, cv))
        if vA < loA: loA = vA; argA = (Av, cv)
        if vA > hiA: hiA = vA
        if vC < loC: loC = vC; argC = (Av, cv)
        if vC > hiC: hiC = vC
print('dNJ2/dA in [%.2f, %.2f], min at %s' % (loA, hiA, argA))
print('dNJ2/dc in [%.2f, %.2f], min at %s' % (loC, hiC, argC))
