# -*- coding: utf-8 -*-
"""t3_dA_ranges: numeric ranges of P0 and Q in dNJ2/dA = P0 + sqrt(w(1-w))*Q."""
import numpy as np, math
Amin, Amax = 2*math.pi/3, math.pi-0.655

# P0 and Q from the symbolic split (recompute numerically directly from definition of dNJ2/dA instead)
import sympy as sp, json
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
c = sp.symbols('c', positive=True)
dA_expr = sp.expand(sp.diff(NJ2, A) + c*sp.diff(NJ2, t) - cg*sp.diff(NJ2, sg) + sg*sp.diff(NJ2, cg)
                    + c*ct*sp.diff(NJ2, st) - c*st*sp.diff(NJ2, ct))
dA_expr = sp.expand(dA_expr.subs(t, c*A))
# extract P0 (pure w part) and Q (sqrt(w(1-w)) coeff) directly
dAr = sp.expand(dA_expr)
for _ in range(10):
    dAr = sp.expand(dAr.subs(st**2, 1-ct**2))
w = sp.symbols('w', positive=True)
E = sp.expand(dAr.subs({ct: sp.sqrt(w), st: sp.sqrt(1-w)}))
for _ in range(15):
    rep = {}
    for p in E.atoms(sp.Pow):
        if p.base == w and sp.Rational(p.exp.denominator) == 2 and int(p.exp.numerator) % 2 == 1:
            k = int(p.exp.numerator); rep[p] = w**((k-1)//2)*sp.sqrt(w)
    if not rep: break
    E = sp.expand(E.subs(rep))
E = sp.expand(E)
P0 = sp.Integer(0); Q = sp.Integer(0)
sw1 = sp.sqrt(w*(1-w))
for term in sp.Add.make_args(E):
    if term.has(sw1):
        Q += sp.expand(term/sw1)
    else:
        P0 += term
P0 = sp.expand(P0); Q = sp.expand(Q)
fP0 = sp.lambdify((A, c, sg, cg, w), P0.subs(t, c*A), 'numpy')
fQ = sp.lambdify((A, c, sg, cg, w), Q.subs(t, c*A), 'numpy')
loP, hiP, loQ, hiQ = 1e18, -1e18, 1e18, -1e18
argP = argQ = None
for i in range(150):
    Av = Amin + i*(Amax-Amin)/150
    for j in range(150):
        cv = 0.4 + j*0.1/150
        if Av*(1+cv) < math.pi: continue
        gv = math.pi-Av; tv = cv*Av
        p0 = float(fP0(Av, cv, math.sin(gv), math.cos(gv), math.cos(tv)**2))
        q = float(fQ(Av, cv, math.sin(gv), math.cos(gv), math.cos(tv)**2))
        if p0 < loP: loP = p0; argP = (Av, cv)
        if p0 > hiP: hiP = p0
        if q < loQ: loQ = q; argQ = (Av, cv)
        if q > hiQ: hiQ = q
print('P0 in [%.2f, %.2f] min at %s' % (loP, hiP, argP))
print('Q in [%.2f, %.2f] min at %s' % (loQ, hiQ, argQ))
print('sqrt(w(1-w))*Q range approx: [%.2f, %.2f]' % (loQ*0.29, hiQ*0.5))
