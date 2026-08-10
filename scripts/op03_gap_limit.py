# -*- coding: utf-8 -*-
"""#3: large-R limits for n=1 and n=4 INF structure."""
import numpy as np
from scipy.optimize import least_squares
from op03_gap_fixed import lams_precise, eigfuns_precise

def make_blocks(edges, R, n, sup):
    bd = np.sort(edges)
    xs = np.concatenate(([0.0], bd, [1.0]))
    inside = np.zeros(len(xs)-1, dtype=bool)
    for k in range(n): inside[2*k+1] = True
    vals = np.where(inside, R if sup else 1.0, 1.0 if sup else R)
    return [(xs[i+1]-xs[i], vals[i]) for i in range(len(xs)-1)]

def residual(edges, R, n, sup):
    e = np.sort(edges)
    full = np.concatenate((e, 1-e[::-1]))
    blocks = make_blocks(full, R, n, sup)
    lam = lams_precise(blocks, n+2)**2
    vp = eigfuns_precise(blocks, np.sqrt(lam[n-1:n+1]), np.array(full))
    f = lam[n-1]*vp[0]**2 - lam[n]*vp[1]**2
    return f[:n]

def solve(R, n, sup, guess):
    g0 = np.sort(np.asarray(guess, dtype=float))
    sol = least_squares(residual, g0, bounds=(np.full(n,1e-4), np.full(n,0.5-1e-4)),
                        args=(R, n, sup), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=400)
    e = np.sort(sol.x)
    full = np.concatenate((e, 1-e[::-1]))
    blocks = make_blocks(full, R, n, sup)
    lam = lams_precise(blocks, n+2)**2
    return full, lam, lam[n]-lam[n-1]

print("=== n=1 large-R sweep ===")
for R in (10.0, 30.0, 100.0, 300.0, 1000.0):
    try:
        fullS, lamS, DS = solve(R, 1, True, [0.4669])
        fullI, lamI, DI = solve(R, 1, False, [0.3613])
        vS = 1-2*fullS[0]
        print(f"R={R:6.0f}: SUP u={fullS[0]:.8f} v={vS:.6f} D+={DS:.8f} | INF u={fullI[0]:.6f} D-={DI:.10f} D-*R={DI*R:.4f}")
    except Exception as ex:
        print(f"R={R}: FAILED {ex}")

print("=== n=4 INF structure (R=4): is the zero-width band real? ===")
# perturb the degenerate solution slightly and re-solve
full, lam, D = solve(4.0, 4, False, [0.1904362, 0.1905, 0.2949425, 0.4484261])
print("n=4 INF with split band:", D, np.array2string(full, precision=6))
full2, lam2, D2 = solve(4.0, 4, False, [0.19, 0.25, 0.35, 0.45])
print("n=4 INF generic seed:", D2, np.array2string(full2, precision=6))
