# -*- coding: utf-8 -*-
"""agentB_multiseed.py: classify curve branches; multi-seed least_squares for all residual roots."""
import sys, time, json
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3')
import numpy as np
from scipy.optimize import least_squares
from agentB_lib import *

def residuals_vec(x, R):
    a, b = x
    cfg = config(a, b, R)
    return np.array([float(f_at(a,b,R,a,cfg)), float(f_at(a,b,R,b,cfg))])

def classify(a, b, R):
    z = zeros_f(a, b, R)
    if z is None:
        return "no-sign-pattern", None
    xm, xp = z
    left = abs(a-xm) < 1e-6   # a is the left zero
    right = abs(b-xp) < 1e-6  # b is the right zero
    return ("good" if (left and right) else ("left-only" if left else ("right-only" if right else "neither"))), z

def scan(R, seeds, tol=1e-9):
    sols = []
    for s0 in seeds:
        a0, b0 = s0
        if not (1e-4 < a0 and a0 < b0 and b0 < 1-1e-4): continue
        try:
            res = least_squares(lambda x: residuals_vec(x, R), [a0, b0],
                                bounds=([1e-6, a0*0+1e-6],[0.999999,0.999999]),
                                xtol=1e-11, ftol=1e-11, gtol=1e-11, max_nfev=200)
            a, b = res.x
            if np.max(np.abs(res.fun)) > tol: continue
            if not (1e-4 < a < b < 1-1e-4): continue
            kind, z = classify(a, b, R)
            sols.append((round(a,10), round(b,10), kind, float(np.max(np.abs(res.fun)))))
        except Exception as e:
            pass
    # dedupe
    uniq = {}
    for a,b,kind,resid in sols:
        key = (round(a,6), round(b,6))
        if key not in uniq:
            uniq[key] = (kind, resid)
    return uniq

if __name__ == '__main__':
    R = float(sys.argv[1]) if len(sys.argv)>1 else 4.0
    np.random.seed(0)
    seeds = []
    grid = np.linspace(0.05, 0.95, 9)
    for a in grid:
        for b in grid:
            if b > a + 0.02: seeds.append((a,b))
    for _ in range(40):
        a, b = np.random.uniform(0.02, 0.98, 2)
        if b > a + 0.02: seeds.append((a,b))
    t0=time.time()
    uniq = scan(R, seeds)
    print(f"R={R}: {len(seeds)} seeds -> {len(uniq)} distinct roots, t={time.time()-t0:.0f}s")
    for (a,b),(kind,resid) in sorted(uniq.items()):
        print(f"  (a,b)=({a:.8f},{b:.8f}) kind={kind} resid={resid:.1e}")
