# -*- coding: utf-8 -*-
"""Find K-denominator degrees per equation and pre-clear them."""
import pickle
import sympy as sp

K, A, B, C = sp.symbols('K A B C')
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))

for name in ['E1', 'E2', 'E5', 'E6']:
    maxden = 0
    for (nm, m), coef in P.items():
        if nm != name:
            continue
        num, den = sp.fraction(sp.together(coef))
        # degree of den in K
        if den == 1:
            d = 0
        else:
            d = sp.Poly(den, K).degree()
        maxden = max(maxden, d)
    print(name, 'max K-denominator degree =', maxden)
