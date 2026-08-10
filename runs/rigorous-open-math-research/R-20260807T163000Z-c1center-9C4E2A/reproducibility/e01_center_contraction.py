# -*- coding: utf-8 -*-
"""e01_center_contraction.py v2 (fast): monotone bisection on v = y2/y1.
Conjecture: XC = (x_+ + x_-)/2 satisfies dXC/da + dXC/db < 1 on the triangle.
"""
import numpy as np, sys, json, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T200000Z-o3a-c1b-7F3A9B\reproducibility")
from c1_lib import cfg, y_at

def qval(a, b, R):
    s1, s2, n1, n2 = cfg(a, b, R)
    return np.sqrt((s1**2/n1)/(s2**2/n2))

def v(x, s1, s2, a, b, R):
    return y_at(s2, a, b, R, x)/y_at(s1, a, b, R, x)

def xcross(a, b, R, target, lo=1e-9, hi=1-1e-9):
    """unique root of v(x) = target (v strictly decreasing)"""
    s1, s2, _, _ = cfg(a, b, R)
    def g(x): return v(x, s1, s2, a, b, R) - target
    gl = g(lo)
    for _ in range(70):
        md = 0.5*(lo+hi)
        if np.signbit(g(md)) == np.signbit(gl):
            lo = md
        else:
            hi = md
    return 0.5*(lo+hi)

def xzeros_fast(a, b, R):
    q = qval(a, b, R)
    return xcross(a, b, R, q), xcross(a, b, R, -q)  # x_-, x_+

def dXC(a, b, R, h=1e-6):
    xm, xp = xzeros_fast(a, b, R)
    xm_a = (xzeros_fast(a+h, b, R)[0] - xzeros_fast(a-h, b, R)[0])/(2*h)
    xm_b = (xzeros_fast(a, b+h, R)[0] - xzeros_fast(a, b-h, R)[0])/(2*h)
    xp_a = (xzeros_fast(a+h, b, R)[1] - xzeros_fast(a-h, b, R)[1])/(2*h)
    xp_b = (xzeros_fast(a, b+h, R)[1] - xzeros_fast(a, b-h, R)[1])/(2*h)
    return dict(xm=xm, xp=xp, sum=(xp_a+xm_a+xp_b+xm_b)/2,
                dxm_da=xm_a, dxm_db=xm_b, dxp_da=xp_a, dxp_db=xp_b)

Rs = [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1e4]
t0 = time.time()
worst = {}
for R in Rs:
    w = -1; wpt = None; wd = None
    npts = 0
    for a in np.linspace(0.02, 0.96, 20):
        for b in np.linspace(a+0.02, 0.98, 20):
            if b <= a + 1e-9: continue
            try:
                d = dXC(a, b, R)
            except Exception:
                continue
            npts += 1
            s = d["sum"]
            if s > w:
                w = s; wpt = (round(float(a),3), round(float(b),3)); wd = d
    worst[R] = dict(max_sum=float(w), at=wpt, npts=npts,
                    dxm_da=float(wd["dxm_da"]), dxm_db=float(wd["dxm_db"]),
                    dxp_da=float(wd["dxp_da"]), dxp_db=float(wd["dxp_db"]))
    print(f"R={R}: max(dXC/da+dXC/db) = {w:.6f} at {wpt} (npts={npts})")
print("elapsed", round(time.time()-t0,1), "s")
print(json.dumps(worst, indent=1))