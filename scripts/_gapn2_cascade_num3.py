# -*- coding: utf-8 -*-
"""R-209 M3 numerical branch solve (fast truncated power-dict).

Builds the exact truncated system symbolically ONCE via truncated polynomial
arithmetic (smul/spow capped at the target order), lambdifies, solves with
least_squares.  Full integer-power series through u^9.

STRICT bookkeeping; root values are EVIDENCE.
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

NR = 10
Ks = [sp.symbols('K%d' % j) for j in range(NR + 1)]
As = [sp.symbols('A%d' % j) for j in range(NR + 1)]
Bs = [sp.symbols('B%d' % j) for j in range(NR + 1)]
Cs = [sp.symbols('C%d' % j) for j in range(NR + 1)]


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


def eq_coeff(name, n):
    """Coefficient of u^n of pre-cleared equation 'name' (truncated)."""
    Kd = {j: Ks[j] for j in range(n + 1)}
    Ad = {j: As[j] for j in range(n + 1)}
    Bd = {j: Bs[j] for j in range(n + 1)}
    Cd = {j: Cs[j] for j in range(n + 1)}
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


orders = ([('E1', n) for n in range(0, 11, 2)]
          + [('E2', n) for n in range(0, 11, 2)]
          + [('E5', n) for n in range(0, 11)]
          + [('E6', n) for n in [3, 5, 7, 9]])

print('building symbolic system (truncated power dict)...', flush=True)
sys_expr = []
for (name, n) in orders:
    sys_expr.append(eq_coeff(name, n))
    tt = len(sys_expr[-1].as_ordered_terms()) if sys_expr[-1] != 0 else 0
    print('  %s_%d: %d terms' % (name, n, tt), flush=True)

allunk = Ks + As + Bs + Cs
Fn = sp.lambdify(allunk, sys_expr, 'numpy')
print('lambdified.', flush=True)


def fun(v):
    return np.array([float(x) for x in Fn(*v)])


guess = np.zeros(len(allunk))
g = {'K0': 3.4553, 'A0': 2 / 3.4553, 'K2': 2.937, 'A2': -0.643,
     'B0': 0.2898, 'B2': -0.469, 'C0': 1.4741, 'C2': 3.466}
for i, s in enumerate(allunk):
    guess[i] = g.get(str(s), 0.0)

print('initial |res| = %.3e' % np.max(np.abs(fun(guess))), flush=True)
sol = least_squares(fun, guess, x_scale='jac', xtol=1e-13, ftol=1e-13,
                    gtol=1e-13, max_nfev=40000)
zs = {str(s): v for s, v in zip(allunk, sol.x)}
print('|residual| = %.3e' % np.max(np.abs(sol.fun)), flush=True)
for name in ['K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'A0', 'A1', 'A2', 'A3',
             'A4', 'B0', 'B1', 'B2', 'B3', 'B4', 'C0', 'C1', 'C2', 'C3', 'C4']:
    v = zs.get(name, 0.0)
    if abs(v) > 1e-13:
        print('  %s = %+.12e' % (name, v), flush=True)
print('A0*K0 = %.15f' % (zs['A0'] * zs['K0']))
print('odd: K1=%.3e K3=%.3e K5=%.3e A1=%.3e B1=%.3e C1=%.3e' % (
    zs.get('K1', 0), zs.get('K3', 0), zs.get('K5', 0),
    zs.get('A1', 0), zs.get('B1', 0), zs.get('C1', 0)))

# save full solution
import json
json.dump(zs, open(r'scripts/_gapn2_largeR_branch.json', 'w'))
print('saved scripts/_gapn2_largeR_branch.json')
