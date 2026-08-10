# -*- coding: utf-8 -*-
"""largeR_scan2.py: fixed-point scan with v-based sign check and zero verification.
delta ~ 0.118/sqrt(R) informed seeds; tight residual tolerance."""
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
    if len(roots) < 2: return None
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

def v_at(a, b, R, x):
    rr = roots2_robust(a, b, R)
    if rr is None: return None
    s1, s2 = rr
    from clean_lib import y_at
    y1 = y_at(s1, a, b, R, x); y2 = y_at(s2, a, b, R, x)
    return y2/y1

def zeros_v(a, b, R, info):
    """x_-, x_+ via v = +/- q, q = (s1/s2)*sqrt(n2/n1); v monotone."""
    s1, s2 = info['s1'], info['s2']
    from clean_lib import norm_n
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    q = (s1/s2)*np.sqrt(n2/n1)
    # bisection on v - q and v + q
    def vv(x): return v_at(a, b, R, x)
    lo, hi = 1e-9, 1-1e-9
    # x_-: v(x)=q (v decreasing from 1 to <0); exists iff v(lo)>q>v(hi)
    if not (vv(lo) > q > vv(hi)): return None
    l, h = lo, hi
    for _ in range(90):
        md = 0.5*(l+h)
        if vv(md) > q: l = md
        else: h = md
    xm = 0.5*(l+h)
    # x_+: v(x)=-q
    if not (vv(lo) > -q > vv(hi)): return None
    l, h = lo, hi
    for _ in range(90):
        md = 0.5*(l+h)
        if vv(md) > -q: l = md
        else: h = md
    xp = 0.5*(l+h)
    return xm, xp

def good_fp(R):
    from scipy.optimize import least_squares
    dhat = 0.118/np.sqrt(R)
    seeds = [(0.5-dhat, 0.5+dhat), (0.5-2*dhat, 0.5+2*dhat), (0.5-dhat/2, 0.5+dhat/2),
             (0.499, 0.501), (0.495, 0.505), (0.49, 0.51), (0.45, 0.55), (0.48, 0.52)]
    def res(p):
        a, b = p
        if not (1e-8 < a < b < 1-1e-8): return [1e3, 1e3]
        info = lam_norm_v(a, b, R)
        if info is None: return [1e3, 1e3]
        return [info['R1'], info['R2']]
    out = []
    for seed in seeds:
        try:
            sol = least_squares(res, seed, bounds=([1e-8,1e-8],[1-1e-8,1-1e-8]), xtol=1e-14, ftol=1e-14, max_nfev=6000)
            a, b = sol.x
            info = lam_norm_v(a, b, R)
            if info is None: continue
            good = (abs(info['R1']) < 1e-9 and abs(info['R2']) < 1e-9 and info['va'] > 0 and info['vb'] < 0)
            if not good: continue
            z = zeros_v(a, b, R, info)
            if z is None: continue
            xm, xp = z
            if abs(xm-a) > 1e-7 or abs(xp-b) > 1e-7: continue
            out.append((a, b, info, xm, xp))
        except Exception:
            continue
    seen = []
    for item in out:
        a, b, info, xm, xp = item
        if not any(abs(a-a2) < 1e-8 for (a2, b2, _, _, _) in seen):
            seen.append(item)
    return seen

def hprime(a, b, R, h=1e-6):
    def R1v(aa, bb):
        info = lam_norm_v(aa, bb, R)
        return info['R1'] if info else np.nan
    def R2v(aa, bb):
        info = lam_norm_v(aa, bb, R)
        return info['R2'] if info else np.nan
    A = (R1v(a+h,b)-R1v(a-h,b))/(2*h)
    B = (R2v(a+h,b)-R2v(a-h,b))/(2*h)
    C = (R2v(a,b+h)-R2v(a,b-h))/(2*h)
    return A, B, C, A/B, -B/C, A/B + B/C

if __name__ == "__main__":
    Rs = [float(x) for x in sys.argv[1:]] or [50.0, 100.0, 200.0, 500.0, 1000.0, 5000.0, 1e4, 1e5, 1e6, 1e7]
    results = []
    for R in Rs:
        t0 = time.time()
        fps = good_fp(R)
        row = dict(R=R, n_fp=len(fps))
        if fps:
            a, b, info, xm, xp = fps[0]
            row.update(a=a, b=b, delta=0.5-a, l1=info['l1'], l2=info['l2'], D=info['l2']-info['l1'],
                       va=info['va'], vb=info['vb'], xm=xm, xp=xp, Rdelta=R*(0.5-a))
            A, B, C, g1p, g2p, hp = hprime(a, b, R)
            row.update(A=A, B=B, C=C, g1p=g1p, g2p=g2p, hp=hp)
        print(json.dumps(row, default=float))
        results.append(row)
    with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\largeR_scan2.json", "w") as f:
        json.dump(results, f, indent=1)
    print("saved largeR_scan2.json")
