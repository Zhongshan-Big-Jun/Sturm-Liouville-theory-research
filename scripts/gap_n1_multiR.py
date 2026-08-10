# -*- coding: utf-8 -*-
"""gap_n1_multiR.py: verify unique interior stationary point + boundary comparison for several R."""
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

def boundary_max(R, mode):
    """max D over 2-block configs (SUP side) / min D over 2-block (INF side)."""
    best = None
    for t in np.linspace(0.002, 0.998, 250):
        for bl in ([(t,1.0),(1-t,R)],[(t,R),(1-t,1.0)]):
            d = D_of(bl)
            if best is None or (d > best[0] if mode=="SUP" else d < best[0]):
                best = (d, t, bl)
    return best

for R in (2.0, 4.0, 10.0):
    print(f"##### R={R} #####")
    for mode in ("SUP","INF"):
        seeds = [(a,b) for a in np.linspace(0.02,0.96,20) for b in np.linspace(0.02,0.96,20) if 0.04<a+b<0.96]
        roots = []
        for seed in seeds:
            res = least_squares(lambda ab: self_consistent(mode,R,ab), seed, xtol=1e-11, ftol=1e-11, gtol=1e-11, max_nfev=150)
            a,b = res.x
            if not (1e-6<a<1 and 1e-6<b and a+b<1-1e-6): continue
            r = np.linalg.norm(res.fun)
            if r < 1e-5:
                entry = (round(a,6), round(b,6), r)
                if not any(abs(entry[0]-t[0])<5e-5 and abs(entry[1]-t[1])<5e-5 for t in roots):
                    roots.append(entry)
        bl = make_blocks(mode, R, roots[0][0], roots[0][1]) if len(roots)>=1 else None
        Dstar = D_of(bl) if bl else float('nan')
        bd = boundary_max(R, mode)
        print(f"  {mode}: #interior stationary = {len(roots)}; symmetric at a={roots[0][0]:.6f} b={roots[0][1]:.6f} D*={Dstar:.6f}")
        print(f"        2-block {'max' if mode=='SUP' else 'min'} D={bd[0]:.6f} at t={bd[1]:.4f}  (rho=1: {3*np.pi**2:.4f}, rho=R: {3*np.pi**2/R:.4f})")
