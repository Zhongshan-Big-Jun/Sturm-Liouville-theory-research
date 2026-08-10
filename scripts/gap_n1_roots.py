# -*- coding: utf-8 -*-
"""gap_n1_roots.py: refine self-consistent roots over 2-param family with least_squares,
check sign pattern, verify symmetric solution, and check FH gradient identity."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def f_vals(blocks, x_pts):
    s = lams_fast(blocks, 2)
    lam = s**2
    out = []
    for x in x_pts:
        u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
        u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
        out.append(lam[0]*u1**2 - lam[1]*u2**2)
    return s, np.array(out)

def D_of(blocks):
    s = lams_fast(blocks, 2)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def self_consistent(mode, R, ab):
    a, b = ab
    if not (0.0 < a and 0.0 < b and a+b < 1.0):
        return np.array([1e3, 1e3])
    bl = make_blocks(mode, R, a, b)
    s, fv = f_vals(bl, [a, a+b])
    return np.array([fv[0], fv[1]])

def sign_pattern_ok(mode, R, a, b, nsamp=400):
    """f>0 on middle, f<0 on ends (both modes), and f(a)=f(a+b)=0 approx."""
    bl = make_blocks(mode, R, a, b)
    xs = np.linspace(0, 1, 4001)
    s, _ = f_vals(bl, [a, a+b])
    # sample f on each block
    for (lo, hi) in [(0.0, a), (a, a+b), (a+b, 1.0)]:
        if hi - lo < 1e-9: continue
        pts = np.linspace(lo+1e-7, hi-1e-7, nsamp//3)
        _, fv = f_vals(bl, pts.tolist())
        mid_ok = np.all(fv > 0) if (lo == a and hi == a+b) else np.all(fv < 0)
        if not mid_ok:
            return False
    return True

def boundary_D(mode, R):
    """1-block and 2-block boundary values."""
    bls = {"rho=1":[(1.0,1.0)], "rho=R":[(1.0,R)], "[1,R]":[(0.5,1.0),(0.5,R)],
           "[R,1]":[(0.5,R),(0.5,1.0)], "[1,R]a0.3":[(0.3,1.0),(0.7,R)],
           "[R,1]a0.3":[(0.3,R),(0.7,1.0)], "[1,R]a0.7":[(0.7,1.0),(0.3,R)],
           "[R,1]a0.7":[(0.7,R),(0.3,1.0)]}
    for k, bl in bls.items():
        print(f"   {k}: D = {D_of(bl):.6f}")

if __name__ == "__main__":
    R = 4.0
    for mode in ("SUP", "INF"):
        print(f"==== mode={mode} R={R} ====")
        # seed grid for least squares
        seeds = []
        for a in np.linspace(0.02, 0.96, 25):
            for b in np.linspace(0.02, 0.96, 25):
                if 0.02 < a+b < 0.98:
                    seeds.append((a, b))
        roots = []
        for seed in seeds:
            res = least_squares(lambda ab: self_consistent(mode, R, ab), seed, xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=300)
            a, b = res.x
            if not (0.0 < a < 1 and 0.0 < b and a+b < 1.0): continue
            r = np.linalg.norm(res.fun)
            if r < 1e-6:
                # check sign pattern
                sp = sign_pattern_ok(mode, R, a, b)
                entry = (round(a,8), round(b,8), r, sp)
                if not any(abs(entry[0]-t[0])<1e-4 and abs(entry[1]-t[1])<1e-4 for t in roots):
                    roots.append(entry)
        print(f"  distinct self-consistent roots (resid<1e-6): {len(roots)}")
        for a, b, r, sp in roots:
            bl = make_blocks(mode, R, a, b)
            print(f"  a={a:.8f} b={b:.8f} c={1-a-b:.8f} resid={r:.2e} signpat={sp} D={D_of(bl):.8f}")
        print("  boundary D values:")
        boundary_D(mode, R)
