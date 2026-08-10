# -*- coding: utf-8 -*-
"""gap_n1_roots2.py: refined self-consistent root search (fixed guards)."""
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
    if not (1e-9 < a and 1e-9 < b and a+b < 1-1e-9):
        return np.array([1e3, 1e3])
    bl = make_blocks(mode, R, a, b)
    s, fv = f_vals(bl, [a, a+b])
    return np.array([fv[0], fv[1]])

def sign_pattern_ok(mode, R, a, b):
    bl = make_blocks(mode, R, a, b)
    ok = True
    for (lo, hi, expect_pos) in [(0.0, a, False), (a, a+b, True), (a+b, 1.0, False)]:
        if hi - lo < 2e-7: continue
        pts = np.linspace(lo+1e-7, hi-1e-7, 60)
        _, fv = f_vals(bl, pts.tolist())
        if expect_pos:
            ok = ok and np.all(fv > -1e-6)
        else:
            ok = ok and np.all(fv < 1e-6)
    return ok

if __name__ == "__main__":
    R = 4.0
    for mode in ("SUP", "INF"):
        print(f"==== mode={mode} R={R} ====")
        seeds = [(a, b) for a in np.linspace(0.02, 0.96, 25) for b in np.linspace(0.02, 0.96, 25) if 0.04 < a+b < 0.96]
        roots = []
        for seed in seeds:
            res = least_squares(lambda ab: self_consistent(mode, R, ab), seed, xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=200)
            a, b = res.x
            if not (1e-6 < a < 1 and 1e-6 < b and a+b < 1-1e-6): continue
            r = np.linalg.norm(res.fun)
            if r < 1e-6:
                sp = sign_pattern_ok(mode, R, a, b)
                entry = (round(a,7), round(b,7), r, sp)
                if not any(abs(entry[0]-t[0])<5e-5 and abs(entry[1]-t[1])<5e-5 for t in roots):
                    roots.append(entry)
        print(f"  distinct self-consistent roots (resid<1e-6): {len(roots)}")
        for a, b, r, sp in roots:
            bl = make_blocks(mode, R, a, b)
            print(f"  a={a:.8f} b={b:.8f} c={1-a-b:.8f} resid={r:.2e} signpat={sp} D={D_of(bl):.8f}")
