# -*- coding: utf-8 -*-
"""amax1_scan2.py: robust branch-1 domain edge scan (fine sec grid, narrow b-window).
Determines whether Gamma_1 extends beyond b0 and locates a_max1(R)."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from scipy.optimize import brentq

def cfg(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 12000), np.linspace(1.2, 3*np.pi, 12000)])
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx[:4]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(70):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    roots = sorted(set(np.round(r, 13) for r in roots))
    if len(roots) < 2: return None
    s1, s2 = roots[0], roots[1]
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    return dict(R1=s1*s1*y1a*y1a/n1 - s2*s2*y2a*y2a/n2,
                R2=s1*s1*y1b*y1b/n1 - s2*s2*y2b*y2b/n2, va=y2a/y1a, vb=y2b/y1b)

def g1_at(a, R, bw=0.02, nb=400):
    bb = np.linspace(a+1e-5, a+bw, nb)
    vals = []
    for b in bb:
        c = cfg(a, b, R)
        vals.append(c['R1'] if c else np.nan)
    for i in range(len(bb)-1):
        v0, v1 = vals[i], vals[i+1]
        if np.isfinite(v0) and np.isfinite(v1) and v0*v1 < 0:
            try:
                b0r = brentq(lambda b: cfg(a, b, R)['R1'], bb[i], bb[i+1], xtol=1e-13)
            except Exception:
                continue
            c = cfg(a, b0r, R)
            if c is not None and c['va'] > 0 and c['vb'] < 0:
                return b0r
    return None

a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi
print(f"a0={a0:.9f} b0={b0:.9f}")
for R in [1e3, 1e4, 1e5]:
    # trace forward from b0 - 0.01 with adaptive fine steps
    a = b0 - 0.01
    b_prev = g1_at(a, R)
    if b_prev is None:
        print(f"R={R:.0e}: no root at b0-0.01; abort"); continue
    last = (a, b_prev)
    a_cur = a; step = 5e-4
    while a_cur < 0.60:
        a_next = a_cur + step
        b_next = g1_at(a_next, R, bw=0.02, nb=800)
        if b_next is None:
            step /= 4
            if step < 1e-6:
                break
            continue
        last = (a_next, b_next)
        a_cur = a_next
        step = min(5e-4, step*4)
    print(f"R={R:.0e}: a_max1 ~ {a_cur:.9f}  (>b0? {a_cur > b0})  g1(a_max1)={last[1]:.9f}")
    # also report near b0
    for aa in [b0 - 1e-5, b0, b0 + 1e-5, b0 + 1e-4]:
        bb = g1_at(aa, R, bw=0.02, nb=800)
        print(f"   a={aa:.9f}: g1={bb if bb is None else round(bb,9)} h(b0)-side={None if bb is None else round(bb-aa,8)}")
