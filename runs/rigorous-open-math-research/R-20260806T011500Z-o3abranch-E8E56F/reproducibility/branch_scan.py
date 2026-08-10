# -*- coding: utf-8 -*-
"""branch_scan.py v2: parallel good-branch scan + local branch evaluation."""
import sys, time, json
import numpy as np
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from vec_lib import residuals_vec

def both_roots_at(a, R, nb=500, ns=2501):
    b_grid = np.linspace(a+1e-7, 1-1e-7, nb)
    R1, R2, s1, s2 = residuals_vec(a, b_grid, R, ns=ns)
    goodL = np.isfinite(R1) & np.isfinite(s2) & (np.sin(s2*a) > 0)
    goodR = np.isfinite(R2) & np.isfinite(s2) & (np.sin(s2*b_grid) < 0)
    vL = np.where(goodL, R1, np.nan)
    vR = np.where(goodR, R2, np.nan)
    outL = []; outR = []
    for i in range(nb-1):
        if vL[i]*vL[i+1] < 0:
            lo, hi = b_grid[i], b_grid[i+1]
            for _ in range(60):
                md = 0.5*(lo+hi)
                r = residuals_vec(a, np.array([md]), R, ns=1501)[0][0]
                if np.isfinite(r) and r*vL[i] < 0: hi = md
                else: lo = md
            outL.append(0.5*(lo+hi))
        if vR[i]*vR[i+1] < 0:
            lo, hi = b_grid[i], b_grid[i+1]
            for _ in range(60):
                md = 0.5*(lo+hi)
                r = residuals_vec(a, np.array([md]), R, ns=1501)[1][0]
                if np.isfinite(r) and r*vR[i] < 0: hi = md
                else: lo = md
            outR.append(0.5*(lo+hi))
    return a, outL, outR

def scan_R(R, na=120, alo=0.35, ahi=0.75, workers=8):
    aa = np.linspace(alo, ahi, na)
    g1 = []; g2 = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(both_roots_at, float(a), R) for a in aa]
        for f in futs:
            a, outL, outR = f.result()
            if outL: g1.append((a, outL))
            if outR: g2.append((a, outR))
    g1.sort(); g2.sort()
    return g1, g2

if __name__ == "__main__":
    Rs = [float(x) for x in sys.argv[1:]] or [1.05, 2.0, 4.0, 10.0, 100.0]
    for R in Rs:
        t0 = time.time()
        g1, g2 = scan_R(R)
        print(f"R={R}: t={time.time()-t0:.0f}s")
        for name, g in [("G1", g1), ("G2", g2)]:
            mult = [(a, r) for (a, r) in g if len(r) > 1]
            if not g:
                print(f"  {name}: EMPTY"); continue
            ar = (min(a for a, _ in g), max(a for a, _ in g))
            bvals = [r[0] for (a, r) in g if len(r) == 1]
            br = (min(bvals), max(bvals)) if bvals else None
            print(f"  {name}: a-range [{ar[0]:.5f},{ar[1]:.5f}] multi={len(mult)}"
                  + (f" b-range [{(round(br[0],5), round(br[1],5))}]" if br else ""))
            if mult:
                print(f"    multi examples: {[(round(a,4), [round(x,4) for x in r]) for a, r in mult[:4]]}")
