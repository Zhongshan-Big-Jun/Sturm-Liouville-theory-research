# -*- coding: utf-8 -*-
"""#3: high-precision self-consistent solutions for gap extrema, n=1..4."""
import numpy as np
from scipy.optimize import least_squares
from op03_gap_precise import f_edges

def solve(R, n, sup, guess, max_nfev=300):
    g0 = np.sort(np.asarray(guess, dtype=float))
    lb = np.full(n, 1e-4); ub = np.full(n, 0.5-1e-4)
    sol = least_squares(lambda e: f_edges(e, R, n, sup)[0], g0, bounds=(lb, ub),
                        xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=max_nfev)
    e = np.sort(sol.x)
    f, lam, blocks, full = f_edges(e, R, n, sup)
    return e, full, lam, np.max(np.abs(f)), lam[n]-lam[n-1]

R = 4.0
seeds = {
    (1,True):[0.4514855879], (1,False):[0.3825991113],
    (2,True):[0.293435,0.365461], (2,False):[0.202883,0.404038],
    (3,True):[0.22025,0.273125,0.469156], (3,False):[0.130448,0.287505,0.411388],
    (4,True):[0.177375,0.218208,0.374392,0.424211],
    (4,False):[0.19044,0.29494,0.44843,0.51],
}
for (n,sup), seed in seeds.items():
    try:
        e, full, lam, res, D = solve(R, n, sup, seed)
        print(f"n={n} {'SUP' if sup else 'INF'}: D={D:.10f} max|f|={res:.1e}")
        print(f"    edges={np.array2string(full, precision=7)}")
        print(f"    lam_n={lam[n-1]:.8f} lam_{n+1}={lam[n]:.8f}")
    except Exception as ex:
        print(f"n={n} {'SUP' if sup else 'INF'}: FAILED {ex}")
