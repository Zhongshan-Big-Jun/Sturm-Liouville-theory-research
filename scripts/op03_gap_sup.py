# -*- coding: utf-8 -*-
"""#3: SUP via bounded optimization of D over band edges (Powell)."""
import numpy as np
from scipy.optimize import minimize
from op03_gap_n1 import lams_blocks

def make_blocks_from_edges(edges, R, n, sup):
    bd = np.sort(edges)
    xs = np.concatenate(([0.0], bd, [1.0]))
    inside = np.zeros(len(xs)-1, dtype=bool)
    for k in range(n):
        inside[2*k+1] = True
    vals = np.where(inside, R if sup else 1.0, 1.0 if sup else R)
    return [(xs[i+1]-xs[i], vals[i]) for i in range(len(xs)-1)]

def negD(e, R, n, sup):
    e = np.sort(np.clip(e, 1e-4, 0.5-1e-4))
    full = np.concatenate((e, 1 - e[::-1]))
    blocks = make_blocks_from_edges(full, R, n, sup)
    lam = lams_blocks(blocks, k=n+2)
    return -(lam[n]-lam[n-1])

def solve_sup(R, n, guess):
    e0 = np.sort(guess)
    best = (1e9, None)
    for shift in (0.0, 0.01, -0.01, 0.02):
        e0s = np.clip(e0 + shift, 0.02, 0.49)
        r = minimize(negD, e0s, args=(R, n, True), method='Powell',
                     options={'xtol':1e-12, 'ftol':1e-12, 'maxiter':3000})
        if r.fun < best[0]:
            best = (r.fun, r.x)
    e = np.sort(np.clip(best[1], 1e-4, 0.5-1e-4))
    full = np.concatenate((e, 1 - e[::-1]))
    blocks = make_blocks_from_edges(full, R, n, True)
    lam = lams_blocks(blocks, k=n+2)
    return full, lam, lam[n]-lam[n-1]

for n, guess in [(3, [0.184, 0.280, 0.444]), (4, [0.143, 0.220, 0.346, 0.438]), (5, [0.12, 0.18, 0.28, 0.34, 0.42])]:
    full, lam, D = solve_sup(R=4.0, n=n, guess=guess)
    print(f"n={n} SUP: D={D:.8f}")
    print(f"   edges={np.array2string(full, precision=6)}")
    print(f"   lam_n={lam[n-1]:.8f} lam_{n+1}={lam[n]:.8f}")
    print(f"   (2n+1)pi^2={ (2*n+1)*np.pi**2:.6f}")
