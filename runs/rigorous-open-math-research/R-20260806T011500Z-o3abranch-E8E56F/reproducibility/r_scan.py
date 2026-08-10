# -*- coding: utf-8 -*-
"""r_scan.py: systematic R-scan of fp, common range, h endpoint signs, min h'."""
import sys, time, json
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from local_branch import g1_at, g2_at, deriv_abc, R1, R2
from scipy.optimize import least_squares

def fp_find(R, seed=None):
    if seed is None: seed = (0.45, 0.55)
    def res(p):
        a, b = p
        if not (1e-6 < a < b < 1-1e-6): return [1e3, 1e3]
        return [R1(a,b,R), R2(a,b,R)]
    sol = least_squares(res, seed, bounds=([1e-6,1e-6],[1-1e-6,1-1e-6]), xtol=1e-14, ftol=1e-14)
    return tuple(sol.x)

def common_range(R, alo=0.30, ahi=0.75, na=200, tol_exist=0.02):
    """find [amin, amax] where both branches exist, by scanning a-grid."""
    aa = np.linspace(alo, ahi, na)
    have = []
    for a in aa:
        g1 = g1_at(a, R); g2 = g2_at(a, R)
        if g1 is not None and g2 is not None:
            have.append(a)
    if not have:
        return None, None
    amin, amax = min(have), max(have)
    # refine left endpoint
    lo, hi = alo, amin
    for _ in range(40):
        md = 0.5*(lo+hi)
        if g1_at(md, R) is not None and g2_at(md, R) is not None: hi = md
        else: lo = md
    amin = hi
    lo, hi = amax, ahi
    for _ in range(40):
        md = 0.5*(lo+hi)
        if g1_at(md, R) is not None and g2_at(md, R) is not None: lo = md
        else: hi = md
    amax = lo
    return amin, amax

def scan_R(R):
    fp = fp_find(R)
    amin, amax = common_range(R)
    out = dict(R=R, fp=list(fp))
    if amin is None:
        out['common_range'] = None
        return out
    out['common_range'] = [amin, amax]
    # h at endpoints
    g1l, g2l = g1_at(amin, R), g2_at(amin, R)
    g1r, g2r = g1_at(amax, R), g2_at(amax, R)
    out['h_left'] = g1l - g2l; out['h_right'] = g1r - g2r
    # h' on a grid over common range
    aa = np.linspace(amin, amax, 40)
    hps = []
    for a in aa:
        g1 = g1_at(a, R); g2 = g2_at(a, R)
        if g1 is None or g2 is None: continue
        A1, B1, C1, _ = deriv_abc(a, g1, R)
        A2, B2, C2, _ = deriv_abc(a, g2, R)
        g1p = A1/B1; g2p = -B2/C2
        hps.append((a, g1p, g2p, g1p-g2p))
    hps = np.array(hps)
    out['min_hp'] = float(hps[:,3].min())
    out['argmin_hp'] = float(hps[hps[:,3].argmin(), 0])
    out['hp_at_fp'] = None
    if fp:
        a0, b0 = fp
        if amin <= a0 <= amax:
            A1, B1, C1, _ = deriv_abc(a0, b0, R)
            g1p = A1/B1; g2p = -B1/C1
            out['hp_at_fp'] = g1p - g2p
    # A,B,C signs along branches (sample)
    signs = []
    for a in np.linspace(amin, amax, 12):
        g1 = g1_at(a, R); g2 = g2_at(a, R)
        A1, B1, C1, R1b = deriv_abc(a, g1, R)
        A2, B2, C2, _ = deriv_abc(a, g2, R)
        signs.append(dict(a=a, A1=A1, B1=B1, C1=C1, T3=R1b+B1, A2=A2, B2=B2, C2=C2))
    out['signs'] = signs
    return out

if __name__ == "__main__":
    Rs = [float(x) for x in sys.argv[1:]] or [1.05, 1.5, 2.0, 3.0, 4.0, 10.0, 100.0]
    results = []
    for R in Rs:
        t0 = time.time()
        out = scan_R(R)
        print(f"R={R}: fp={out['fp']} common={out.get('common_range')} h_left={out.get('h_left'):+.5f} h_right={out.get('h_right'):+.5f} min_hp={out.get('min_hp'):.5f} argmin={out.get('argmin_hp'):.5f} hp_fp={out.get('hp_at_fp')} t={time.time()-t0:.0f}s")
        results.append(out)
    json.dump(results, open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\r_scan.json", "w"), indent=1)
