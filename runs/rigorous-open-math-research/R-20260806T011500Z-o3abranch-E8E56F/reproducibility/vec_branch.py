# -*- coding: utf-8 -*-
"""vec_branch.py: fast good-branch exploration (vectorized over b-grid) for Lemmas A/B/C.
Uses vec_lib. Good-left root: R1=0 and v(a)>0 (sin(s2 a)>0). Good-right root: R2=0 and v(b)<0."""
import sys, time, json
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
import vec_lib as vl

def residuals_vec(a, b_grid, R):
    """R1,R2 arrays over b_grid; also s1,s2 arrays."""
    b_grid = np.atleast_1d(np.asarray(b_grid, dtype=float))
    s1, s2 = vl.roots2_bisect(a, b_grid, R, ns=3501)
    N1 = vl.norm_Y(s1, a, b_grid, R)
    N2 = vl.norm_Y(s2, a, b_grid, R)
    Y1a = np.sin(s1*a); Y2a = np.sin(s2*a)
    m = np.sqrt(R)
    th1 = s1*m*(b_grid-a); th2 = s2*m*(b_grid-a)
    Y1b = np.sin(s1*a)*np.cos(th1) + (np.cos(s1*a)/m)*np.sin(th1)
    Y2b = np.sin(s2*a)*np.cos(th2) + (np.cos(s2*a)/m)*np.sin(th2)
    R1 = s1**2*Y1a**2/N1 - s2**2*Y2a**2/N2
    R2 = s1**2*Y1b**2/N1 - s2**2*Y2b**2/N2
    return R1, R2, s1, s2

def good_left_roots(a, R, nb=600, tol=1e-9):
    """b values in (a,1) with R1=0 and sin(s2 a)>0 (good left), vectorized."""
    b_grid = np.linspace(a+1e-7, 1-1e-7, nb)
    R1, R2, s1, s2 = residuals_vec(a, b_grid, R)
    goodmask = np.isfinite(R1) & np.isfinite(s2) & (np.sin(s2*a) > 0)
    out = []
    v = np.where(goodmask, R1, np.nan)
    for i in range(nb-1):
        if v[i]*v[i+1] < 0:
            lo, hi = b_grid[i], b_grid[i+1]
            for _ in range(60):
                md = 0.5*(lo+hi)
                R1m, _, s1m, s2m = residuals_vec(a, np.array([md]), R)
                if np.isfinite(R1m[0]) and (R1m[0]*v[i] < 0):
                    hi = md
                else:
                    lo = md
            out.append(0.5*(lo+hi))
    return out

def good_right_roots(a, R, nb=600, tol=1e-9):
    b_grid = np.linspace(a+1e-7, 1-1e-7, nb)
    R1, R2, s1, s2 = residuals_vec(a, b_grid, R)
    goodmask = np.isfinite(R2) & np.isfinite(s2) & (np.sin(s2*b_grid) < 0)
    v = np.where(goodmask, R2, np.nan)
    out = []
    for i in range(nb-1):
        if v[i]*v[i+1] < 0:
            lo, hi = b_grid[i], b_grid[i+1]
            for _ in range(60):
                md = 0.5*(lo+hi)
                _, R2m, _, s2m = residuals_vec(a, np.array([md]), R)
                if np.isfinite(R2m[0]) and (R2m[0]*v[i] < 0):
                    hi = md
                else:
                    lo = md
            out.append(0.5*(lo+hi))
    return out

def branch_grid(R, na=160, alo=0.35, ahi=0.70, nb=600):
    g1 = []; g2 = []
    for a in np.linspace(alo, ahi, na):
        r1 = good_left_roots(a, R, nb=nb)
        r2 = good_right_roots(a, R, nb=nb)
        if len(r1) >= 1: g1.append((a, r1))
        if len(r2) >= 1: g2.append((a, r2))
    return g1, g2

if __name__ == "__main__":
    R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    t0 = time.time()
    g1, g2 = branch_grid(R)
    print(f"R={R}: t={time.time()-t0:.0f}s")
    # summarize per-a root counts
    for name, g in [("G1", g1), ("G2", g2)]:
        mult = [ (a, r) for (a, r) in g if len(r) > 1 ]
        print(f"{name}: a-count={len(g)}, multi-root a's: {len(mult)}")
        if g:
            arange = (min(a for a,_ in g), max(a for a,_ in g))
            print(f"{name} a-range: [{arange[0]:.5f}, {arange[1]:.5f}]")
            # sample b values
            if mult:
                print("  sample multi:", mult[:3])
    json.dump(dict(R=R, g1=[[a, r] for (a,r) in g1], g2=[[a,r] for (a,r) in g2]),
              open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\branch_{}.json".format(int(R*100)), "w"))
