# -*- coding: utf-8 -*-
"""Print reduced E1_2, E6_5, E5_5 exactly (truncated power-dict) and compare
against the full-subs derivation of _gapn2_cascade_reduce.py."""
import pickle
import sympy as sp
from sympy import pi

K, A, B, C = sp.symbols('K A B C')
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P.items()}


def smul(X, Y, nmax):
    o = {}
    for i, cx in X.items():
        for j, cy in Y.items():
            m = i + j
            if m <= nmax:
                o[m] = o.get(m, 0) + cx * cy
    return o


def spow(X, n, nmax):
    if n == 0:
        return {0: sp.Integer(1)}
    o = spow(X, n // 2, nmax)
    o = smul(o, o, nmax)
    if n % 2 == 1:
        o = smul(o, X, nmax)
    return o


def eq_coeff(name, n, Kd, Ad, Bd, Cd):
    acc = {}
    for (nm, m), coef in Pc.items():
        if nm != name or m > n:
            continue
        want = n - m
        poly = sp.Poly(coef, K, A, B, C)
        Kpow = {dd: spow(Kd, dd, n) for dd in range(poly.degree(K) + 1)}
        Apow = {dd: spow(Ad, dd, n) for dd in range(poly.degree(A) + 1)}
        Bpow = {dd: spow(Bd, dd, n) for dd in range(poly.degree(B) + 1)}
        Cpow = {dd: spow(Cd, dd, n) for dd in range(poly.degree(C) + 1)}
        for mon, cmon in zip(poly.monoms(), poly.coeffs()):
            s = {0: cmon}
            if mon[0]:
                s = smul(s, Kpow[mon[0]], n)
            if mon[1]:
                s = smul(s, Apow[mon[1]], n)
            if mon[2]:
                s = smul(s, Bpow[mon[2]], n)
            if mon[3]:
                s = smul(s, Cpow[mon[3]], n)
            for w in s:
                acc[w] = acc.get(w, 0) + s[w]
    return sp.expand(acc.get(want, 0))


K0, K1, K2, K3, K4 = sp.symbols('K0 K1 K2 K3 K4')
B0, B1, B2, B3, B4 = sp.symbols('B0 B1 B2 B3 B4')
C0, C1, C2, C3, C4 = sp.symbols('C0 C1 C2 C3 C4')
A2, A3, A4, A5 = sp.symbols('A2 A3 A4 A5')

Kd = {0: K0, 1: K1, 2: K2, 3: K3, 4: K4}
Bd = {0: B0, 1: B1, 2: B2, 3: B3, 4: B4}
Cd = {0: C0, 1: C1, 2: C2, 3: C3, 4: C4}
Ad = {2: A2, 3: A3, 4: A4, 5: A5, 0: 2 / K0, 1: -2 * K1 / K0**2}

e = sp.together(eq_coeff('E1', 2, Kd, Ad, Bd, Cd))
e = sp.expand(e * K0**3)
print('E1_2 (power-dict, cleared):')
print(sp.factor(e))
print()
e6 = sp.together(eq_coeff('E6', 5, Kd, Ad, Bd, Cd))
e6 = sp.expand(e6 * K0**2)
print('E6_5 (power-dict, cleared):')
print(sp.factor(e6))
