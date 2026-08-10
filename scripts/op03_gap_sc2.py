# -*- coding: utf-8 -*-
"""#3: solve self-consistent gap extrema for n=3,4 (SUP) and verify band count."""
import numpy as np
from scipy.optimize import fsolve
from op03_gap_n1 import lams_blocks, eigfuns_at

def make_blocks_from_edges(edges, R, n, sup):
    bd = np.sort(edges)
    xs = np.concatenate(([0.0], bd, [1.0]))
    inside = np.zeros(len(xs)-1, dtype=bool)
    for k in range(n):
        inside[2*k+1] = True
    vals = np.where(inside, R if sup else 1.0, 1.0 if sup else R)
    return [(xs[i+1]-xs[i], vals[i]) for i in range(len(xs)-1)]

def residuals(bd, R, n, sup):
    e = np.sort(bd)
    full = np.concatenate((e, 1 - e[::-1]))
    blocks = make_blocks_from_edges(full, R, n, sup)
    lam = lams_blocks(blocks, k=n+2)
    pts = np.array(full)
    vals = eigfuns_at(blocks, lam[n-1:n+1], pts)
    f = lam[n-1]*vals[0]**2 - lam[n]*vals[1]**2
    return f[:n]

def solve_sc(R, n, sup, guess):
    e0 = np.sort(guess)
    sol = fsolve(residuals, e0, args=(R, n, sup), xtol=1e-13, full_output=True)
    e = np.sort(sol[0])
    full = np.concatenate((e, 1 - e[::-1]))
    blocks = make_blocks_from_edges(full, R, n, sup)
    lam = lams_blocks(blocks, k=n+2)
    D = lam[n]-lam[n-1]
    return full, lam, D

def verify_bands(full, R, n, sup):
    """Check rho_pred == rho_true and f has exactly n bands."""
    blocks = make_blocks_from_edges(full, R, n, sup)
    lam = lams_blocks(blocks, k=n+2)
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    pts = np.array(sorted(set(np.round(np.linspace(2e-4, 1-2e-4, 500), 5))))
    vals = eigfuns_at(blocks, lam[n-1:n+1], pts)
    f = lam[n-1]*vals[0]**2 - lam[n]*vals[1]**2
    rho_pred = np.where(f > 0, R if sup else 1.0, 1.0 if sup else R)
    rho_true = np.zeros_like(pts)
    for i, p in enumerate(pts):
        for j in range(len(xs)-1):
            if xs[j] <= p <= xs[j+1]:
                rho_true[i] = blocks[j][1]; break
    nz = np.sum(np.signbit(f[1:]) != np.signbit(f[:-1]))
    return np.mean(rho_pred == rho_true), nz, f, pts

R = 4.0
for n, guess in [(3, [0.184, 0.280, 0.444]), (4, [0.143, 0.220, 0.346, 0.438])]:
    for sup in (True, False):
        full, lam, D = solve_sc(R, n, sup, guess)
        m, nz, f, pts = verify_bands(full, R, n, sup)
        print(f"n={n} {'SUP' if sup else 'INF'}: D={D:.8f} edges={np.array2string(full, precision=5)}")
        print(f"    band-consistency={m:.4f} sign-changes={nz}")
