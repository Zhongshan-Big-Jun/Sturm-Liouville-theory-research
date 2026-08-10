# -*- coding: utf-8 -*-
"""largeR_scan.py: good-root fixed point + branch quantities at large R, robust eigenvalue finder.
Good-root check: R1~0, R2~0, v(a)>0, v(b)<0 (sign consistency)."""
import sys, json, time
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec

def roots2_robust(a, b, R):
    s1 = np.linspace(1e-12, 1.0, 20000)
    s2 = np.linspace(1.0, 3*np.pi, 20000)
    s = np.concatenate([s1, s2])
    M = np.array([sec(si, a, b, R) for si in s])
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(90):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    roots = sorted(set(np.round(r, 14) for r in roots))
    if len(roots) < 2:
        return None
    return roots[0], roots[1]

def lam_norm_v(a, b, R):
    rr = roots2_robust(a, b, R)
    if rr is None: return None
    s1, s2 = rr
    from clean_lib import norm_n, y_at
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    R1 = s1*s1*y1a*y1a/n1 - s2*s2*y2a*y2a/n2
    R2 = s1*s1*y1b*y1b/n1 - s2*s2*y2b*y2b/n2
    va = y2a/y1a; vb = y2b/y1b
    return dict(s1=s1, s2=s2, l1=s1*s1, l2=s2*s2, R1=R1, R2=R2, va=va, vb=vb)

def good_fp(R, seeds=None):
    from scipy.optimize import least_squares
    if seeds is None:
        seeds = [(0.499, 0.501), (0.49, 0.51), (0.48, 0.52), (0.45, 0.55), (0.4, 0.6)]
    def res(p):
        a, b = p
        if not (1e-8 < a < b < 1-1e-8): return [1e3, 1e3]
        info = lam_norm_v(a, b, R)
        if info is None: return [1e3, 1e3]
        return [info['R1'], info['R2']]
    out = []
    for seed in seeds:
        try:
            sol = least_squares(res, seed, bounds=([1e-8,1e-8],[1-1e-8,1-1e-8]), xtol=1e-13, ftol=1e-13, max_nfev=4000)
            a, b = sol.x
            info = lam_norm_v(a, b, R)
            if info is None: continue
            good = (abs(info['R1']) < 1e-6 and abs(info['R2']) < 1e-6 and info['va'] > 0 and info['vb'] < 0)
            if good:
                out.append((a, b, info))
        except Exception:
            continue
    # dedupe
    seen = []
    for item in out:
        a, b, info = item
        if not any(abs(a-a2) < 1e-8 for (a2, b2, _) in seen):
            seen.append(item)
    return seen

def hprime_at_fp(a, b, R, h=1e-6):
    """g1' - g2' at the fixed point using branch-side finite differences (A,B,C)."""
    def R1v(aa, bb):
        info = lam_norm_v(aa, bb, R)
        return info['R1'] if info else np.nan
    def R2v(aa, bb):
        info = lam_norm_v(aa, bb, R)
        return info['R2'] if info else np.nan
    A = (R1v(a+h,b)-R1v(a-h,b))/(2*h)
    B = (R2v(a+h,b)-R2v(a-h,b))/(2*h)
    C = (R2v(a,b+h)-R2v(a,b-h))/(2*h)
    g1p = A/B; g2p = -B/C
    return g1p, g2p, g1p-g2p

if __name__ == "__main__":
    Rs = [float(x) for x in sys.argv[1:]] or [50.0, 100.0, 200.0, 500.0, 1000.0, 5000.0, 1e4, 1e5, 1e6]
    results = []
    for R in Rs:
        t0 = time.time()
        fps = good_fp(R)
        row = dict(R=R, n_fp=len(fps))
        if fps:
            a, b, info = fps[0]
            row.update(a=a, b=b, delta=0.5-a, l1=info['l1'], l2=info['l2'], D=info['l2']-info['l1'],
                       R1=info['R1'], R2=info['R2'], va=info['va'], vb=info['vb'], s1=info['s1'], s2=info['s2'])
            g1p, g2p, hp = hprime_at_fp(a, b, R)
            row.update(g1p=g1p, g2p=g2p, hp=hp)
            row['Rdelta'] = R*(0.5-a)
        print(json.dumps(row))
        results.append(row)
    with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\largeR_scan.json", "w") as f:
        json.dump(results, f, indent=1)
    print("saved largeR_scan.json")
