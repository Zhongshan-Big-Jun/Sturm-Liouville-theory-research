# -*- coding: utf-8 -*-
"""R-209 M3 reduced-final seed solve (per R-210 fix recommendation).

Build the reduced residual ONCE symbolically with truncated power-dict
arithmetic (eq_coeff pattern of _gapn2_cascade_num3.py), parameterized by the
19 reduced unknowns, with a0 = 2/K0 and a1 = -2 K1/K0^2 encoded via dict
substitution (NEVER as separate variables).  Precompile -> lambdify -> ONE
least_squares call from the handoff fit seed; fall back to scipy root and
mpmath damped Newton on failure.

STRICT bookkeeping (exact pre-cleared P, exact identities); root values are
EVIDENCE.
"""
import pickle
import numpy as np
import sympy as sp
from sympy import pi, sqrt
from scipy.optimize import least_squares, root

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


def eq_coeff(name, n, Kd, Ad, Bd, Cd):
    """Coefficient of u^n of pre-cleared 'name' with the given series dicts."""
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


# ---- 19 reduced unknowns (symbolic) ----
# K0,K1,K2,K3,K4 ; B0,B1,B2,B3,B4 ; C0,C1,C2,C3,C4 ; A2,A3,A4,A5
K0, K1, K2, K3, K4 = sp.symbols('K0 K1 K2 K3 K4')
B0, B1, B2, B3, B4 = sp.symbols('B0 B1 B2 B3 B4')
C0, C1, C2, C3, C4 = sp.symbols('C0 C1 C2 C3 C4')
A2, A3, A4, A5 = sp.symbols('A2 A3 A4 A5')


def build_dicts():
    """Series dicts with a0=2/K0 and a1=-2K1/K0^2 enforced."""
    NR = 8
    Kd = {0: K0, 1: K1, 2: K2, 3: K3, 4: K4}
    Bd = {0: B0, 1: B1, 2: B2, 3: B3, 4: B4}
    Cd = {0: C0, 1: C1, 2: C2, 3: C3, 4: C4}
    Ad = {2: A2, 3: A3, 4: A4, 5: A5}
    Ad[0] = 2 / K0
    Ad[1] = -2 * K1 / K0**2
    for dd in range(NR + 1):
        Kd.setdefault(dd, 0)
        Bd.setdefault(dd, 0)
        Cd.setdefault(dd, 0)
        Ad.setdefault(dd, 0)
    return Kd, Ad, Bd, Cd


Kd, Ad, Bd, Cd = build_dicts()

# orders: reduced seed + higher levels (E1/E2 even 2..8, E5 4..8, E6 5,7,9)
orders = ([('E1', n) for n in [2, 4, 6, 8]]
          + [('E2', n) for n in [2, 4, 6, 8]]
          + [('E5', n) for n in [4, 5, 6, 7, 8]]
          + [('E6', n) for n in [5, 7, 9]])

print('building reduced symbolic system (19 unknowns)...', flush=True)
sys_expr = []
for (name, n) in orders:
    sys_expr.append(eq_coeff(name, n, Kd, Ad, Bd, Cd))
    tt = len(sys_expr[-1].as_ordered_terms()) if sys_expr[-1] != 0 else 0
    print('  %s_%d: %d terms' % (name, n, tt), flush=True)

unk19 = [K0, K1, K2, K3, K4, B0, B1, B2, B3, B4, C0, C1, C2, C3, C4,
         A2, A3, A4, A5]
Fn = sp.lambdify(unk19, sys_expr, 'numpy')
print('lambdified.', flush=True)


def fun(v):
    r = Fn(*v)
    return np.array([float(x) for x in r])


