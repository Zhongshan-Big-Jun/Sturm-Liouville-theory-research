# -*- coding: utf-8 -*-
"""#3: verify band structure + R-sweep for n=1 with fixed machinery."""
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

def band_check(full, R, n, sup):
    blocks = make_blocks(full, R, n, sup)
    lam = lams_precise(blocks, n+2)**2
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    pts = np.array(sorted(set(np.round(np.linspace(3e-4, 1-3e-4, 400), 6))))
    vp = eigfuns_precise(blocks, np.sqrt(lam[n-1:n+1]), pts)
    f = lam[n-1]*vp[0]**2 - lam[n]*vp[1]**2
    rho_pred = np.where(f > 0, R if sup else 1.0, 1.0 if sup else R)
    rho_true = np.zeros_like(pts)
    for i, p in enumerate(pts):
        for j in range(len(xs)-1):
            if xs[j] <= p <= xs[j+1]: rho_true[i] = blocks[j][1]; break
    return np.mean(rho_pred == rho_true)

print("=== R=4 band checks ===")
cfgs = {
    (1,True):[0.4514855], (1,False):[0.3825983],
    (2,True):[0.2934344,0.3654607], (2,False):[0.2028824,0.4040382],
    (3,True):[0.2202494,0.2731374,0.4691661], (3,False):[0.130447,0.2875056,0.411388],
    (4,True):[0.1775259,0.2182728,0.3743985,0.4242345],
}
for (n,sup), g in cfgs.items():
    full = np.concatenate((np.sort(g), 1-np.sort(g)[::-1]))
    m = band_check(full, 4.0, n, sup)
    print(f"n={n} {'SUP' if sup else 'INF'}: band-match={m:.4f}")

print("=== n=1 R-sweep (SUP [1,R,1], INF [R,1,R]) ===")
for R in (1.5, 2.0, 3.0, 4.0, 10.0, 100.0):
    # seeds scale ~ from R=4 solution; guess by continuity
    g_sup = [0.4514855]; g_inf = [0.3825983]
    fullS, lamS, DS = solve(R, 1, True, g_sup)
    fullI, lamI, DI = solve(R, 1, False, g_inf)
    print(f"R={R:7.2f}: SUP u={fullS[0]:.6f} D+={DS:.8f}  (3pi^2={3*np.pi**2:.4f})  | INF u={fullI[0]:.6f} D-={DI:.8f} (3pi^2/R={3*np.pi**2/R:.6f})")
