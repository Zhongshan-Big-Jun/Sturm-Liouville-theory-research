# -*- coding: utf-8 -*-
"""#3: SUP via least_squares on residual f=0 (bounded), seeded from INF solutions."""
import numpy as np
from scipy.optimize import least_squares
from op03_gap_n1 import lams_blocks, eigfuns_at

def make_blocks_from_edges(edges, R, n, sup):
    bd = np.sort(edges)
    xs = np.concatenate(([0.0], bd, [1.0]))
    inside = np.zeros(len(xs)-1, dtype=bool)
    for k in range(n):
        inside[2*k+1] = True
    vals = np.where(inside, R if sup else 1.0, 1.0 if sup else R)
    return [(xs[i+1]-xs[i], vals[i]) for i in range(len(xs)-1)]

def residual_edges(e, R, n, sup):
    e = np.sort(e)
    full = np.concatenate((e, 1 - e[::-1]))
    blocks = make_blocks_from_edges(full, R, n, sup)
    lam = lams_blocks(blocks, k=n+2)
    pts = np.array(full)
    vals = eigfuns_at(blocks, lam[n-1:n+1], pts)
    f = lam[n-1]*vals[0]**2 - lam[n]*vals[1]**2
    return f[:n]

def solve(R, n, sup, guess):
    lb = np.full(n, 1e-3); ub = np.full(n, 0.5-1e-3)
    sol = least_squares(residual_edges, np.sort(guess), bounds=(lb, ub),
                        args=(R, n, sup), xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=200)
    e = np.sort(sol.x)
    full = np.concatenate((e, 1 - e[::-1]))
    blocks = make_blocks_from_edges(full, R, n, sup)
    lam = lams_blocks(blocks, k=n+2)
    return full, lam, lam[n]-lam[n-1], sol.cost

R = 4.0
# INF solutions from earlier run (use as SUP seeds)
inf_guesses = {
    3: [0.130448, 0.287505, 0.411388],
    4: [0.19044, 0.29494, 0.44843],
}
for n, g in inf_guesses.items():
    for tag, sup, seed in [("SUP", True, g), ("INF", False, g)]:
        full, lam, D, cost = solve(R, n, sup, seed)
        print(f"n={n} {tag}: D={D:.8f} cost={cost:.2e}")
        print(f"   edges={np.array2string(full, precision=6)} lam_n={lam[n-1]:.8f} lam_{n+1}={lam[n]:.8f}")
