# -*- coding: utf-8 -*-
"""Diagnostic v2: level-by-level with solved-values substitution (fast)."""
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

# substitute a numeric probe for every coefficient to check linearity/structure
probe = {}
for j in range(ND + 1):
    probe[Ks[j]] = sp.symbols('k%d' % j)
    probe[As[j]] = sp.symbols('a%d' % j)
    probe[Bs[j]] = sp.symbols('b%d' % j)
    probe[Cs[j]] = sp.symbols('c%d' % j)


def eq_coeff(name, n, sub):
    """sub = dict mapping every Ks/As/Bs/Cs symbol to a VALUE (exact), plus u
    handled separately.  Only include series terms up to degree n."""
    deg = n + 1
    Kex = sum(sub[Ks[j]] * u**j for j in range(deg))
    Aex = sum(sub[As[j]] * u**j for j in range(deg))
    Bex = sum(sub[Bs[j]] * u**j for j in range(deg))
    Cex = sum(sub[Cs[j]] * u**j for j in range(deg))
    tot = 0
    for (nm, m), coef in Pc.items():
        if nm != name:
            continue
        cc = sp.expand((coef.subs({K: Kex, A: Aex, B: Bex, C: Cex})) * u**m)
        c = cc.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)


# Level 0: which unknowns appear in E1_0, E2_0, E5_2, E6_3
for j in range(0, 6):
    print('=== LEVEL j=%d ===' % j)
    # subs: lower indices -> symbolic marker (already solved conceptually), current -> marker too
    for name, n in [('E1', j), ('E2', j), ('E5', j + 2), ('E6', j + 3)]:
        e = eq_coeff(name, n, probe)
        # which unknowns (among ALL levels) appear
        present = sorted(set(str(v) for v in probe.values() if e.has(v)))
        # restrict to current level j
        cursym = ['k%d' % j, 'a%d' % j, 'b%d' % j, 'c%d' % j]
        curl = [s for s in cursym if e.has(sp.symbols(s))]
        print('  %s_%d: current-level=%s total-syms=%d' % (name, n, curl, len(present)))
