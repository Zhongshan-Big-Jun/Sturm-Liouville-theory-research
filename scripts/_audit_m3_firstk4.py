# -*- coding: utf-8 -*-
"""Efficient: first appearance of K4 and A4 in E1 (even-only raw orders),
using shallow series.  Also where B2 appears (should be >=4 due to u^2 offset).
"""
import pickle
import sympy as sp

u = sp.symbols('u', positive=True)
K, A, B, Cv = sp.symbols('K A B C')
P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}

K0, K1, K2, K3, K4 = sp.symbols('K0 K1 K2 K3 K4')
A0, A1, A2, A3, A4 = sp.symbols('A0 A1 A2 A3 A4')
B0, B1, B2 = sp.symbols('B0 B1 B2')
C0, C1, C2 = sp.symbols('C0 C1 C2')

Kd = K0 + K1*u + K2*u**2 + K3*u**3 + K4*u**4
Ad = sp.expand(A0 + A1*u + A2*u**2 + A3*u**3 + A4*u**4).subs({A0: 2/K0, A1: -2*K1/K0**2})
Bd = B0 + B1*u + B2*u**2
Cd = C0 + C1*u + C2*u**2

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

for lab, var in [('K4', K4), ('A4', A4), ('B2', B2)]:
    for nm in ['E1', 'E2', 'E5', 'E6']:
        first = None
        for n in range(0, 9):
            if sp.simplify(sp.diff(coeff_cleared(nm, n), var)) != 0:
                first = n
                break
        print('%s first in %s at order' % (lab, nm), first)
