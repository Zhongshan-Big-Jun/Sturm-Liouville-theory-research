# -*- coding: utf-8 -*-
"""Fast focused: verify that E5_5 and E1_3 at level 3 do NOT depend on B3 or
C3 (the B3,C3 columns vanish).  Series truncated to the minimal needed depth.
"""
import pickle
import sympy as sp

u = sp.symbols('u', positive=True)
K, A, B, Cv = sp.symbols('K A B C')
P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}

K0, K1, K2, K3 = sp.symbols('K0 K1 K2 K3')
A0, A1, A2, A3 = sp.symbols('A0 A1 A2 A3')
B0, B1, B2, B3 = sp.symbols('B0 B1 B2 B3')
C0, C1, C2, C3 = sp.symbols('C0 C1 C2 C3')

Kd = K0 + K1*u + K2*u**2 + K3*u**3
Ad = sp.expand(A0 + A1*u + A2*u**2 + A3*u**3).subs({A0: 2/K0, A1: -2*K1/K0**2})
Bd = B0 + B1*u + B2*u**2 + B3*u**3
Cd = C0 + C1*u + C2*u**2 + C3*u**3

def coeff_cleared(name, n):
    tot = 0
    for (nm, m), coef in P0.items():
        if nm != name or m > n:
            continue
        f = sp.expand(sp.expand((coef * K**DNAME[name]).subs(
            {K: Kd, A: Ad, B: Bd, Cv: Cd})) * u**m)
        c = f.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)

for (nm, n) in [('E5', 5), ('E1', 3), ('E2', 3), ('E6', 6)]:
    c = coeff_cleared(nm, n)
    print('%s_%d:' % (nm, n),
          '  dB3=%s' % (sp.simplify(sp.diff(c, B3)) != 0),
          '  dC3=%s' % (sp.simplify(sp.diff(c, C3)) != 0),
          '  dK3=%s' % (sp.simplify(sp.diff(c, K3)) != 0),
          '  dA3=%s' % (sp.simplify(sp.diff(c, A3)) != 0))
