# -*- coding: utf-8 -*-
"""Diagnostic: for each level j, print which of the 4 current-level unknowns
appear in the 4 level equations, and the degree (linear?) in them."""
import pickle
import sympy as sp
from sympy import pi

ND = 9
u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P.items()}

Ks = [sp.symbols('K%d' % j) for j in range(ND + 1)]
As = [sp.symbols('A%d' % j) for j in range(ND + 1)]
Bs = [sp.symbols('B%d' % j) for j in range(ND + 1)]
Cs = [sp.symbols('C%d' % j) for j in range(ND + 1)]
allv = Ks + As + Bs + Cs


def eq_coeff(name, n, deg):
    tot = 0
    for (nm, m), coef in Pc.items():
        if nm != name:
            continue
        cc = sp.expand((coef.subs({K: sum(Ks[j]*u**j for j in range(deg)),
                                   A: sum(As[j]*u**j for j in range(deg)),
                                   B: sum(Bs[j]*u**j for j in range(deg)),
                                   C: sum(Cs[j]*u**j for j in range(deg))})) * u**m)
        c = cc.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)


# At level j, current unknowns are K_j,A_j,B_j,C_j (j from 0..ND)
for j in range(0, 5):
    cur = [Ks[j], As[j], Bs[j], Cs[j]]
    print('=== LEVEL j=%d ===' % j)
    for name, n in [('E1', j), ('E2', j), ('E5', j + 2), ('E6', j + 3)]:
        e = eq_coeff(name, n, min(n + 2, ND + 1))
        # degree in the current unknowns
        degs = []
        for v in cur:
            p = sp.Poly(e, v)
            degs.append('%s^%d' % (v, p.degree(v)))
        # which current unknowns actually appear
        present = [str(v) for v in cur if e.has(v)]
        # total degree if linear?
        print('  %s_%d: current unknowns present=%s; degs=%s' % (name, n, present, degs))
