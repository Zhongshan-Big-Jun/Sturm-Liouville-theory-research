# -*- coding: utf-8 -*-
"""t3_dencheck: find where the normalization breaks."""
import sympy as sp, pickle, math

with open('misc/t3_poly.pkl','rb') as fh: d = pickle.load(fh)
G, Gc, Gx, u, P, numGx, den_extra, NumJ = d['G'], d['Gc'], d['Gx'], d['u'], d['P'], d['numGx'], d['den_extra'], d['NumJ']
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
Av, cv = 2*math.pi/3, 0.5
tv = cv*Av; gv = math.pi-Av
sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
print('Gx direct:', float(Gx.subs(sv).evalf(20)))
print('numGx/(P^3 den_extra):', float((numGx/(P**3*den_extra)).subs(sv).evalf(20)))
print('NumJ/(P^4 den_extra):', float((NumJ/(P**4*den_extra)).subs(sv).evalf(20)))
print('G^2+Gc-uGx:', float((G**2+Gc-u*Gx).subs(sv).evalf(20)))
# check denominators of G, Gc, u
nG, dG = sp.fraction(sp.together(G))
nGc, dGc = sp.fraction(sp.together(Gc))
nu, du = sp.fraction(sp.together(u))
print('dG:', sp.factor(dG))
print('dGc:', sp.factor(dGc))
print('du:', sp.factor(du))
