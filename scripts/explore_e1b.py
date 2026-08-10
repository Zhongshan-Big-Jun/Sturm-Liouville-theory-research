# -*- coding: utf-8 -*-
"""E1 exploration v5: coarse scan + refine for R1(a,b0) roots (evidence only)."""
import numpy as np, time
src = open(r"F:\LaTeX\BVE research\scripts\explore_e1.py", encoding="utf-8").read()
exec(src.split('a0 = np.arccos')[0])
a0 = np.arccos(0.25)/np.pi; b0 = 1-a0

def r1(a, R):
    return residual_both(a, b0, R)[0]

for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1e4]:
    t0 = time.time()
    na = 800
    aa = np.linspace(1e-6, 1-1e-6, na)
    vals = np.array([r1(a, R) for a in aa])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx:
        lo, hi = aa[i], aa[i+1]
        flo = r1(lo, R)
        for _ in range(60):
            md = 0.5*(lo+hi)
            if np.signbit(r1(md, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    info = []
    for a in roots:
        xm, xp = band(a, b0, R)
        if xm != xm: info.append("nan"); continue
        if abs(a-xm) < 1e-5: info.append("x-")
        elif abs(a-xp) < 1e-5: info.append("x+")
        else: info.append("other")
    print(f"R={R:g}: roots={[round(r,5) for r in roots]} sheets={info}  ({time.time()-t0:.1f}s)")