# -*- coding: utf-8 -*-
"""R-209 M3 decisive seed solve: full 8-unknown seed (K1, B1 included,
a0=2/K0, a1=-2K1/K0^2 enforced) with 8 equations E1_2,E2_2,E6_5,E5_4,E5_5,
E5_6,E5_7,E6_7.  Multi-start to locate any root near K0 ~ 3.4."""
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


def eq_coeff(name, n, Kex, Aex, Bex, Cex):
    tot = 0
    for (nm, m), coef in Pc.items():
        if nm != name:
            continue
        cc = sp.expand(coef.subs({K: Kex, A: Aex, B: Bex, C: Cex}) * u**m)
        c = cc.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)


K0, K1, K2, A2, B0, B1, C0, C1 = sp.symbols('K0 K1 K2 A2 B0 B1 C0 C1')

Kex = K0 + K1 * u + K2 * u**2
Aex = (2 / K0) + (-2 * K1 / K0**2) * u + A2 * u**2
Bex = B0 + B1 * u
Cex = C0 + C1 * u

names = ['E1_2', 'E2_2', 'E6_5', 'E5_4', 'E5_5', 'E5_6', 'E5_7', 'E6_7']
orders = [('E1', 2), ('E2', 2), ('E6', 5), ('E5', 4), ('E5', 5), ('E5', 6), ('E5', 7), ('E6', 7)]
eqs = []
for (name, n) in orders:
    e = sp.expand(sp.together(eq_coeff(name, n, Kex, Aex, Bex, Cex)) * K0**6)
    eqs.append(e)
    print('  %s: %d terms' % (name, len(e.as_ordered_terms())), flush=True)

targets = [K0, K1, K2, A2, B0, B1, C0, C1]
Fn = sp.lambdify(targets, eqs, 'numpy')


def fun(v):
    return np.array([float(x) for x in Fn(*v)], dtype=float)


base = np.array([3.4553, 0.0, 2.937, -0.643, 0.2898, 0.0, 1.4741, 0.0])
print('initial |res| = %.3e' % np.max(np.abs(fun(base))), flush=True)

# multi-start: vary K0 and K1 signs/magnitudes around the fit
starts = []
for K0v in [3.0, 3.4, 3.5, 3.6]:
    for K1v in [0.0, 0.3, -0.3, 1.0, -1.0]:
        s = base.copy()
        s[0] = K0v
        s[1] = K1v
        starts.append(s)

best = None
best_res = 1e99
for si, s in enumerate(starts):
    res = least_squares(fun, s, xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=40000)
    r = np.max(np.abs(res.fun))
    if r < best_res:
        best_res = r
        best = res.x
    print('  start[%d] K0=%.1f K1=%.1f -> |res|=%.3e K0=%.6f' % (si, s[0], s[1], r, res.x[0]), flush=True)

print()
print('BEST |res| = %.3e' % best_res)
if best is not None:
    for t, v in zip(['K0', 'K1', 'K2', 'A2', 'B0', 'B1', 'C0', 'C1'], best):
        print('  %s = %+.12e' % (t, v))
    print('  a0 = 2/K0 = %.10f ; a1 = -2K1/K0^2 = %.10f' % (2 / best[0], -2 * best[1] / best[0]**2))
    print('  C(0) = 1 + B0*K0/2 + 3pi/(2K0) - K0^2/12 = %.10e' % (
        1 + best[4] * best[0] / 2 + 3 * pi / (2 * best[0]) - best[0]**2 / 12))
    print('  D*R -> 2 K0 C0 = %.10f' % (2 * best[0] * best[6]))
    import json
    tnames = ['K0', 'K1', 'K2', 'A2', 'B0', 'B1', 'C0', 'C1']
    json.dump({k: float(v) for k, v in zip(tnames, best)},
              open(r'scripts/_gapn2_largeR_reduced_seed.json', 'w'), indent=1)
    print('  saved scripts/_gapn2_largeR_reduced_seed.json')
