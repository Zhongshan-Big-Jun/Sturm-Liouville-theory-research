# -*- coding: utf-8 -*-
"""Investigate E6_7/E6_9 discrepancy: compare pickle vs my from-scratch E6
terms term-by-term, and validate EACH against exact closed.py numeric E6 with
lowered u for the tail."""
import pickle, sys, math
import numpy as np
import sympy as sp
from sympy import pi

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')
P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))

print('Pickle E6_7 =', sp.expand(P0[('E6', 7)]))
print()
print('Pickle E6_9 =', sp.expand(P0[('E6', 9)]))

# Rebuild my E6_7, E6_9 from scratch (same construction as audit a1a2)
Nmax = 10
eps_val = u**3
k2 = K*u
k3 = K*u + C*u**5
p1 = pi/2 + A*u**2
p3 = pi/4 + B*u**2
fac = 1 + C*u**4/K
p1t = p1*fac
p3t = p3*fac
p2 = k2/2 - eps_val*(p1 + p3)
p2t = k3/2 - eps_val*fac*(p1 + p3)

def to_dict(expr, nmax):
    e = sp.expand(sp.series(sp.expand(expr), u, 0, nmax + 1).removeO())
    out = {}
    for m in range(0, nmax + 1):
        c = e.coeff(u, m)
        if c != 0:
            out[m] = sp.simplify(sp.expand(c))
    return out

def mul(A, B, nmax):
    out = {}
    for m1, c1 in A.items():
        for m2, c2 in B.items():
            m = m1 + m2
            if m <= nmax:
                out[m] = out.get(m, 0) + c1*c2
    return {m: sp.simplify(c) for m, c in out.items() if c != 0}

def mk(x):
    return {m: c*u**m for m, c in x.items()}

# cot(p1t) = cos/sin expanded; compare direct approach
s_cos_p1t = to_dict(sp.cos(mk(p1t)), 8) if False else to_dict(sp.cos(p1t), 8)
s_sin_p1t = to_dict(sp.sin(p1t), 8)
s_cos_p2 = to_dict(sp.cos(p2), Nmax)
s_sin_p2 = to_dict(sp.sin(p2), Nmax)
s_cos_p2t = to_dict(sp.cos(p2t), Nmax)
s_sin_p2t = to_dict(sp.sin(p2t), Nmax)
s_sin_p1 = to_dict(sp.sin(p1), 8)
s_cos_p1 = to_dict(sp.cos(p1), 8)

# cot(p1t): -tan(p1t-pi/2)  (solver method)
cot1 = to_dict(-sp.tan(p1t - pi/2), 8)
# alternative: cos(p1t)/sin(p1t)
cot2 = to_dict(sp.cos(p1t)/sp.sin(p1t), 8)
print('\ncot method1 (-tan(p1t-pi/2)) == cot method2 (cos/sin)?',
      all(sp.simplify(cot1.get(m,0)-cot2.get(m,0)) == 0 for m in set(cot1)|set(cot2)))

u3 = {3: sp.Integer(1)}
t6a = mul(u3, s_cos_p2t, Nmax)
t6b = mul(s_sin_p2t, cot1, Nmax)
t6 = mul(s_sin_p1, {m: t6a.get(m, 0) + t6b.get(m, 0) for m in set(t6a) | set(t6b)}, Nmax)
t6c = mul(mul(u3, s_cos_p2, Nmax), s_sin_p1, Nmax)
t6d = mul(s_sin_p2, s_cos_p1, Nmax)
E6mine = {m: t6.get(m, 0) + t6c.get(m, 0) + t6d.get(m, 0) for m in set(t6) | set(t6c) | set(t6d)}
E6mine = {m: sp.simplify(c) for m, c in E6mine.items() if c != 0}

for m in [3, 5, 7, 9]:
    m1 = sp.expand(E6mine.get(m, 0))
    pk = sp.expand(P0[('E6', m)])
    print('\nE6_%d: diff(pickle - mine) =' % m, sp.simplify(pk - m1))
