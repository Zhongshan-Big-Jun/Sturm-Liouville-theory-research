# -*- coding: utf-8 -*-
"""Reduced-seed solve: enforce A0=2/K0, A1=-2 K1/K0^2 exactly, solve the
reduced system in (K0,K1,B0,C0,K2,A2,C1,B1,...) via least_squares on the
EXACT pre-cleared equations.  Physical branch only (seed K0~3.46).
"""
import pickle
import numpy as np
import sympy as sp
from sympy import pi, sqrt
from scipy.optimize import least_squares

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P.items()}

NR = 8  # series through u^8


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


# parameterization: full series dicts built from a flat vector of coefficients.
# order of unknowns: K0,K1,K2,K3,K4 (5), B0,B1,B2,B3,B4 (5), C0,C1,C2,C3,C4 (5),
# A2,A3,A4,A5 (4), A0,A1 fixed by identities. total 19 unknowns.
def build_dicts(z):
    # K, A, B, C series dicts
    Kd = {j: 0 for j in range(NR + 1)}
    Bd = {j: 0 for j in range(NR + 1)}
    Cd = {j: 0 for j in range(NR + 1)}
    Ad = {j: 0 for j in range(NR + 1)}
    # z layout
    Kd[0] = z[0]
    Bd[0] = z[1]
    Cd[0] = z[2]
    Ad[2] = z[3]
    Kd[1] = z[4]
    Bd[1] = z[5]
    Cd[1] = z[6]
    Kd[2] = z[7]
    Bd[2] = z[8]
    Cd[2] = z[9]
    Ad[3] = z[10]
    Kd[3] = z[11]
    Bd[3] = z[12]
    Cd[3] = z[13]
    Ad[4] = z[14]
    Kd[4] = z[15]
    Bd[4] = z[16]
    Cd[4] = z[17]
    Ad[5] = z[18]
    # identities
    K0 = Kd[0]
    Ad[0] = 2 / K0
    Ad[1] = -2 * Kd[1] / K0**2
    return Kd, Ad, Bd, Cd


def eq_coeff_num(name, n, Kd, Ad, Bd, Cd):
    """Coefficient of u^n of pre-cleared 'name', numeric (float dicts)."""
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
    return acc.get(want, 0)


orders = ([('E1', n) for n in [2, 4, 6, 8]]
          + [('E2', n) for n in [2, 4, 6, 8]]
          + [('E5', n) for n in [4, 5, 6, 7, 8]]
          + [('E6', n) for n in [5, 7, 9]])


def fun(z):
    Kd, Ad, Bd, Cd = build_dicts(z)
    r = []
    for (name, n) in orders:
        e = eq_coeff_num(name, n, Kd, Ad, Bd, Cd)
        r.append(float(sp.N(e, 30)))
    return np.array(r)


# seed from handoff fit
g0 = np.array([
    3.4553,     # K0
    0.2898,     # B0
    1.4741,     # C0
    -0.643,     # A2
    0.02,       # K1
    0.0,        # B1
    0.0,        # C1
    2.937,      # K2
    -0.469,     # B2
    3.466,      # C2
    0.0,        # A3
    0.0,        # K3
    0.0,        # B3
    0.0,        # C3
    0.0,        # A4
    0.0,        # K4
    0.0,        # B4
    0.0,        # C4
    0.0,        # A5
])

print('initial |res| = %.3e' % np.max(np.abs(fun(g0))), flush=True)
sol = least_squares(fun, g0, x_scale='jac', xtol=1e-13, ftol=1e-13,
                    gtol=1e-13, max_nfev=60000)
print('|residual| = %.3e' % np.max(np.abs(sol.fun)), flush=True)
z = sol.x
Kd, Ad, Bd, Cd = build_dicts(z)
print('K0=%.10f  A0=%.10f  A0*K0=%.12f' % (Kd[0], Ad[0], Kd[0]*Ad[0]))
print('  K: K1=%.6e K2=%.8f K3=%.6e K4=%.6e' % (Kd[1], Kd[2], Kd[3], Kd[4]))
print('  A: A1=%.6e A2=%.8f A3=%.6e A4=%.6e A5=%.6e' % (Ad[1], Ad[2], Ad[3], Ad[4], Ad[5]))
print('  B: B0=%.8f B1=%.6e B2=%.8f B3=%.6e B4=%.6e' % (Bd[0], Bd[1], Bd[2], Bd[3], Bd[4]))
print('  C: C0=%.8f C1=%.6e C2=%.8f C3=%.6e C4=%.6e' % (Cd[0], Cd[1], Cd[2], Cd[3], Cd[4]))
for (name, n), r in zip(orders, sol.fun):
    if abs(r) > 1e-10:
        print('  RESID %s_%d = %.3e' % (name, n, r))
print('A1 + 2*K1/K0^2 = %.3e (should be 0)' % (Ad[1] + 2*Kd[1]/Kd[0]**2))
