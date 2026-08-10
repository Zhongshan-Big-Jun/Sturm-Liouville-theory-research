# -*- coding: utf-8 -*-
"""E1 exploration v6: g1(b0) = b-value on Gamma_1 at a=b0, via roots of R1(b0,b)=0 (evidence only)."""
import numpy as np, time
src = open(r"F:\LaTeX\BVE research\scripts\explore_e1.py", encoding="utf-8").read()
exec(src.split('a0 = np.arccos')[0])
a0 = np.arccos(0.25)/np.pi; b0 = 1-a0

def r1at(b, R):
    return residual_both(b0, b, R)[0]

for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1e4]:
    t0 = time.time()
    na = 500
    bb = np.linspace(b0+1e-5, 1-1e-5, na)
    vals = np.array([r1at(b, R) for b in bb])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx:
        lo, hi = bb[i], bb[i+1]
        flo = r1at(lo, R)
        for _ in range(60):
            md = 0.5*(lo+hi)
            if np.signbit(r1at(md, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    # identify x- sheet: for (b0, b), need b0 = x_-
    info = []
    for b in roots:
        xm, xp = band(b0, b, R)
        if xm != xm: info.append((b, "nan")); continue
        if abs(b0-xm) < 3e-4: info.append((b, "x-"))
        elif abs(b0-xp) < 3e-4: info.append((b, "x+"))
        else: info.append((b, "other"))
    print(f"R={R:g}: roots of R1(b0,b)=0: " + "; ".join(f"b={b:.5f} ({s})" for b,s in info) + f"  ({time.time()-t0:.1f}s)")
    for b,s in info:
        if s == "x-":
            print(f"    -> g1(b0)={b:.6f}, h(b0)=g1(b0)-b0={b-b0:+.6f}")