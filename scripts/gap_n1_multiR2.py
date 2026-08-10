# -*- coding: utf-8 -*-
"""gap_n1_multiR2.py: fixed interior stationary point search."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def f_vals(blocks, x_pts):
    s = lams_fast(blocks, 2)
    lam = s**2
    out = []
    for x in x_pts:
        u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
        u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
        out.append(lam[0]*u1**2 - lam[1]*u2**2)
    return np.array(out)

def D_of(blocks):
    s = lams_fast(blocks, 2)
    return s[1]**2 - s[0]**2

def self_consistent(mode, R, ab):
    a, b = ab
    if not (1e-9 < a and 1e-9 < b and a+b < 1-1e-9):
        return np.array([1e3, 1e3])
    bl = make_blocks(mode, R, a, b)
    fv = f_vals(bl, [a, a+b])
    return np.array([fv[0], fv[1]])

known = {(2.0,"SUP"):31.1023, (2.0,"INF"):14.1278, (4.0,"SUP"):32.61398, (4.0,"INF"):6.78448, (10.0,"SUP"):34.4513, (10.0,"INF"):2.6089}

for R in (2.0, 4.0, 10.0):
    print(f"##### R={R} #####")
    for mode in ("SUP","INF"):
        seeds = [(a,b) for a in np.linspace(0.05,0.95,22) for b in np.linspace(0.03,0.93,22) if 0.1<a+b<0.9]
        roots = []
        for seed in seeds:
            res = least_squares(lambda ab: self_consistent(mode,R,ab), seed, xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=300)
            a,b = res.x
            if not (0.02<a<0.98 and 0.02<b and a+b<0.98): continue   # genuinely interior
            r = np.linalg.norm(res.fun)
            if r < 1e-6:
                entry = (round(a,6), round(b,6), r)
                if not any(abs(entry[0]-t[0])<2e-4 and abs(entry[1]-t[1])<2e-4 for t in roots):
                    roots.append(entry)
        print(f"  {mode}: interior stationary points = {len(roots)}")
        for a,b,r in roots:
            bl = make_blocks(mode,R,a,b)
            D = D_of(bl)
            tag = "symmetric" if abs(a-(1-a-b))<1e-4 else "ASYMMETRIC"
            print(f"     a={a:.6f} b={b:.6f} c={1-a-b:.6f} resid={r:.1e} D={D:.6f} [{tag}] (known {known.get((R,mode))})")
