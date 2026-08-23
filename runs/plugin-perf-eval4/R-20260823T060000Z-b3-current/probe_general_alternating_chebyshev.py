"""Lightweight EVIDENCE probe for the general alternating Chebyshev secular
representation (Lemma C1) and O2 central-pair maxima.

Not a proof. Use scipy/numpy only for numerical cross-checks.
"""
import math
import numpy as np
from scipy.optimize import brentq


def secular_direct(x, r, n, s):
    p = r * x
    q = s * x
    A = np.array([[math.cos(p), math.sin(p)],
                  [-math.sin(p), math.cos(p)]])
    B = np.array([[math.cos(q), math.sin(q) / s],
                  [-s * math.sin(q), math.cos(q)]])
    M = np.linalg.matrix_power(A @ B, n) @ A
    return M[0, 1]


def secular_cheb(x, r, n, s):
    p = r * x
    q = s * x
    m = math.cos(p) * math.cos(q) - (s + 1 / s) * math.sin(p) * math.sin(q) / 2
    delta = math.sin(q) / (s * math.sin(p))
    U0 = 1.0
    U1 = 2 * m
    if n == 0:
        return math.sin(p) * U0
    if n == 1:
        return math.sin(p) * (U1 + delta * U0)
    prev = U0
    cur = U1
    for _ in range(2, n + 1):
        nxt = 2 * m * cur - prev
        prev, cur = cur, nxt
    return math.sin(p) * (cur + delta * prev)


def central_pair_ratio(r, n, s):
    xs = np.linspace(1e-4, 2.0, 10000)
    vals = np.array([secular_direct(v, r, n, s) for v in xs])
    idx = np.nonzero(vals[:-1] * vals[1:] < 0)[0]
    roots = []
    for i in idx:
        z = brentq(secular_direct, xs[i], xs[i + 1], args=(r, n, s),
                   xtol=1e-13, rtol=1e-13)
        if not roots or abs(z - roots[-1]) > 1e-5:
            roots.append(z)
    if len(roots) < n + 1:
        return None, roots
    return (roots[n] / roots[n - 1]) ** 2, roots


if __name__ == '__main__':
    s = 2.0
    print('Lemma C1 numeric check (max abs diff on sample grid):')
    for n in range(2, 6):
        for r in [1.0, 1.5, 2.0, 2.5, 3.0]:
            err = max(abs(secular_direct(x, r, n, s) - secular_cheb(x, r, n, s))
                      for x in np.linspace(0.02, 2.0, 101))
            print(f'  n={n} r={r} maxerr={err:.3g}')
    print('O2 EVIDENCE for R=4, n=2 central pair ratio:')
    s = 2.0
    for r in [1.0, 1.5, 2.0, 2.5, 3.0]:
        val, _ = central_pair_ratio(r, 2, s)
        print(f'  r={r} ratio={val if val is not None else float("nan"):.6f}')
