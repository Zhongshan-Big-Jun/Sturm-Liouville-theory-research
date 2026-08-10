# -*- coding: utf-8 -*-
"""hb0_cfg.py: h(b0) at 1e6, 1e7 via clean_lib cfg solver, fine scan near b0."""
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

b0v = np.arccos(-0.25)/np.pi
for R in [1e6, 1e7]:
    a = b0v - 1e-7
    bb = np.linspace(a+1e-5, a+0.002, 200)
    vals = []
    for b in bb:
        c = cfg(a, b, R)
        vals.append(c['R1'] if c else np.nan)
    found = False
    for i in range(len(bb)-1):
        v0, v1 = vals[i], vals[i+1]
        if np.isfinite(v0) and np.isfinite(v1) and v0*v1 < 0:
            try:
                b0 = brentq(lambda b: cfg(a, b, R)['R1'], bb[i], bb[i+1], xtol=1e-13)
            except Exception:
                continue
            c = cfg(a, b0, R)
            if c is not None and c['va'] > 0:
                print(f"  R={R:.0e}: h(b0)={b0-b0v:+.6e} h*sqrtR={(b0-b0v)*np.sqrt(R):.4f} va={c['va']:.2e}")
                found = True
                break
    if not found:
        print(f"  R={R:.0e}: good root not found in fine scan")
