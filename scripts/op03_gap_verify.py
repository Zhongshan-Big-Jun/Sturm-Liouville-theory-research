# -*- coding: utf-8 -*-
"""#3: verify self-consistency of pattern-search configs + n=1 R-sweep."""
import numpy as np
from op03_gap_n1 import lams_blocks, eigfuns_at

def make_blocks_from_edges(edges, R, n, sup):
    bd = np.sort(edges)
    xs = np.concatenate(([0.0], bd, [1.0]))
    inside = np.zeros(len(xs)-1, dtype=bool)
    for k in range(n):
        inside[2*k+1] = True
    vals = np.where(inside, R if sup else 1.0, 1.0 if sup else R)
    return [(xs[i+1]-xs[i], vals[i]) for i in range(len(xs)-1)]

def verify(full, R, n, sup):
    blocks = make_blocks_from_edges(full, R, n, sup)
    lam = lams_blocks(blocks, k=n+2)
    pts = np.array(full)
    vals = eigfuns_at(blocks, lam[n-1:n+1], pts)
    f_bd = lam[n-1]*vals[0]**2 - lam[n]*vals[1]**2
    # interior check on fine grid
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    g = np.linspace(2e-4, 1-2e-4, 600)
    vg = eigfuns_at(blocks, lam[n-1:n+1], g)
    fg = lam[n-1]*vg[0]**2 - lam[n]*vg[1]**2
    # check fg>0 exactly on R-bands
    rho_pred = np.where(fg > 0, R if sup else 1.0, 1.0 if sup else R)
    rho_true = np.zeros_like(g)
    for i, p in enumerate(g):
        for j in range(len(xs)-1):
            if xs[j] <= p <= xs[j+1]:
                rho_true[i] = blocks[j][1]; break
    match = np.mean(rho_pred == rho_true)
    return lam, f_bd, match, lam[n]-lam[n-1]

print("=== R=4 verification ===")
configs = {
    (1,True): np.array([0.4514855879]),
    (1,False): np.array([0.3825991113]),
    (2,True): np.array([0.293435, 0.365461]),
    (2,False): np.array([0.202883, 0.404038]),
    (3,True): np.array([0.22025, 0.273125, 0.469156]),
    (3,False): np.array([0.130448, 0.287505, 0.411388]),
    (4,True): np.array([0.177375, 0.218208, 0.374392, 0.424211]),
    (4,False): np.array([0.19044, 0.29494, 0.44843]),
}
for (n, sup), e in configs.items():
    full = np.concatenate((e, 1 - e[::-1]))
    lam, f_bd, match, D = verify(full, 4.0, n, sup)
    print(f"n={n} {'SUP' if sup else 'INF'}: D={D:.8f} |f(bd)|max={np.max(np.abs(f_bd)):.2e} band-match={match:.4f}")
