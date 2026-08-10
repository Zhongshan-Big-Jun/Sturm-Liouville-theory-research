# -*- coding: utf-8 -*-
"""t3_correctNJ: recompute correct J2_2d numerator and NJ."""
import sympy as sp, pickle, json, math

with open('misc/t3_poly.pkl','rb') as fh: d = pickle.load(fh)
G, Gc, Gx, u, P, numGx, den_extra, NumJ = d['G'], d['Gc'], d['Gx'], d['u'], d['P'], d['numGx'], d['den_extra'], d['NumJ']
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
nG, dG = sp.fraction(sp.together(G))
nGc, dGc = sp.fraction(sp.together(Gc))
nu, du = sp.fraction(sp.together(u))
# correct: G = 4 nG/P^2 (since dG = (P/2)^2), Gc = 8 nGc/P^3, u = 2 nu/P
NumJ2 = sp.expand(16*nG**2*den_extra + 8*nGc*P*den_extra - 2*nu*numGx)
print('NumJ2 polynomial?', all(sp.degree(sp.fraction(sp.together(NumJ2))[1], s) == 0 for s in [A,t,sg,cg,st,ct]))
q0, rem0 = sp.div(NumJ2, den_extra)
print('div by den_extra:', rem0 == 0)
if rem0 == 0:
    NJ2 = sp.expand(q0)
    poly = sp.Poly(NJ2, A, t, sg, cg, st, ct)
    print('NJ2 terms:', len(poly.monoms()), 'deg:', poly.total_degree())
    coeffs = poly.coeffs(); monoms = poly.monoms()
    pos = [c for c in coeffs if c > 0]; neg = [c for c in coeffs if c < 0]
    print('pos:', len(pos), 'sum', sum(pos), 'max', max(pos), ' neg:', len(neg), 'sum', sum(neg), 'min', min(neg))
    # verify at corner
    Av, cv = 2*math.pi/3, 0.5
    tv = cv*Av; gv = math.pi-Av
    sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
    Pv = float(P.subs(sv).evalf(20))
    print('NJ2/P^4 at corner:', float(NJ2.subs(sv).evalf(20))/Pv**4)
    res = {'nterms': len(monoms), 'deg': poly.total_degree(),
           'monoms': [list(m) for m in monoms], 'coeffs': [str(c) for c in coeffs]}
    with open('misc/t3_NJ2.json','w') as fh: json.dump(res, fh)
    print('saved misc/t3_NJ2.json')
