# fd_lib.py - INDEPENDENT finite-difference solver for the Dirichlet string
# -y'' = lambda rho y on (0,1), y(0) = y(1) = 0.
# Written from scratch for the re-audit run R-20260806T151000Z-o1reaudit-5A1C3D.
# Evidence-level numerics only; every proof-level claim is argued analytically
# in audit_report.md.

import numpy as np
from scipy.linalg import eigh

def fd_eigs(rho_vals, N, k_max=4):
    """rho_vals: values of rho at interior grid points x_i = i/N, i=1..N-1.
    Returns (ascending eigenvalues[:k_max], interior eigenvector matrix)."""
    h = 1.0 / N
    m = N - 1
    A = np.zeros((m, m))
    for i in range(m):
        A[i, i] = 2.0
        if i > 0:
            A[i, i - 1] = -1.0
        if i < m - 1:
            A[i, i + 1] = -1.0
    A = A / h ** 2
    B = np.diag(rho_vals)
    w, v = eigh(A, B)
    return w[:k_max], v


def fd_eigvals(rho_vals, N, k_max=4):
    """Eigenvalues only (generalized symmetric eigenproblem), faster than fd_eigs."""
    from scipy.linalg import eigvalsh
    h = 1.0 / N
    m = N - 1
    A = np.zeros((m, m))
    for i in range(m):
        A[i, i] = 2.0
        if i > 0:
            A[i, i - 1] = -1.0
        if i < m - 1:
            A[i, i + 1] = -1.0
    A = A / h ** 2
    B = np.diag(rho_vals)
    return eigvalsh(A, B)[:k_max]

def grid_rho_from_steps(breaks, values, N):
    """Evaluate the step function at the N-1 interior grid points."""
    x = np.linspace(0.0, 1.0, N + 1)[1:-1]
    idx = np.searchsorted(breaks, x, side='right') - 1
    idx = np.clip(idx, 0, len(values) - 1)
    return np.asarray(values, dtype=float)[idx]

def l1_exact(rho, sigma):
    """Exact L1 distance between two step functions (merged breakpoints)."""
    br, vr = rho
    bs, vs = sigma
    pts = sorted(set(br) | set(bs))
    tot = 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        if b <= a:
            continue
        mid = 0.5 * (a + b)
        i1 = np.searchsorted(br, mid, side='right') - 1
        i2 = np.searchsorted(bs, mid, side='right') - 1
        tot += abs(vr[i1] - vs[i2]) * (b - a)
    return tot

def stepval(x, breaks, values):
    idx = np.searchsorted(breaks, x, side='right') - 1
    idx = np.clip(idx, 0, len(values) - 1)
    return values[idx]

def hs_norm2(rho, sigma, n=1600):
    """||S_rho - S_sigma||_HS^2 by 2D trapezoid on an n x n grid.
    Kernel difference G(x,t)*(sqrt(rho(x))sqrt(rho(t)) - sqrt(sigma(x))sqrt(sigma(t)))."""
    x = np.linspace(0.0, 1.0, n)
    br, vr = rho
    bs, vs = sigma
    rx = np.array([stepval(xi, br, vr) for xi in x])
    sx = np.array([stepval(xi, bs, vs) for xi in x])
    G = np.minimum.outer(x, x) * (1.0 - np.maximum.outer(x, x))
    sr = np.sqrt(np.outer(rx, rx))
    ss = np.sqrt(np.outer(sx, sx))
    K = G * (sr - ss)
    h = 1.0 / (n - 1)
    w = np.ones(n)
    w[0] = w[-1] = 0.5
    return h * h * np.sum(np.outer(w, w) * K ** 2)

def fh_cross_integrals(rho, sigma, n=1600):
    """Returns dict with I1 = int int G^2 A(x)^2, I2 = int int G^2 A(x) A(t),
    norms of A = |rho - sigma|, for the F-001 chain checks."""
    x = np.linspace(0.0, 1.0, n)
    br, vr = rho
    bs, vs = sigma
    rx = np.array([stepval(xi, br, vr) for xi in x])
    sx = np.array([stepval(xi, bs, vs) for xi in x])
    A = np.abs(rx - sx)
    G = np.minimum.outer(x, x) * (1.0 - np.maximum.outer(x, x))
    G2 = G ** 2
    h = 1.0 / (n - 1)
    w = np.ones(n)
    w[0] = w[-1] = 0.5
    W = np.outer(w, w)
    I1 = h * h * np.sum(W * G2 * np.outer(A, np.ones(n)) ** 2)
    I2 = h * h * np.sum(W * G2 * np.outer(A, A))
    A1 = h * np.sum(w * A)
    A2 = h * np.sum(w * A ** 2)
    return {"I1": I1, "I2": I2, "A1": A1, "A2": A2}