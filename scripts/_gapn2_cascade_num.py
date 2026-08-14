# -*- coding: utf-8 -*-
"""R-209 M3 cascade numerical solve (fast): level-by-level with exact
truncated power-dict and concrete solved lower values.

After the STRICT reduction (A0=2/K0, A1=-2 K1/K0^2), the remaining seed
unknowns are {K0,K1,B0,B1,C0,C1,K2,A2,B2,C2,...}.  We solve the seed
nonlinearly (least_squares from the handoff fit seed), then each higher
level j>=3 as an affine system in (K_j,A_j,B_j,C_j) [careful: which appear].

This is the numerical part (EVIDENCE); the STRICT structure is in the
addendum.  Output: full branch coefficients.
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
        return {0: 1.0 if not isinstance(next(iter(X.values()), 1), sp.Basic) and False else sp.Integer(1)}
    return None  # placeholder


def poly_coeffs_float(coef, Kser, Aser, Bser, Cser, nmax):
    """Evaluate coefficient of u in [0..nmax] of polynomial coef (in K,A,B,C)
    with SERIES dicts {degree: float}, truncated.  Returns dict degree->float."""
    # Build truncated powers via numpy-free dict mult
    def spow_f(X, n):
        if n == 0:
            return {0: 1.0}
        out = spow_f(X, n // 2)
        out = smulf(out, out)
        if n % 2 == 1:
            out = smulf(out, X)
        return out
    def smulf(X, Y):
        out = {}
        for i, cx in X.items():
            for j, cy in Y.items():
                m = i + j
                if m <= nmax:
                    out[m] = out.get(m, 0) + cx * cy
        return out
    poly = sp.Poly(coef, K, A, B, C)
    Kpow = {n: spow_f(Kser, n) for n in range(poly.degree(K) + 1)}
    Apow = {n: spow_f(Aser, n) for n in range(poly.degree(A) + 1)}
    Bpow = {n: spow_f(Bser, n) for n in range(poly.degree(B) + 1)}
    Cpow = {n: spow_f(Cser, n) for n in range(poly.degree(C) + 1)}
    acc = {}
    for mon, cmon in zip(poly.monoms(), poly.coeffs()):
        cf = float(cmon)
        s = {0: cf}
        if mon[0]:
            s = smulf(s, Kpow[mon[0]])
        if mon[1]:
            s = smulf(s, Apow[mon[1]])
        if mon[2]:
            s = smulf(s, Bpow[mon[2]])
        if mon[3]:
            s = smulf(s, Cpow[mon[3]])
        for m, c in s.items():
            acc[m] = acc.get(m, 0) + c
    return acc


def residual(z, orders, nmax):
    """z: dict of unknown name->float. orders: list of (name, n)."""
    # series dicts
    Kd = {j: z.get('K%d' % j, 0.0) for j in range(nmax + 1)}
    Ad = {j: z.get('A%d' % j, 0.0) for j in range(nmax + 1)}
    Bd = {j: z.get('B%d' % j, 0.0) for j in range(nmax + 1)}
    Cd = {j: z.get('C%d' % j, 0.0) for j in range(nmax + 1)}
    res = []
    for (name, n) in orders:
        tot = {}
        for (nm, m), coef in Pc.items():
            if nm != name or m > n:
                continue
            ser = poly_coeffs_float(coef, Kd, Ad, Bd, Cd, nmax)
            want = n - m
            if want in ser:
                tot[want] = tot.get(want, 0) + ser[want]
        res.append(sum(tot.values()))
    return np.array(res)


def main():
    # unknowns through K9/A9/B9/C9
    unk = (['K%d' % j for j in range(10)] + ['A%d' % j for j in range(10)]
           + ['B%d' % j for j in range(10)] + ['C%d' % j for j in range(10)])
    # orders: E1,E2 even 0..10, E5 0..10, E6 3,5,7,9
    orders = ([( 'E1', n) for n in range(0, 11, 2)]
              + [('E2', n) for n in range(0, 11, 2)]
              + [('E5', n) for n in range(0, 11)]
              + [('E6', n) for n in [3, 5, 7, 9]])
    guess = {name: 0.0 for name in unk}
    # handoff fit seed
    guess['K0'] = 3.4553
    guess['A0'] = 2 / 3.4553
    guess['K2'] = 2.937
    guess['A2'] = -0.643
    guess['B0'] = 0.2898
    guess['B2'] = -0.469
    guess['C0'] = 1.4741
    guess['C2'] = 3.466
    # enforce A0 K0 = 2 exactly at start
    guess['A0'] = 2 / guess['K0']
    vec0 = np.array([guess[k] for k in unk])
    nmax = 9

    def fun(v):
        z = dict(zip(unk, v))
        return residual(z, orders, nmax)

    print('initial |res| = %.3e' % np.max(np.abs(fun(vec0))), flush=True)
    sol = least_squares(fun, vec0, x_scale='jac', xtol=1e-13, ftol=1e-13,
                        gtol=1e-13, max_nfev=20000)
    zs = dict(zip(unk, sol.x))
    print('|residual| = %.3e' % np.max(np.abs(sol.fun)), flush=True)
    for name in ['K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9',
                 'A0', 'A1', 'A2', 'A3', 'A4', 'B0', 'B1', 'B2', 'C0', 'C1', 'C2', 'C3', 'C4']:
        print('  %s = %.12f' % (name, zs[name]), flush=True)
    # verify A0*K0
    print('A0*K0 = %.12f' % (zs['A0'] * zs['K0']))
    # check odd coefficients
    print('odd: K1=%g K3=%g K5=%g A1=%g B1=%g C1=%g' % (
        zs['K1'], zs['K3'], zs['K5'], zs['A1'], zs['B1'], zs['C1']))


if __name__ == '__main__':
    main()