# --- seed from handoff fit ---
g0 = np.array([
    3.4553,    # K0
    0.02,      # K1
    2.937,     # K2
    0.0,       # K3
    0.0,       # K4
    0.2898,    # B0
    0.0,       # B1
    -0.469,    # B2
    0.0,       # B3
    0.0,       # B4
    1.4741,    # C0
    0.0,       # C1
    3.466,     # C2
    0.0,       # C3
    0.0,       # C4
    -0.643,    # A2
    0.0,       # A3
    0.0,       # A4
    0.0,       # A5
])

print('initial |res| = %.3e' % np.max(np.abs(fun(g0))), flush=True)
sol = least_squares(fun, g0, x_scale='jac', xtol=1e-13, ftol=1e-13,
                    gtol=1e-13, max_nfev=60000)
z = sol.x
print('least_squares |residual| = %.3e' % np.max(np.abs(sol.fun)), flush=True)


def report(zv, tag):
    K0v, K1v, K2v, K3v, K4v = zv[0], zv[1], zv[2], zv[3], zv[4]
    B0v, B1v, B2v, B3v, B4v = zv[5], zv[6], zv[7], zv[8], zv[9]
    C0v, C1v, C2v, C3v, C4v = zv[10], zv[11], zv[12], zv[13], zv[14]
    A2v, A3v, A4v, A5v = zv[15], zv[16], zv[17], zv[18]
    a0 = 2 / K0v
    a1 = -2 * K1v / K0v**2
    print('[%s] K0=%.10f a0=%.10f a1=%.6e' % (tag, K0v, a0, a1))
    print('  K: K1=%.6e K2=%.8f K3=%.6e K4=%.6e' % (K1v, K2v, K3v, K4v))
    print('  A: A2=%.8f A3=%.6e A4=%.6e A5=%.6e' % (A2v, A3v, A4v, A5v))
    print('  B: B0=%.8f B1=%.6e B2=%.8f B3=%.6e B4=%.6e' % (B0v, B1v, B2v, B3v, B4v))
    print('  C: C0=%.8f C1=%.6e C2=%.8f C3=%.6e C4=%.6e' % (C0v, C1v, C2v, C3v, C4v))
    # consistency C at u=0
    Cc = 1 + B0v * K0v / 2 + 3 * pi / (2 * K0v) - K0v**2 / 12
    print('  consistency C(0) = %.10e' % float(sp.N(Cc, 30)))
    print('  D*R -> 2*K0*C0 = %.10f ; Dk/u^5 -> C0 = %.10f' % (2 * K0v * C0v, C0v))
    return dict(K0=K0v, K1=K1v, K2=K2v, K3=K3v, K4=K4v, B0=B0v, B1=B1v, B2=B2v,
                B3=B3v, B4=B4v, C0=C0v, C1=C1v, C2=C2v, C3=C3v, C4=C4v,
                A2=A2v, A3=A3v, A4=A4v, A5=A5v, a0=a0, a1=a1)


report(z, 'least_squares')

# verify each order residual
print('per-equation residuals:')
for (name, n), r in zip(orders, sol.fun):
    if abs(r) > 1e-10:
        print('  RESID %s_%d = %.3e' % (name, n, r))

# fallback: scipy root on the same precompiled function
if np.max(np.abs(sol.fun)) > 1e-8:
    print('least_squares residual too high; trying scipy root (hybr)...', flush=True)
    rsol = root(fun, g0, method='hybr')
    print('root success=%s |res|=%s' % (rsol.success, rsol.message))
    if rsol.success:
        report(rsol.x, 'scipy_root')
        print('per-equation residuals (scipy root):')
        for (name, n), r in zip(orders, fun(rsol.x)):
            if abs(r) > 1e-10:
                print('  RESID %s_%d = %.3e' % (name, n, r))

# dump best (least_squares result)
import json
json.dump({k: float(v) for k, v in report(z, 'FINAL').items()},
          open(r'scripts/_gapn2_largeR_reduced_seed.json', 'w'), indent=1)
print('saved scripts/_gapn2_largeR_reduced_seed.json (least_squares result)')
