# -*- coding: utf-8 -*-
"""Reduce seed: substitute A0=2/K0, A1=-2K1/K0^2 into the seed equations."""
import pickle
import sympy as sp
from sympy import pi, sqrt, Rational

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P.items()}

K0, K1, K2 = sp.symbols('K0 K1 K2')
A0, A1, A2 = sp.symbols('A0 A1 A2')
B0, B1, B2 = sp.symbols('B0 B1 B2')
C0, C1, C2 = sp.symbols('C0 C1 C2')

def eq_coeff(name, n, Kex, Aex, Bex, Cex):
    tot = 0
    for (nm, m), coef in Pc.items():
        if nm != name:
            continue
        cc = sp.expand(coef.subs({K: Kex, A: Aex, B: Bex, C: Cex}) * u**m)
        c = cc.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)

# reduced substitutions
A0_sub = 2 / K0
A1_sub = -2 * K1 / K0**2

# After reduction, E1_0,E2_0,E6_3,E5_2 identically 0 (up to the A0K0-2 factor).
# E1_1 = 0 identically after A1_sub.

# Now check E6_5, E1_2, E2_2, E5_4, E5_5 with reduction.
Kex = K0 + K1*u + K2*u**2
Aex = A0_sub + A1_sub*u + A2*u**2
Bex = B0 + B1*u + B2*u**2
Cex = C0 + C1*u + C2*u**2

for name, n in [('E1', 2), ('E2', 2), ('E6', 5), ('E5', 4), ('E5', 5), ('E5', 6)]:
    e = eq_coeff(name, n, Kex, Aex, Bex, Cex)
    print('%s_%d =' % (name, n), sp.factor(sp.simplify(e)))
    print()
