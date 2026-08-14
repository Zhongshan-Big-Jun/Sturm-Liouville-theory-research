# -*- coding: utf-8 -*-
"""Joint seed system: all 12 unknowns (K0..K2, A0..A2, B0..B2, C0..C2)
symbolic simultaneously.  Extract the seed equations at orders up to 5."""
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

# series up to u^2 for each
Kex = K0 + K1*u + K2*u**2
Aex = A0 + A1*u + A2*u**2
Bex = B0 + B1*u + B2*u**2
Cex = C0 + C1*u + C2*u**2


def eq_coeff(name, n):
    tot = 0
    for (nm, m), coef in Pc.items():
        if nm != name:
            continue
        cc = sp.expand(coef.subs({K: Kex, A: Aex, B: Bex, C: Cex}) * u**m)
        c = cc.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)


order_map = {'E1': [0, 1, 2], 'E2': [0, 1, 2], 'E5': [2, 3, 4, 5], 'E6': [3, 4, 5]}
eqs = []
for name, orders in order_map.items():
    for n in orders:
        e = eq_coeff(name, n)
        e = sp.factor(e)
        eqs.append((name, n, e))
        print('%s_%d =' % (name, n), e)
        print()
