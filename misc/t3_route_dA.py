# -*- coding: utf-8 -*-
"""t3_route_dA: verify dNJ2/dA|c < 0 numerically and q=1 line with NJ2."""
import sympy as sp, json, math
import numpy as np

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
c = sp.symbols('c', positive=True)

with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

dA_expr = sp.expand(sp.diff(NJ2, A) + c*sp.diff(NJ2, t) - cg*sp.diff(NJ2, sg) + sg*sp.diff(NJ2, cg)
                    + c*ct*sp.diff(NJ2, st) - c*st*sp.diff(NJ2, ct))
dA_expr = sp.expand(dA_expr.subs(t, c*A))
f_dA = sp.lambdify((A,c,sg,cg,st,ct), dA_expr, 'numpy')
f_NJ = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'numpy')

Amin, Amax = 2*math.pi/3, math.pi-0.655
def ev(Av, cv):
    tv = cv*Av; gv = math.pi-Av
    return float(f_dA(Av, cv, math.sin(gv), math.cos(gv), math.sin(tv), math.cos(tv))), \
           float(f_NJ(Av, tv, math.sin(gv), math.cos(gv), math.sin(tv), math.cos(tv)))

# grid scan over loose region
loA, hiA = 1e30, -1e30; loN, hiN = 1e30, -1e30
argA = None; argN = None
N = 120
for i in range(N+1):
    for j in range(N+1):
        Av = Amin + i*(Amax-Amin)/N
        cv = 0.4 + j*0.1/N
        if Av*(1+cv) < math.pi: continue
        dA, nj = ev(Av, cv)
        if dA > hiA: hiA = dA; argA = ('max',Av,cv)
        if dA < loA: loA = dA; argA = ('min',Av,cv)
        if nj > hiN: hiN = nj; argN = ('max',Av,cv)
        if nj < loN: loN = nj; argN = ('min',Av,cv)
print('dNJ2/dA|c over loose region: [%.1f, %.1f]  %s' % (loA, hiA, argA))
print('NJ2 over loose region: [%.2f, %.2f]  %s' % (loN, hiN, argN))

# q=1 line: A = pi/(1+c), t = cA = pi c/(1+c), gamma = pi - A = pi c/(1+c)
print()
print('q=1 line: NJ2 values for c in [0.4,0.5]:')
best = (1e30, None)
for j in range(101):
    cv = 0.4 + j*0.1/100
    Av = math.pi/(1+cv); tv = cv*Av; gv = math.pi-Av
    nj = float(f_NJ(Av, tv, math.sin(gv), math.cos(gv), math.sin(tv), math.cos(tv)))
    if nj < best[0]: best = (nj, (Av, cv))
print('min NJ2 on q=1 line:', best)

# factor q1 with NJ2
g = sp.symbols('g', positive=True)
s, c2 = sp.symbols('s c2', positive=True)
NJ_q1p = sp.expand(NJ2.subs({A: sp.pi-g, t: g, sg: s, cg: c2, st: s, ct: c2}))
try:
    print('factor (poly in s,c with pi):')
    print(sp.factor(NJ_q1p))
except Exception as e:
    print('failed:', e)
