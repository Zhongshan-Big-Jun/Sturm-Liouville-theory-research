# sl_lib.py - transfer-matrix solver for the Dirichlet string -y'' = lambda rho y
# Evidence-level numerics for the O1 revision run.
# Piecewise-constant rho given as (breaks, values): intervals (breaks[i], breaks[i+1])
# have value values[i]; breaks[0] = 0, breaks[-1] = 1.

import numpy as np
from numpy.polynomial.legendre import leggauss

def M_interval(L, c, lam):
    """Transfer matrix for y'' + lam*c*y = 0 over length L (state (y, y'))."""
    if L <= 0:
        return np.eye(2)
    k = np.sqrt(lam * c)
    if k == 0:
        return np.array([[1.0, L], [0.0, 1.0]])
    ck, sk = np.cos(k * L), np.sin(k * L)
    return np.array([[ck, sk / k], [-k * sk, ck]])

def secular(lam, breaks, values):
    """F(lam) = y(1) for the solution with y(0) = 0, y'(0) = 1."""
    M = np.eye(2)
    for i in range(len(breaks) - 1):
        L = breaks[i + 1] - breaks[i]
        if L > 0:
            M = M_interval(L, values[i], lam) @ M
    return M[0, 1]

def eigenvalues(breaks, values, k_max=4, lam_max=None, grid_step=0.002, eps=1e-13):
    """Return eigenvalues lambda_1 < ... < lambda_{k_max}, all simple.
    Root-finding: sign changes of the entire secular function on a fine grid,
    then brentq.  If fewer than k_max roots are found, raise."""
    if lam_max is None:
        lam_max = (k_max + 1) ** 2 * np.pi ** 2 + 1.0
    n = int(np.ceil(lam_max / grid_step)) + 1
    grid = np.linspace(0.0, lam_max, n)
    F = np.array([secular(g, breaks, values) for g in grid])
    roots = []
    for i in range(n - 1):
        if F[i] == 0.0:
            roots.append(grid[i])
        elif F[i] * F[i + 1] < 0:
            a, b = grid[i], grid[i + 1]
            # brentq via scipy
            from scipy.optimize import brentq
            r = brentq(secular, a, b, args=(breaks, values), xtol=1e-15, rtol=1e-14)
            roots.append(r)
    roots = sorted(set(np.round(roots, 12)))
    roots = [r for r in roots if r > 1e-9]
    if len(roots) < k_max:
        raise RuntimeError(f"only {len(roots)} roots found for k_max={k_max}")
    return roots[:k_max]

def state_at(x, lam, breaks, values):
    """State (y, y') at x for the solution with y(0)=0, y'(0)=1."""
    M = np.eye(2)
    i = 0
    while i < len(breaks) - 1 and breaks[i + 1] <= x:
        L = breaks[i + 1] - breaks[i]
        if L > 0:
            M = M_interval(L, values[i], lam) @ M
        i += 1
    # now x in [breaks[i], breaks[i+1]]
    L = x - breaks[i]
    if L > 0:
        M = M_interval(L, values[i], lam) @ M
    return M @ np.array([0.0, 1.0])

def eigenfuncs(breaks, values, lams, n_nodes_per_interval=24, xgrid=None):
    """Return u_k (L^2(rho)-normalized, sign > 0 near 0) and their derivatives
    on a fine grid, plus the grid itself.  Normalization via Gauss-Legendre."""
    xg = np.linspace(0.0, 1.0, 20001)
    us = []
    for lam in lams:
        u = np.array([state_at(x, lam, breaks, values)[0] for x in xg])
        # Gauss-Legendre normalization
        norm2 = 0.0
        for i in range(len(breaks) - 1):
            a, b = breaks[i], breaks[i + 1]
            if b - a <= 0:
                continue
            nodes, wts = leggauss(n_nodes_per_interval)
            xs = 0.5 * (a + b) + 0.5 * (b - a) * nodes
            vals = np.array([state_at(x, lam, breaks, values)[0] for x in xs])
            norm2 += 0.5 * (b - a) * np.sum(wts * values[i] * vals ** 2)
        u = u / np.sqrt(norm2)
        if u[1] < 0:
            u = -u
        us.append(u)
    up = []
    for lam in lams:
        u_deriv = np.array([state_at(x, lam, breaks, values)[1] for x in xg])
        # normalize with same factor
        norm2 = 0.0
        for i in range(len(breaks) - 1):
            a, b = breaks[i], breaks[i + 1]
            if b - a <= 0:
                continue
            nodes, wts = leggauss(n_nodes_per_interval)
            xs = 0.5 * (a + b) + 0.5 * (b - a) * nodes
            vals = np.array([state_at(x, lam, breaks, values)[0] for x in xs])
            norm2 += 0.5 * (b - a) * np.sum(wts * values[i] * vals ** 2)
        sign = 1.0 if u[1] > 0 else -1.0
        u_deriv = u_deriv / np.sqrt(norm2) * sign
        up.append(u_deriv)
    return us, up, xg

def f_of(breaks, values, lams, us=None, up=None):
    """f = lambda_1 u_1^2 - lambda_2 u_2^2 on the fine grid."""
    if us is None:
        us, up, xg = eigenfuncs(breaks, values, lams)
    return lams[0] * us[0] ** 2 - lams[1] * us[1] ** 2, us, up

def count_sign_changes(vals, xg):
    """Count sign changes of a function sampled on a fine grid; returns indices."""
    s = np.sign(vals)
    idx = np.where(s[1:] * s[:-1] < 0)[0]
    return list(idx)

def zeros_of_f(fvals, xg):
    """Zeros of f via linear interpolation at sign changes."""
    zs = []
    s = np.sign(fvals)
    for i in range(len(fvals) - 1):
        if s[i] * s[i + 1] < 0:
            x0, x1 = xg[i], xg[i + 1]
            f0, f1 = fvals[i], fvals[i + 1]
            zs.append(x0 + (x1 - x0) * (-f0) / (f1 - f0))
    return np.array(zs)

def D_of(breaks, values, lams=None):
    if lams is None:
        lams = eigenvalues(breaks, values, k_max=2)
    return lams[1] - lams[0]
