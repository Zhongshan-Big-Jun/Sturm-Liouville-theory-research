# -*- coding: utf-8 -*-
"""#3: direct self-consistent solver for gap extrema (fixed: n unknowns, n residuals by symmetry)."""
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

if __name__ == "__main__":
    R = 4.0
    for sup in (True, False):
        full, lam, D = solve_sc(R, 1, sup, [0.45])
        print(f"n=1 {'SUP' if sup else 'INF'}: edge={full[0]:.10f} lam1={lam[0]:.8f} lam2={lam[1]:.8f} D={D:.8f}")
    for sup in (True, False):
        full, lam, D = solve_sc(R, 2, sup, [0.27, 0.38])
        print(f"n=2 {'SUP' if sup else 'INF'}: edges={np.array2string(full, precision=6)} lam2={lam[1]:.8f} lam3={lam[2]:.8f} D={D:.8f}")
    for sup in (True, False):
        full, lam, D = solve_sc(R, 3, sup, [0.19, 0.31, 0.44])
        print(f"n=3 {'SUP' if sup else 'INF'}: edges={np.array2string(full, precision=6)} lam3={lam[2]:.8f} lam4={lam[3]:.8f} D={D:.8f}")
