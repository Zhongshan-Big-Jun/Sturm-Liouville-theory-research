# -*- coding: utf-8 -*-
"""Determine where B3,C3 (and B1,C1) first appear, cheaply.  We only need the
LEVEL-3 and LEVEL-4 equations and the presence of the relevant unknowns.
Shallower series (through u^3 for both) to keep it fast; presence of a level-3
unknown in a level-4 equation is captured by the leading terms.
"""
import pickle
import sympy as sp
from sympy import pi, sqrt

u = sp.symbols('u', positive=True)
K, A, B, Cv = sp.symbols('K A B C')
P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P0.items()}

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

# Which level-3 unknowns appear in the level-3 equations E1_3,E2_3,E5_5,E6_6
# and in the level-4 equations E1_4,E2_4,E5_6,E6_7?
unk_at = {0: {'K': K0, 'A': A0, 'B': B0, 'C': C0},
          1: {'K': K1, 'A': A1, 'B': B1, 'C': C1},
          2: {'K': K2, 'A': A2, 'B': B2, 'C': C2},
          3: {'K': K3, 'A': A3, 'B': B3, 'C': C3}}

for j in [3, 4]:
    eqs = [('E1', j), ('E2', j), ('E5', j + 2), ('E6', j + 3)]
    line = []
    for (nm, n) in eqs:
        c = coeff_cleared(nm, n)
        present = ''
        for lab in ['K', 'A', 'B', 'C']:
            vl = unk_at[j][lab] if j in unk_at else None
            if vl is not None and sp.simplify(sp.diff(c, vl)) != 0:
                present += lab
            else:
                present += 'x'
        line.append('%s_%d:%s' % (nm, n, present))
    print('level-%d equations, level-%d unknown (K,A,B,C):' % (j, j))
    print('  ', '  '.join(line))
