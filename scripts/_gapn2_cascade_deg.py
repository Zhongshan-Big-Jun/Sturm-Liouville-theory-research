# -*- coding: utf-8 -*-
"""Inspect max degrees of P coefficients in K,A,B,C and time build steps."""
import pickle
import sympy as sp
import time

K, A, B, C = sp.symbols('K A B C')
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))

degK, degA, degB, degC = [], [], [], []
for (name, m), coef in P.items():
    poly = sp.Poly(coef, K, A, B, C)
    degK.append(poly.degree(K))
    degA.append(poly.degree(A))
    degB.append(poly.degree(B))
    degC.append(poly.degree(C))
print('Kmax=%d Amax=%d Bmax=%d Cmax=%d' % (max(degK), max(degA), max(degB), max(degC)))
print('total monomials per P entry (top few):')
for (name, m), coef in sorted(P.items()):
    poly = sp.Poly(coef, K, A, B, C)
    print('  %s_%d: monoms=%d Kdeg=%d Adeg=%d Bdeg=%d Cdeg=%d'
          % (name, m, len(poly.monoms()), poly.degree(K), poly.degree(A), poly.degree(B), poly.degree(C)))
