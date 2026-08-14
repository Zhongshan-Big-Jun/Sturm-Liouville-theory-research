# -*- coding: utf-8 -*-
"""Timing test: per-level truncated series substitution with concrete lower
values.  Check how long ONE level costs using power-dict truncation."""
import pickle
import sympy as sp
from sympy import pi
import time

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P.items()}


def smul(X, Y, nmax):
    out = {}
    for i, cx in X.items():
        for j, cy in Y.items():
            m = i + j
            if m <= nmax:
                out[m] = out.get(m, 0) + cx * cy
    return out


def spow(X, n, nmax):
    if n == 0:
        return {0: sp.Integer(1)}
    out = spow(X, n // 2, nmax)
    out = smul(out, out, nmax)
    if n % 2 == 1:
        out = smul(out, X, nmax)
    return out


def poly_to_series(coef, Ks, As, Bs, Cs, nmax):
    """coef = polynomial in K,A,B,C.  Substitute truncated series dicts {degree:coeff}
    and return dict degree->coeff of the result, truncated to nmax."""
    # find degrees
    num = coef
    # expand as polynomial monomials
    poly = sp.Poly(num, K, A, B, C)
    acc = {}
    Kmax = poly.degree(K)
    Amax = poly.degree(A)
    Bmax = poly.degree(B)
    Cmax = poly.degree(C)
    Kpow = {n: spow(Ks, n, nmax) for n in range(Kmax + 1)}
    Apow = {n: spow(As, n, nmax) for n in range(Amax + 1)}
    Bpow = {n: spow(Bs, n, nmax) for n in range(Bmax + 1)}
    Cpow = {n: spow(Cs, n, nmax) for n in range(Cmax + 1)}
    for mon, cmon in zip(poly.monoms(), poly.coeffs()):
        s = {0: cmon}
        if mon[0]:
            s = smul(s, Kpow[mon[0]], nmax)
        if mon[1]:
            s = smul(s, Apow[mon[1]], nmax)
        if mon[2]:
            s = smul(s, Bpow[mon[2]], nmax)
        if mon[3]:
            s = smul(s, Cpow[mon[3]], nmax)
        for m, c in s.items():
            acc[m] = acc.get(m, 0) + c
    return acc


# level j=1 test: build series with K0..: use probe numeric rationals for lower,
# symbolic only for level j
ND = 9
Ks = [sp.symbols('K%d' % j) for j in range(ND + 1)]
As = [sp.symbols('A%d' % j) for j in range(ND + 1)]
Bs = [sp.symbols('B%d' % j) for j in range(ND + 1)]
Cs = [sp.symbols('C%d' % j) for j in range(ND + 1)]

# fake solved lower values (small rationals)
solved = {}
for j in range(0, 2):
    solved[Ks[j]] = sp.Rational(7, 2) if j == 0 else sp.Rational(1, 5)
    solved[As[j]] = sp.Rational(4, 7) if j == 0 else sp.Rational(1, 9)
    solved[Bs[j]] = sp.Rational(1, 4) if j == 0 else sp.Rational(1, 11)
    solved[Cs[j]] = sp.Rational(3, 2) if j == 0 else sp.Rational(1, 13)

# series dicts: index -> expression (solved value for j'<j, symbolic for j'=j, 0 above)
j = 2
Kd = {n: (solved.get(Ks[n], (Ks[n] if n == j else 0))) for n in range(ND + 1)}
Ad = {n: (solved.get(As[n], (As[n] if n == j else 0))) for n in range(ND + 1)}
Bd = {n: (solved.get(Bs[n], (Bs[n] if n == j else 0))) for n in range(ND + 1)}
Cd = {n: (solved.get(Cs[n], (Cs[n] if n == j else 0))) for n in range(ND + 1)}

# trim to nmax
nmax = j + 2
Kd = {n: v for n, v in Kd.items() if n <= nmax}
Ad = {n: v for n, v in Ad.items() if n <= nmax}
Bd = {n: v for n, v in Bd.items() if n <= nmax}
Cd = {n: v for n, v in Cd.items() if n <= nmax}

t0 = time.time()
for (name, m), coef in Pc.items():
    if name != 'E1':
        continue
    ser = poly_to_series(coef, Kd, Ad, Bd, Cd, nmax)
    break
t1 = time.time()
print('one E1 coefficient (E1_10 likely) took %.2f s' % (t1 - t0))
print('E1_2 coefficient:', ser.get(2))
