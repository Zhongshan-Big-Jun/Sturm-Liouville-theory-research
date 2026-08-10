# -*- coding: utf-8 -*-
"""#3: large-R SUP with better seeds; n=4 INF level-set structure."""
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
                        args=(R, n, sup), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=600)
    e = np.sort(sol.x)
    full = np.concatenate((e, 1-e[::-1]))
    blocks = make_blocks(full, R, n, sup)
    lam = lams_precise(blocks, n+2)**2
    return full, lam, lam[n]-lam[n-1]

print("=== n=1 SUP large R (seeds near 0.485) ===")
for R in (30.0, 100.0, 300.0, 1000.0, 3000.0):
    try:
        fullS, lamS, DS = solve(R, 1, True, [0.485])
        print(f"R={R:5.0f}: u={fullS[0]:.8f} v={1-2*fullS[0]:.6f} D+={DS:.8f}")
    except Exception as ex:
        print(f"R={R}: FAILED {ex}")

print("=== n=4 INF (R=4): components of {f>0} ===")
full, lam, D = solve(4.0, 4, False, [0.1904362, 0.2949425, 0.4484261, 0.51])
blocks = make_blocks(full, 4.0, 4, False)
pts = np.linspace(5e-4, 1-5e-4, 2001)
vp = eigfuns_precise(blocks, np.sqrt(lam[3:5]), pts)
f = lam[3]*vp[0]**2 - lam[4]*vp[1]**2
pos = f > 0
edges_idx = np.nonzero(pos[1:] != pos[:-1])[0] + 1
bounds = [0.0] + [pts[i] for i in edges_idx] + [1.0]
comps = []
for i in range(len(bounds)-1):
    if pos[(np.abs(pts-0.5*(bounds[i]+bounds[i+1]))).argmin()]:
        comps.append((bounds[i], bounds[i+1]))
print(f"D={D:.6f}, {len(comps)} components of {{f>0}}: {[f'({a:.4f},{b:.4f})' for a,b in comps]}")
print("config bands (rho=1):")
xs = [0.0]
for L, c in blocks: xs.append(xs[-1]+L)
for i in range(len(xs)-1):
    if blocks[i][1] == 1.0:
        print(f"  ({xs[i]:.4f},{xs[i+1]:.4f})")
