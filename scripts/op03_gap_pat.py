# -*- coding: utf-8 -*-
"""#3: n=3,4 SUP via pattern search over band edges (high-precision D)."""
import numpy as np
from op03_gap_n1 import lams_blocks

def make_blocks_from_edges(edges, R, n, sup):
    bd = np.sort(edges)
    xs = np.concatenate(([0.0], bd, [1.0]))
    inside = np.zeros(len(xs)-1, dtype=bool)
    for k in range(n):
        inside[2*k+1] = True
    vals = np.where(inside, R if sup else 1.0, 1.0 if sup else R)
    return [(xs[i+1]-xs[i], vals[i]) for i in range(len(xs)-1)]

def D_of(e, R, n, sup):
    e = np.sort(np.clip(e, 2e-3, 0.5-2e-3))
    full = np.concatenate((e, 1 - e[::-1]))
    blocks = make_blocks_from_edges(full, R, n, sup)
    lam = lams_blocks(blocks, k=n+2)
    return lam[n]-lam[n-1]

def pattern_search(R, n, sup, x0, steps, nrounds=60):
    x = np.array(x0, dtype=float)
    best = -D_of(x, R, n, sup)
    for it in range(nrounds):
        improved = False
        for i in range(n):
            for sgn in (1.0, -1.0):
                xt = x.copy(); xt[i] += sgn*steps[i]
                if xt[i] < 2e-3 or xt[i] > 0.5-2e-3: continue
                v = -D_of(xt, R, n, sup)
                if v < best:
                    best = v; x = xt; improved = True
        for i in range(n):
            if steps[i] > 1e-9:
                steps[i] *= 0.5
        if not improved and max(steps) < 2e-5:
            break
    return x, -best

R = 4.0
for n, x0 in [(3, [0.184, 0.280, 0.444]), (4, [0.143, 0.220, 0.346, 0.438])]:
    x, D = pattern_search(R, n, True, x0, [0.02]*n)
    full = np.concatenate((np.sort(x), 1 - np.sort(x)[::-1]))
    print(f"n={n} SUP: D={D:.8f} edges={np.array2string(full, precision=6)}")
    # also constant comparison
    print(f"   (2n+1)pi^2 = {(2*n+1)*np.pi**2:.6f}")
