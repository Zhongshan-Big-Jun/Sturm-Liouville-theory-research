# -*- coding: utf-8 -*-
"""amax1_scan.py: branch-1 (Gamma_1) fine scan near and beyond b0 at large R.
Determines a_max1(R), the right end of I_1, and whether it exceeds b0."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, y_at, norm_n, roots2
from scipy.optimize import brentq

def r1(a, b, R, s1=None, s2=None):
    if s1 is None or s2 is None:
        s1, s2 = roots2(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1**2*(np.sin(s1*a)/s1)**2/n1 - s2**2*(np.sin(s2*a)/s2)**2/n2

def v_ratio(a, b, R, s1=None, s2=None):
    if s1 is None or s2 is None:
        s1, s2 = roots2(a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    return y2a/y1a, y2b/y1b

def g1_at(a, R, lo_b, hi_b):
    """root of R1(a,.)=0 in (lo_b, hi_b); returns None if no root / not good."""
    f = lambda bb: r1(a, bb, R)
    if f(lo_b)*f(hi_b) > 0:
        return None
    b = brentq(f, lo_b, hi_b, xtol=1e-14, rtol=1e-14)
    s1, s2 = roots2(a, b, R)
    va, vb = v_ratio(a, b, R, s1, s2)
    if not (va > 0 and vb < 0):
        return None
    return b

a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi
print(f"a0={a0:.9f} b0={b0:.9f}")
for R in [1000.0, 1e4, 1e5, 1e6]:
    start = 0.55
    a = start
    last_good = None
    prev = None
    step = 5e-4
    # first find good root at start
    b = g1_at(a, R, a + 1e-6, 1 - 1e-6)
    if b is None:
        print(f"R={R}: no good branch-1 root at a={a}; trying closer to a0")
        continue
    last_good = (a, b)
    fine = False
    a_max = None
    while a < 0.585:
        a = last_good[0] + step
        b = g1_at(a, R, last_good[1] - 2e-3, min(1 - 1e-9, last_good[1] + 2e-3))
        if b is None:
            # refine step near the boundary
            step = step/4
            if step < 2e-6:
                a_max = last_good[0]
                break
            continue
        last_good = (a, b)
        step = min(5e-4, 8*step)
    a_max = last_good[0]
    print(f"R={R}: a_max1={a_max:.9f}  (>b0? {a_max > b0})  g1(a_max)={last_good[1]:.9f}  delta_b0={a_max-b0:+.3e}")
    # report values at b0 and just below/above
    for aa in [b0 - 1e-4, b0, b0 + 1e-4]:
        bb = g1_at(aa, R, aa + 1e-6, 1 - 1e-6)
        if bb is not None:
            print(f"   a={aa:.9f}: g1={bb:.9f} h1= g1-a={bb-aa:+.3e}")
        else:
            print(f"   a={aa:.9f}: no good root")
