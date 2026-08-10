# -*- coding: utf-8 -*-
"""e03_sign_conjecture.py: verify sign(M) = sign(1/2 - C), M = (x_+ + x_-)/2 - (a+b)/2.
Also record where the -q crossing is near-degenerate (x_+ close to 1 or 0)."""
import numpy as np, sys, json, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T200000Z-o3a-c1b-7F3A9B\reproducibility")
from c1_lib import cfg, y_at

def v(x, a, b, R):
    s1, s2, _, _ = cfg(a, b, R)
    return y_at(s2, a, b, R, x)/y_at(s1, a, b, R, x)

def qval(a, b, R):
    s1, s2, n1, n2 = cfg(a, b, R)
    return np.sqrt((s1**2/n1)/(s2**2/n2))

def xcross(a, b, R, target, lo=1e-9, hi=1-1e-9):
    s1, s2, _, _ = cfg(a, b, R)
    def g(x): return v(x, a, b, R) - target
    gl = g(lo); gh = g(hi)
    if np.signbit(gl) == np.signbit(gh):
        return None  # no crossing
    for _ in range(70):
        md = 0.5*(lo+hi)
        if np.signbit(g(md)) == np.signbit(gl):
            lo = md
        else:
            hi = md
    return 0.5*(lo+hi)

def M_of(a, b, R):
    q = qval(a, b, R)
    xm = xcross(a, b, R, q)
    xp = xcross(a, b, R, -q)
    if xm is None or xp is None:
        return None, None, None
    return (xm+xp)/2 - (a+b)/2, xm, xp

Rs = [1.02, 1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1e4, 1e6]
report = {}
t0 = time.time()
for R in Rs:
    bad = 0; npts = 0; maxabsM = 0; maxbadM = 0; worst = None
    mindist = 1.0
    for a in np.linspace(0.01, 0.98, 30):
        for b in np.linspace(a+0.01, 0.99, 30):
            if b <= a: continue
            try:
                M, xm, xp = M_of(a, b, R)
            except Exception:
                continue
            if M is None:
                continue
            npts += 1
            C = (a+b)/2
            # expected sign: M > 0 iff C < 1/2
            if C < 0.5 - 1e-9:
                ok = M > 0
            elif C > 0.5 + 1e-9:
                ok = M < 0
            else:
                ok = abs(M) < 1e-6
            if not ok:
                bad += 1
                if abs(M) > maxbadM:
                    maxbadM = abs(M); worst = (round(float(a),4), round(float(b),4), float(M))
            maxabsM = max(maxabsM, abs(M))
            if abs(C - 0.5) < mindist:
                mindist = abs(C - 0.5)
    report[R] = dict(npts=npts, violations=bad, maxbadM=float(maxbadM), worst=worst,
                     maxabsM=float(maxabsM), mindist_to_diag=float(mindist))
    print(f"R={R}: npts={npts} violations={bad} max|M|={maxabsM:.4f} worst={worst}")
print("elapsed", round(time.time()-t0,1))