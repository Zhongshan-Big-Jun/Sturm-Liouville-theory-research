# -*- coding: utf-8 -*-
"""R-209 M3 STRICT cascade: full integer-power branch of E1=E2=E5=E6=0.

u = R^(-1/6); k2 = K u, k3 = K u + C u^5, p1 = pi/2 + a u^2,
p3 = pi/4 + b u^2, eps = u^3.  K, a, b, c are full power series in u.

Equations pre-cleared of K denominators (K>0 on the branch): E1(x1),
E2(xK^2), E5(xK^5), E6(xK).  Level j (handoff): unknowns (K_j,a_j,b_j,c_j),
equations E1_j, E2_j, E5_{j+2}, E6_{j+3}.

Realization: at each level substitute the exact solved lower coefficients,
treat the current level's 4 unknowns symbolically, the higher ones as 0, and
take the truncated power-dict coefficient.  The seed (levels 0-2) is
nonlinear; every later level is affine in the 4 unknowns and solved exactly.

All arithmetic exact (sympy); pi symbolic.
"""
import pickle
import sympy as sp
from sympy import pi, Rational, sqrt

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')

P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P.items()}

ND = 9
Ks = [sp.symbols('K%d' % j) for j in range(ND + 1)]
As = [sp.symbols('A%d' % j) for j in range(ND + 1)]
Bs = [sp.symbols('B%d' % j) for j in range(ND + 1)]
Cs = [sp.symbols('C%d' % j) for j in range(ND + 1)]


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


def poly_ser(coef, Kd, Ad, Bd, Cd, nmax):
    poly = sp.Poly(coef, K, A, B, C)
    Kpow = {n: spow(Kd, n, nmax) for n in range(poly.degree(K) + 1)}
    Apow = {n: spow(Ad, n, nmax) for n in range(poly.degree(A) + 1)}
    Bpow = {n: spow(Bd, n, nmax) for n in range(poly.degree(B) + 1)}
    Cpow = {n: spow(Cd, n, nmax) for n in range(poly.degree(C) + 1)}
    acc = {}
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


solv = {}


def record(name, j, val):
    val = sp.nsimplify(val)
    solv[sp.symbols(name + str(j))] = val
    return val


def series_dicts(j, nmax):
    """Return Kd/Ad/Bd/Cd: solved value for idx<j, symbolic at idx=j, 0 for idx>j."""
    def mk(symlist):
        d = {}
        for n in range(nmax + 1):
            sym = symlist[n]
            if sym in solv:
                d[n] = solv[sym]
            elif n == j:
                d[n] = sym
            else:
                d[n] = 0
        return d
    return mk(Ks), mk(As), mk(Bs), mk(Cs)


def level_eq(name, n, j, Kd, Ad, Bd, Cd, nmax):
    """Coefficient of u^n in pre-cleared equation 'name' at level j."""
    tot = {}
    for (nm, m), coef in Pc.items():
        if nm != name or m > n:
            continue
        ser = poly_ser(coef, Kd, Ad, Bd, Cd, nmax)
        # contribution to u^n: ser degree (n-m)
        want = n - m
        if want in ser:
            tot[want] = tot.get(want, 0) + ser[want]
    return sp.expand(sum(tot.values()))


def solved_series(nmax):
    Kd = {n: (solv.get(Ks[n], 0)) for n in range(nmax + 1)}
    Ad = {n: (solv.get(As[n], 0)) for n in range(nmax + 1)}
    Bd = {n: (solv.get(Bs[n], 0)) for n in range(nmax + 1)}
    Cd = {n: (solv.get(Cs[n], 0)) for n in range(nmax + 1)}
    return Kd, Ad, Bd, Cd


# =========================================================================
# LEVELS 0,1,2: nonlinear seed.
# =========================================================================
# Level 0 equations: E1_0 (u0), E2_0 (u0), E5_2 (u2), E6_3 (u3).
j = 0
Kd, Ad, Bd, Cd = series_dicts(j, 4)
print('E1_0 =', sp.factor(level_eq('E1', 0, j, Kd, Ad, Bd, Cd, 2)))
print('E2_0 =', sp.factor(level_eq('E2', 0, j, Kd, Ad, Bd, Cd, 2)))
print('E5_2 =', sp.factor(level_eq('E5', 2, j, Kd, Ad, Bd, Cd, 3)))
print('E6_3 =', sp.factor(level_eq('E6', 3, j, Kd, Ad, Bd, Cd, 3)))
print()

# Level 1: unknowns K1,A1,B1,C1.  Equations E1_1 (u1), E2_1 (u1), E5_3 (u3),
# E6_4 (u4).
j = 1
Kd, Ad, Bd, Cd = series_dicts(j, 6)
print('E1_1 =', sp.factor(level_eq('E1', 1, j, Kd, Ad, Bd, Cd, 4)))
print('E2_1 =', sp.factor(level_eq('E2', 1, j, Kd, Ad, Bd, Cd, 4)))
print('E5_3 =', sp.factor(level_eq('E5', 3, j, Kd, Ad, Bd, Cd, 4)))
print('E6_4 =', sp.factor(level_eq('E6', 4, j, Kd, Ad, Bd, Cd, 4)))
print()

# Level 2: unknowns K2,A2,B2,C2.  Equations E1_2 (u2), E2_2 (u2), E5_4 (u4),
# E6_5 (u5).
j = 2
Kd, Ad, Bd, Cd = series_dicts(j, 7)
print('E1_2 =', sp.factor(level_eq('E1', 2, j, Kd, Ad, Bd, Cd, 5)))
print('E2_2 =', sp.factor(level_eq('E2', 2, j, Kd, Ad, Bd, Cd, 5)))
print('E5_4 =', sp.factor(level_eq('E5', 4, j, Kd, Ad, Bd, Cd, 5)))
print('E6_5 =', sp.factor(level_eq('E6', 5, j, Kd, Ad, Bd, Cd, 5)))
