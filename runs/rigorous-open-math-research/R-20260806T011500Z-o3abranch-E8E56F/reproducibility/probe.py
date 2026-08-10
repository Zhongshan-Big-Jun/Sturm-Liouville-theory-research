# -*- coding: utf-8 -*-
"""probe.py: fast per-a branch probes using vec_lib; branch endpoints by bisection."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from vec_lib import residuals_vec

def roots_at(a, R, nb=500, ns=1501):
    b_grid = np.linspace(a+1e-7, 1-1e-7, nb)
    R1, R2, s1, s2, Y1b, Y2b = residuals_vec(a, b_grid, R, ns=ns)
    goodL = np.isfinite(R1) & np.isfinite(s2) & (np.sin(s2*a) > 0)
    goodR = np.isfinite(R2) & np.isfinite(s2) & (np.signbit(Y2b) != np.signbit(Y1b))
    vL = np.where(goodL, R1, np.nan)
    vR = np.where(goodR, R2, np.nan)
    outL = []; outR = []
    for i in range(nb-1):
        if not np.isnan(vL[i]) and not np.isnan(vL[i+1]) and vL[i]*vL[i+1] < 0:
            lo, hi = b_grid[i], b_grid[i+1]
            for _ in range(70):
                md = 0.5*(lo+hi)
                r = residuals_vec(a, np.array([md]), R, ns=801)[0][0]
                if np.isfinite(r) and r*vL[i] < 0: hi = md
                else: lo = md
            outL.append(0.5*(lo+hi))
        if not np.isnan(vR[i]) and not np.isnan(vR[i+1]) and vR[i]*vR[i+1] < 0:
            lo, hi = b_grid[i], b_grid[i+1]
            for _ in range(70):
                md = 0.5*(lo+hi)
                r = residuals_vec(a, np.array([md]), R, ns=801)[1][0]
                if np.isfinite(r) and r*vR[i] < 0: hi = md
                else: lo = md
            outR.append(0.5*(lo+hi))
    g1 = outL[0] if len(outL) == 1 else (outL if outL else None)
    g2 = outR[0] if len(outR) == 1 else (outR if outR else None)
    return g1, g2

def left_endpoint_g1(R, lo=0.30, hi=0.47):
    found = None
    for a in np.linspace(lo, hi, 40):
        g1, _ = roots_at(a, R, nb=300, ns=1201)
        if g1 is not None and not isinstance(g1, list):
            found = a; break
    if found is None:
        return None
    lo2, hi2 = lo, found
    for _ in range(50):
        md = 0.5*(lo2+hi2)
        g1, _ = roots_at(md, R, nb=200, ns=1001)
        ok = g1 is not None and not isinstance(g1, list)
        if ok: hi2 = md
        else: lo2 = md
    return hi2

def right_endpoint(R, which, lo_hint=0.5, hi_hint=0.85):
    def has(a):
        g1, g2 = roots_at(a, R, nb=300, ns=1201)
        g = g1 if which == "G1" else g2
        return g is not None and not isinstance(g, list)
    last_ok = None
    for a in np.linspace(lo_hint, hi_hint, 80):
        if has(a): last_ok = a
        else: break
    if last_ok is None:
        return None
    lo2, hi2 = last_ok, min(last_ok + (hi_hint-lo_hint)/80*2.5, hi_hint)
    for _ in range(50):
        md = 0.5*(lo2+hi2)
        if has(md): lo2 = md
        else: hi2 = md
    return lo2

if __name__ == "__main__":
    import time
    R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    t0 = time.time()
    aL = left_endpoint_g1(R)
    print(f"R={R}: left endpoint of G1 = {aL} (t={time.time()-t0:.0f}s)")
    t0 = time.time()
    aR1 = right_endpoint(R, "G1")
    aR2 = right_endpoint(R, "G2")
    print(f"right endpoint G1 = {aR1}, G2 = {aR2} (t={time.time()-t0:.0f}s)")
    amin = aL; amax = min(aR1, aR2)
    print(f"common range [{amin:.6f}, {amax:.6f}]")
    for a in np.linspace(amin, amax, 7):
        g1, g2 = roots_at(a, R)
        print(f"  a={a:.6f}: g1={g1 if not isinstance(g1,list) else [round(x,5) for x in g1]}, g2={g2 if not isinstance(g2,list) else [round(x,5) for x in g2]}")
