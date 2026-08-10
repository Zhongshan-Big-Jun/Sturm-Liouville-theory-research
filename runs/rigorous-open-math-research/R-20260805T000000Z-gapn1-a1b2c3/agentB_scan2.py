# -*- coding: utf-8 -*-
"""agentB_scan2.py: multi-seed residual scan with (a,w) parameterization (a<b enforced)."""
import sys, time, json
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3')
import numpy as np
from scipy.optimize import least_squares
from agentB_lib import *

def resid(x, R):
    a, w = x
    b = a + w
    if not (1e-6 < a and 1e-6 < w and b < 1-1e-6):
        return np.array([1e3, 1e3])
    cfg = config(a, b, R)
    return np.array([float(f_at(a,b,R,a,cfg)), float(f_at(a,b,R,b,cfg))])

def classify(a, b, R):
    z = zeros_f(a, b, R)
    if z is None: return "no-sign-pattern"
    xm, xp = z
    if abs(a-xm) < 1e-6 and abs(b-xp) < 1e-6: return "good"
    if abs(a-xm) < 1e-6: return "left-only"
    if abs(b-xp) < 1e-6: return "right-only"
    return "neither"

if __name__ == '__main__':
    R = float(sys.argv[1])
    nseeds = int(sys.argv[2]) if len(sys.argv)>2 else 60
    rng = np.random.default_rng(42)
    seeds = []
    grid = np.linspace(0.03, 0.95, 11)
    for a in grid:
        for w in np.linspace(0.03, 0.95, 11):
            if a + w < 0.999: seeds.append((a, w))
    for _ in range(nseeds):
        a = rng.uniform(0.01, 0.98); w = rng.uniform(0.01, 0.98-a)
        seeds.append((a, w))
    sols = {}
    t0=time.time()
    for (a0, w0) in seeds:
        try:
            res = least_squares(lambda x: resid(x, R), [a0, w0], bounds=([1e-6,1e-6],[0.999,0.999]),
                                xtol=1e-11, ftol=1e-11, gtol=1e-11, max_nfev=120)
            a, w = res.x; b = a+w
            if np.max(np.abs(res.fun)) > 1e-7: continue
            if not (1e-6 < a < b < 1-1e-6): continue
            kind = classify(a, b, R)
            key = (round(a,6), round(b,6))
            sols[key] = (kind, float(np.max(np.abs(res.fun))))
        except Exception:
            pass
    print(f"R={R}: {len(seeds)} seeds -> {len(sols)} roots, t={time.time()-t0:.0f}s")
    for (a,b),(kind,resd) in sorted(sols.items()):
        print(f"  (a,b)=({a:.8f},{b:.8f}) kind={kind} resid={resd:.1e}")
