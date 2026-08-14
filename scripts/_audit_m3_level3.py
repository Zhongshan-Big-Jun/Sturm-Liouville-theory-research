# -*- coding: utf-8 -*-
"""Independent audit A3 (level j=3): form the 4x4 coefficient matrix of the
level-3 equations (E1_3, E2_3, E5_5, E6_6) in the level-3 unknowns
(K3,A3,B3,C3), verify affine linearity, and test nonsingularity.
Lower levels: A0=2/K0, A1=-2*K1/K0^2 (exact STRICT identities); K1,K2,A2,
B0,B1,B2,C0,C1,C2 free symbols.  The level-3 matrix must be independent of the
level-3 unknowns; its determinant is tested at representative lower values.
Note: the even-only seed (K1=0) is excluded because E5_5 would not vanish.
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

A0r = 2/K0
A1r = -2*K1/K0**2

# Level-3 series: lower solved (A0=A0r, A1=A1r), level-3 unknown at index 3.
Kd = K0 + K1*u + K2*u**2 + K3*u**3
Ad = A0r + A1r*u + A2*u**2 + A3*u**3
Bd = B0 + B1*u + B2*u**2 + B3*u**3
Cd = C0 + C1*u + C2*u**2 + C3*u**3


def coeff_cleared(name, n, Ks, As, Bs, Cs):
    tot = 0
    for (nm, m), coef in P0.items():
        if nm != name or m > n:
            continue
        f = sp.expand(sp.expand((coef * K**DNAME[name]).subs(
            {K: Ks, A: As, B: Bs, Cv: Cs})) * u**m)
        c = f.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)


f1 = coeff_cleared('E1', 3, Kd, Ad, Bd, Cd)
f2 = coeff_cleared('E2', 3, Kd, Ad, Bd, Cd)
f5 = coeff_cleared('E5', 5, Kd, Ad, Bd, Cd)
f6 = coeff_cleared('E6', 6, Kd, Ad, Bd, Cd)

# Verify affine in (K3,A3,B3,C3): second derivatives zero
print('affine checks (second derivatives in level-3 vars):')
for nm, e in [('E1_3', f1), ('E2_3', f2), ('E5_5', f5), ('E6_6', f6)]:
    deps = []
    for v in [K3, A3, B3, C3]:
        if sp.simplify(sp.diff(sp.diff(e, v), v)) != 0:
            deps.append('d2/d%s^2!=0' % v)
    for v1, v2 in [(K3, A3), (K3, B3), (K3, C3), (A3, B3), (A3, C3), (B3, C3)]:
        if sp.simplify(sp.diff(sp.diff(e, v1), v2)) != 0:
            deps.append('d2/d%s d%s!=0' % (v1, v2))
    print('  %s nonlinear terms: %s' % (nm, deps if deps else 'none (affine)'))

# Build matrix M3 = d(f1,f2,f5,f6)/d(K3,A3,B3,C3)
funs = [f1, f2, f5, f6]
vars3 = [K3, A3, B3, C3]
M = sp.zeros(4, 4)
for i, e in enumerate(funs):
    for j, v in enumerate(vars3):
        M[i, j] = sp.simplify(sp.diff(e, v))
print('\n4x4 level-3 coefficient matrix M3 (symbolic lower levels):')
sp.pprint(M)

detM = sp.factor(sp.simplify(M.det()))
print('\ndet(M3) (symbolic) =', detM)

# Nonsingularity test at representative lower values consistent with the seed.
# Use the EVIDENCE limits: K0~3.4553.  Odd components are required nonzero, so
# take K1 e.g. 0.1 (generic); other lowers at generic near-fit values.
val = {K0: 3.4553, K1: 0.1, K2: 2.9, A2: -0.6, B0: 0.29, B1: 0.05, B2: -0.47,
       C0: 1.474, C1: 0.1, C2: 3.4}
Mnum = M.subs(val)
detMnum = sp.N(Mnum.det(), 30)
print('\ndet(M3) numeric at representative lowers =', detMnum)
print('Nonsingular?', abs(detMnum) > 1e-20)
print('Matrix numeric:')
sp.pprint(Mnum.applyfunc(lambda x: sp.N(x, 6)))

# Also test robustness: scan K1 in a small range, K0 held, others generic
import numpy as np
non_sing = True
for K1v in [0.001, 0.01, 0.1, 0.5, 1.0, 2.0]:
    vv = dict(val); vv[K1] = K1v
    d = sp.N(M.subs(vv).det(), 20)
    if abs(d) < 1e-15:
        non_sing = False
        print('det(M3) SMALL at K1=%g: %g' % (K1v, d))
print('M3 nonsingular across K1 scan:', non_sing)
