# -*- coding: utf-8 -*-
"""Independent audit A3 (CORRECTED expansion): re-derive cascade levels
0,1,2 from scratch.  Care: expand AFTER multiplying by u**m so all u
powers distribute before taking coeff.
"""
import pickle
import sympy as sp
from sympy import pi, sqrt, Rational

u = sp.symbols('u', positive=True)
K, A, B, Cv = sp.symbols('K A B C')
P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P0.items()}

K0, K1, K2 = sp.symbols('K0 K1 K2')
A0, A1, A2 = sp.symbols('A0 A1 A2')
B0, B1, B2 = sp.symbols('B0 B1 B2')
C0, C1, C2 = sp.symbols('C0 C1 C2')


def coeff_cleared(name, n, Kd, Ad, Bd, Cd):
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


print('===== LEVEL 0 (K0,A0,B0,C0) =====')
e10 = coeff_cleared('E1', 0, K0, A0, B0, C0)
e20 = coeff_cleared('E2', 0, K0, A0, B0, C0)
e63 = coeff_cleared('E6', 3, K0, A0, B0, C0)
e52 = coeff_cleared('E5', 2, K0, A0, B0, C0)
print('E1_0 =', sp.factor(e10))
print('E2_0 =', sp.factor(e20))
print('E6_3 =', sp.factor(e63))
print('E5_2 =', sp.factor(e52))

# ---------- LEVEL 1 ----------
print('\n===== LEVEL 1 (K0,A0,B0,C0 fixed sym; K1,A1,B1,C1 free) =====')
Kd = K0 + K1*u
Ad = A0 + A1*u
Bd = B0 + B1*u
Cd = C0 + C1*u
e11 = coeff_cleared('E1', 1, Kd, Ad, Bd, Cd)
e21 = coeff_cleared('E2', 1, Kd, Ad, Bd, Cd)
e64 = coeff_cleared('E6', 4, Kd, Ad, Bd, Cd)
print('E1_1 =', sp.factor(e11))
print('E2_1 =', sp.factor(e21))
print('E6_4 =', sp.factor(e64))
print('E2_1*... under A0=2/K0:')
print('  E1_1[A0=2/K0] =', sp.factor(e11.subs({A0: 2/K0})))
print('  E6_4[A0=2/K0] =', sp.factor(e64.subs({A0: 2/K0})))
print('  E2_1[A0=2/K0] =', sp.factor(e21.subs({A0: 2/K0})))
print('Relation a1=-2K1/K0^2 i.e. A1 = -2K1/K0^2:')
print('  All three vanish iff A1*K0^2 + 2*K1 = 0 => A1 = -2 K1/K0^2')

# ---------- LEVEL 2 ----------
print('\n===== LEVEL 2 (reduced: A0=2/K0, A1=-2K1/K0^2) =====')
A0r = 2/K0
A1r = -2*K1/K0**2
Kd = K0 + K1*u + K2*u**2
Ad = A0r + A1r*u + A2*u**2
Bd = B0 + B1*u + B2*u**2
Cd = C0 + C1*u + C2*u**2
e12 = sp.cancel(coeff_cleared('E1', 2, Kd, Ad, Bd, Cd))
e22 = sp.cancel(coeff_cleared('E2', 2, Kd, Ad, Bd, Cd))
e65 = sp.cancel(coeff_cleared('E6', 5, Kd, Ad, Bd, Cd))
e54 = sp.cancel(coeff_cleared('E5', 4, Kd, Ad, Bd, Cd))
e55 = sp.cancel(coeff_cleared('E5', 5, Kd, Ad, Bd, Cd))
e56 = sp.cancel(coeff_cleared('E5', 6, Kd, Ad, Bd, Cd))
print('E1_2 =', e12)
print('E2_2 =', e22)
print('E6_5 =', e65)
print('E5_4 =', e54)
print('E5_5 =', e55)
print('E5_6 =', e56)

print('\n--- Affine-linearity checks in (A2,K2,C0) for E1_2,E2_2,E6_5 ---')
for nm, e, tags in [('E1_2', e12, ['A2', 'K2', 'C0']),
                    ('E2_2', e22, ['A2', 'K2', 'C0']),
                    ('E6_5', e65, ['A2', 'K2', 'C0'])]:
    # linear means second partial in each variable is constant 0
    dA2 = sp.simplify(sp.diff(sp.diff(e, A2), A2))
    dK2 = sp.simplify(sp.diff(sp.diff(e, K2), K2))
    dC0 = sp.simplify(sp.diff(sp.diff(e, C0), C0))
    dA2K2 = sp.simplify(sp.diff(sp.diff(e, A2), K2))
    print('%s: d2/dA2^2=%s, d2/dK2^2=%s, d2/dC0^2=%s, d2/dA2dK2=%s'
          % (nm, dA2 != 0, dK2 != 0, dC0 != 0, dA2K2 != 0))

print('\n--- b0,b1 first appear at E5_6? check E1_2..E5_5 for B0,B1 dependence ---')
for nm, e in [('E1_2', e12), ('E2_2', e22), ('E6_5', e65), ('E5_4', e54), ('E5_5', e55)]:
    dep_B0 = sp.simplify(sp.diff(e, B0)) != 0
    dep_B1 = sp.simplify(sp.diff(e, B1)) != 0
    print('%s: depends on B0? %s  B1? %s' % (nm, dep_B0, dep_B1))
print('E5_6: depends on B0?', sp.simplify(sp.diff(e56, B0)) != 0)

print('\n--- hard constant in E5_5 ---')
# E5_5 after reduction: quadratic/linear in K1,C1? We want the constant term
# when K1=C1=0.
e55c = sp.simplify(sp.cancel(e55.subs({K1: 0, C1: 0})))
print('E5_5[K1=0,C1=0] =', e55c)
print('compare K0^3/2 =', sp.simplify(K0**3/2))
print('E5_5[K1=0,C1=0] - K0^3/2 =', sp.simplify(sp.cancel(e55c - K0**3/2)))
# But note: at the even-only seed A0*K0 must = 2 AND this is K-cleared.
# The point is E5_5 carries a hard constant that cannot vanish when K1=C1=0
# GIVEN A0=2/K0 (level0). Check whether with A0=2/K0 the E5_5 constant is K0^3/2.
print('\nE5_5 full reduced =', e55)
