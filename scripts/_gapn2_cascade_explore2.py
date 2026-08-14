# -*- coding: utf-8 -*-
"""Temporary: use the truncated power-dict machinery of _gapn2_largeR_full.py
to build Sys[(name, n)] = coefficient of u^n, then inspect levels. STRICT.
"""
import sys
sys.path.insert(0, r'scripts')
import pickle
import sympy as sp
from _gapn2_largeR_full import loadP, build_system

u = sp.symbols('u', positive=True)

P = loadP()
unk = sp.symbols('K0 K1 K2 K3 K4 K5 K6 K7 K8 A0 A1 A2 A3 A4 A5 A6 A7 A8 B0 B1 B2 B3 B4 B5 B6 C0 C1 C2 C3 C4 C5 C6')
Sys, Q = build_system(P, unk, nmax=8)

print('Sys keys:', sorted(Sys.keys()))
print()
for j in range(0, 6):
    print('--- LEVEL j = %d ---' % j)
    for name, n in [('E1', j), ('E2', j), ('E5', j + 2), ('E6', j + 3)]:
        e = Sys.get((name, n), 0)
        if e != 0:
            print('%s_%d =' % (name, n))
            print('   ', sp.simplify(e))
    print()
