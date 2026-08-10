# -*- coding: utf-8 -*-
"""agentB_grid.py: residual grid R1=f(a), R2=f(b) and T-map grid for several R."""
import sys, time, json
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3')
import numpy as np
from agentB_lib import *

def residuals(a, b, R):
    cfg = config(a, b, R)
    return float(f_at(a,b,R,a,cfg)), float(f_at(a,b,R,b,cfg))

def grid_scan(R, N=18):
    xs = np.linspace(0.01, 0.99, N)
    out = []
    for a in xs:
        for b in xs:
            if b <= a + 1e-9: continue
            cfg = config(a, b, R)
            r1 = float(f_at(a,b,R,a,cfg)); r2 = float(f_at(a,b,R,b,cfg))
            z = zeros_f_cfg(a, b, R, cfg)
            out.append((a, b, r1, r2, z))
    return out

def zeros_f_cfg(a, b, R, cfg):
    s, n, z0 = cfg
    fa0 = float(f_at(a, b, R, 1e-12, cfg)); fz0 = float(f_at(a, b, R, z0, cfg))
    if not (fa0 < 0 and fz0 > 0): return None
    lo, hi = 0.0, z0
    for _ in range(70):
        m = 0.5*(lo+hi)
        if float(f_at(a,b,R,m,cfg)) < 0: lo = m
        else: hi = m
    xm = 0.5*(lo+hi)
    if not (float(f_at(a,b,R,1.0-1e-12,cfg)) < 0): return None
    lo, hi = z0, 1.0
    for _ in range(70):
        m = 0.5*(lo+hi)
        if float(f_at(a,b,R,m,cfg)) > 0: lo = m
        else: hi = m
    xp = 0.5*(lo+hi)
    return (xm, xp)

if __name__ == '__main__':
    R = float(sys.argv[1]) if len(sys.argv)>1 else 4.0
    N = int(sys.argv[2]) if len(sys.argv)>2 else 18
    t0=time.time()
    data = grid_scan(R, N)
    # find grid cells where R1 and R2 change sign -> crude location of common zeros
    # organize by a-rows and b-columns
    print(f"R={R} grid {N}x{N}: {len(data)} pts, t={time.time()-t0:.0f}s")
    # locate zeros of R1 along rows (fixed a, vary b)
    rows = {}
    for (a,b,r1,r2,z) in data:
        rows.setdefault(round(a,6), []).append((b, r1, r2, z))
    # print rows where r1 crosses zero
    print("rows with R1 sign changes (a: b-crossings approx):")
    for a in sorted(rows):
        pts = sorted(rows[a])
        for i in range(len(pts)-1):
            if pts[i][1]*pts[i+1][1] < 0:
                bc = 0.5*(pts[i][0]+pts[i+1][0])
                print(f"  a={a:.3f}: R1 zero at b~{bc:.3f} (r1={pts[i][1]:.2f}->{pts[i+1][1]:.2f})")
    # columns with R2 sign changes
    print("cols with R2 sign changes (b: a-crossings approx):")
    cols = {}
    for (a,b,r1,r2,z) in data:
        cols.setdefault(round(b,6), []).append((a, r1, r2, z))
    for b in sorted(cols):
        pts = sorted(cols[b])
        for i in range(len(pts)-1):
            if pts[i][2]*pts[i+1][2] < 0:
                ac = 0.5*(pts[i][0]+pts[i+1][0])
                print(f"  b={b:.3f}: R2 zero at a~{ac:.3f} (r2={pts[i][2]:.2f}->{pts[i+1][2]:.2f})")
