# -*- coding: utf-8 -*-
"""Find the power-dict eq_coeff bug by comparing it to the unambiguous
full-substitution at low order."""
import pickle
import sympy as sp
from sympy import pi

K, A, B, C = sp.symbols('K A B C')
u = sp.symbols('u', positive=True)
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P.items()}

K0, K1, K2 = sp.symbols('K0 K1 K2')
A2, A3, A4 = sp.symbols('A2 A3 A4')
B0, C0 = sp.symbols('B0 C0')

# FULL substitution (unambiguous)
Kex = K0 + K1 * u + K2 * u**2
Aex = (2 / K0) + (-2 * K1 / K0**2) * u + A2 * u**2
Bex = B0
Cex = C0
full = 0
for (nm, m), coef in Pc.items():
    if nm != 'E1':
        continue
    cc = sp.expand(coef.subs({K: Kex, A: Aex, B: Bex, C: Cex}) * u**m)
    full += cc
full2 = sp.expand(full.coeff(u, 2))


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


Kd = {0: K0, 1: K1, 2: K2}
Ad = {0: 2 / K0, 1: -2 * K1 / K0**2, 2: A2}
Bd = {0: B0}
Cd = {0: C0}


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
    return acc  # return full dict for inspection


acc = eq_coeff('E1', 2, Kd, Ad, Bd, Cd)
print('power-dict acc keys:', sorted(acc.keys()))
pd2 = acc.get(2, 0)
print('power-dict u^2 =', sp.expand(sp.together(pd2)))
print()
print('full-subs  u^2 =', sp.expand(sp.together(full2)))
print()
print('difference =', sp.simplify(sp.expand(pd2) - sp.expand(full2)))
