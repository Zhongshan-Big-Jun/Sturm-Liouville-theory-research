# -*- coding: utf-8 -*-
"""#3 redo with FIXED machinery: FH identity + self-consistent solutions."""
import numpy as np
from scipy.optimize import least_squares
from op03_gap_fixed import lams_precise, eigfuns_precise

R = 4.0
# 1) FH identity for [1,R,1], moving left junction right by eps
u = 0.30; v0 = 1-2*u
base = [(u,1.0),(v0,R),(u,1.0)]
lam0 = lams_precise(base, 3)**2
vp = eigfuns_precise(base, np.sqrt(lam0[:2]), np.array([u]))
for eps in (1e-4, 1e-5):
    pert = [(u+eps,1.0),(v0-eps,R),(u,1.0)]
    lamP = lams_precise(pert, 3)**2
    num = (lamP[:2]-lam0[:2])/eps
    pred = -lam0[:2]*(1-R)*np.array([vp[0,0]**2, vp[1,0]**2])
    print(f"FH eps={eps}: num={num} pred={pred}")

# 2) self-consistent solver
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
    return full, lam, np.max(np.abs(residual(e, R, n, sup))), lam[n]-lam[n-1]

print("=== self-consistent solutions (fixed machinery), R=4 ===")
seeds = {
    (1,True):[0.45], (1,False):[0.25],
    (2,True):[0.29,0.37], (2,False):[0.21,0.40],
    (3,True):[0.22,0.27,0.47], (3,False):[0.13,0.29,0.41],
    (4,True):[0.18,0.21,0.38,0.42], (4,False):[0.15,0.22,0.35,0.45],
}
for (n,sup), g in seeds.items():
    full, lam, res, D = solve(R, n, sup, g)
    print(f"n={n} {'SUP' if sup else 'INF'}: D={D:.10f} max|f|={res:.1e}")
    print(f"    edges={np.array2string(full, precision=7)} lam_n={lam[n-1]:.8f} lam_{n+1}={lam[n]:.8f}")
