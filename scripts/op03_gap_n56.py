# -*- coding: utf-8 -*-
"""#3: n=5,6 SUP/INF at R=4 (fixed machinery)."""
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
    g0 = np.sort(np.clip(np.asarray(guess, dtype=float), 3e-4, 0.5-3e-4))
    sol = least_squares(residual, g0, bounds=(np.full(n,1e-4), np.full(n,0.5-1e-4)),
                        args=(R, n, sup), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=1000)
    e = np.sort(sol.x)
    full = np.concatenate((e, 1-e[::-1]))
    blocks = make_blocks(full, R, n, sup)
    lam = lams_precise(blocks, n+2)**2
    return full, lam, lam[n]-lam[n-1]

R = 4.0
for n, seed_sup, seed_inf in [
    (5, [0.145,0.175,0.30,0.33,0.44], [0.10,0.16,0.24,0.30,0.40]),
    (6, [0.12,0.145,0.25,0.28,0.37,0.40], [0.08,0.13,0.20,0.25,0.33,0.38]),
]:
    try:
        fullS, lamS, DS = solve(R, n, True, seed_sup)
        fullI, lamI, DI = solve(R, n, False, seed_inf)
        print(f"n={n}: SUP D={DS:.8f} edges={np.array2string(fullS, precision=5)}")
        print(f"      INF D={DI:.8f} edges={np.array2string(fullI, precision=5)}")
        print(f"      (2n+1)pi^2={(2*n+1)*np.pi**2:.4f}  (2n+1)pi^2/R={(2*n+1)*np.pi**2/R:.4f}")
    except Exception as ex:
        print(f"n={n}: FAILED {ex}")
