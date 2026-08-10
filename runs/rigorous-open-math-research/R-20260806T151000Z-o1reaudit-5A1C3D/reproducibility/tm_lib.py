# tm_lib.py - INDEPENDENT exact transfer-matrix solver for the Dirichlet string
# -y'' = lambda rho y on (0,1), y(0) = y(1) = 0, piecewise-constant rho.
# Eigenvalues are roots of the secular function y(1) (solution with y(0)=0,
# y'(0)=1), found by grid scan + brentq; exact to ~1e-12.  Written from
# scratch for the re-audit run (independent of the audited run's battery).

import numpy as np
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

def interval_matrix(L, c, lam):
    if L <= 0.0:
        return np.eye(2)
    k = np.sqrt(lam * c)
    if k == 0.0:
        return np.array([[1.0, L], [0.0, 1.0]])
    ck, sk = np.cos(k * L), np.sin(k * L)
    return np.array([[ck, sk / k], [-k * sk, ck]])

def secular(lam, breaks, values):
    M = np.eye(2)
    for i in range(len(breaks) - 1):
        L = breaks[i + 1] - breaks[i]
        if L > 0.0:
            M = interval_matrix(L, values[i], lam) @ M
    return M[0, 1]

def eigenvalues(breaks, values, k_max=4, lam_max=None, grid_step=0.002):
    if lam_max is None:
        lam_max = (k_max + 1) ** 2 * np.pi ** 2 + 1.0
    n = int(np.ceil(lam_max / grid_step)) + 1
    grid = np.linspace(0.0, lam_max, n)
    F = np.array([secular(g, breaks, values) for g in grid])
    roots = []
    for i in range(n - 1):
        if F[i] == 0.0:
            roots.append(grid[i])
        elif F[i] * F[i + 1] < 0.0:
            r = brentq(secular, grid[i], grid[i + 1], args=(breaks, values),
                       xtol=1e-15, rtol=1e-14)
            roots.append(r)
    roots = sorted(set(np.round(roots, 12)))
    roots = [r for r in roots if r > 1e-9]
    if len(roots) < k_max:
        raise RuntimeError("only %d roots found" % len(roots))
    return roots[:k_max]


def secular_vec(lams, breaks, values):
    """Vectorized secular function y(1) over an array of lambda values."""
    L = np.asarray(lams, dtype=float)
    M00 = np.ones_like(L)
    M01 = np.zeros_like(L)
    M10 = np.zeros_like(L)
    M11 = np.ones_like(L)
    for i in range(len(breaks) - 1):
        le = breaks[i + 1] - breaks[i]
        if le <= 0.0:
            continue
        k = np.sqrt(L * values[i])
        ck = np.cos(k * le)
        sk = np.sin(k * le)
        A00 = ck
        A01 = np.where(k > 0.0, sk / k, le)
        A10 = -k * sk
        A11 = ck
        n00 = A00 * M00 + A01 * M10
        n01 = A00 * M01 + A01 * M11
        n10 = A10 * M00 + A11 * M10
        n11 = A10 * M01 + A11 * M11
        M00, M01, M10, M11 = n00, n01, n10, n11
    return M01

def eigenvalues_vec(breaks, values, k_max=4, lam_max=None, grid_step=0.01):
    """Eigenvalues via vectorized secular scan + brentq refinement."""
    if lam_max is None:
        lam_max = (k_max + 1) ** 2 * np.pi ** 2 + 1.0
    n = int(np.ceil(lam_max / grid_step)) + 1
    grid = np.linspace(0.0, lam_max, n)
    F = secular_vec(grid, breaks, values)
    roots = []
    for i in range(n - 1):
        if F[i] == 0.0:
            roots.append(grid[i])
        elif F[i] * F[i + 1] < 0.0:
            r = brentq(secular, grid[i], grid[i + 1], args=(breaks, values),
                       xtol=1e-15, rtol=1e-14)
            roots.append(r)
    roots = sorted(set(np.round(roots, 12)))
    roots = [r for r in roots if r > 1e-9]
    if len(roots) < k_max:
        raise RuntimeError("only %d roots found" % len(roots))
    return roots[:k_max]

def state_at(x, lam, breaks, values):
    """(y, y') at x for the solution with y(0) = 0, y'(0) = 1."""
    M = np.eye(2)
    i = 0
    while i < len(breaks) - 1 and breaks[i + 1] <= x:
        L = breaks[i + 1] - breaks[i]
        if L > 0.0:
            M = interval_matrix(L, values[i], lam) @ M
        i += 1
    L = x - breaks[i]
    if L > 0.0:
        M = interval_matrix(L, values[i], lam) @ M
    return M @ np.array([0.0, 1.0])

def eigenfuncs(breaks, values, lams, xgrid=None, n_nodes_per_interval=32):
    """L^2(rho)-normalized eigenfunctions (int rho u^2 = 1), sign u > 0 near 0,
    on xgrid (default fine uniform grid)."""
    if xgrid is None:
        xg = np.linspace(0.0, 1.0, 20001)
    else:
        xg = np.asarray(xgrid, dtype=float)
    us = []
    for lam in lams:
        u = np.array([state_at(x, lam, breaks, values)[0] for x in xg])
        norm2 = 0.0
        for i in range(len(breaks) - 1):
            a, b = breaks[i], breaks[i + 1]
            if b - a <= 0.0:
                continue
            nodes, wts = leggauss(n_nodes_per_interval)
            xs = 0.5 * (a + b) + 0.5 * (b - a) * nodes
            vals = np.array([state_at(x, lam, breaks, values)[0] for x in xs])
            norm2 += 0.5 * (b - a) * np.sum(wts * values[i] * vals ** 2)
        u = u / np.sqrt(norm2)
        if u[1] < 0.0:
            u = -u
        us.append(u)
    return us, xg