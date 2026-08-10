# -*- coding: utf-8 -*-
"""Clean search: valid interior critical points (a,b,c > 0.002, correct band structure) for many R."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=1200):
    return lams_fast(blocks, 2, npts=npts)

def f_at(blocks, x, s=None, npts=1200):
    if s is None:
        s = s_of(blocks, npts)
    lam = s**2
    x = np.atleast_1d(np.asarray(x, dtype=float))
    x = np.clip(x, 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], x)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], x)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def resid(mode, R, ab):
    a, b = ab
    if not (0.002 < a and 0.002 < b and a+b < 0.998):
        return np.array([1e3, 1e3])
    bl = make_blocks(mode, R, a, b)
    fv, s = f_at(bl, [a, a+b])
    return fv

def band_ok(mode, R, a, b, s):
    bl = make_blocks(mode, R, a, b)
    xm = np.linspace(a+1e-4, a+b-1e-4, 5)
    fvm, _ = f_at(bl, xm, s=s)
    xo = np.array([(a-1e-4)/2, (1+a+b)/2])  # sample outside
    fvo, _ = f_at(bl, xo, s=s)
    # SUP: f>0 inside (a,a+b), f<0 outside.  INF: f>0 inside, f<0 outside (same! middle block light)
    # Wait: for INF middle block rho=1, f>0 where rho=1 => f>0 inside.  outside f<0 where rho=R.
    return bool(np.all(fvm > 0) and np.all(fvo < 0))

print(f"{'R':>8} {'mode':>4} {'a':>10} {'b':>10} {'c':>10} {'symdef':>10} {'D':>12} {'resid':>8} {'band':>5}")
for R in (1.1, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0, 30.0, 100.0, 1000.0):
    for mode in ("SUP","INF"):
        found = []
        for a in np.linspace(0.05, 0.9, 18):
            for b in np.linspace(0.05, 0.9, 18):
                if not (0.1 < a+b < 0.9): continue
                res = least_squares(lambda ab: resid(mode, R, ab), [a,b],
                                    xtol=1e-10, ftol=1e-10, gtol=1e-10, max_nfev=120)
                a2, b2 = res.x
                if not (0.002 < a2 and 0.002 < b2 and a2+b2 < 0.998): continue
                r = np.linalg.norm(res.fun)
                if r > 1e-5: continue
                bl = make_blocks(mode, R, a2, b2)
                s = s_of(bl)
                ok = band_ok(mode, R, a2, b2, s)
                D = s[1]**2 - s[0]**2
                entry = (round(a2,7), round(b2,7))
                if not any(abs(entry[0]-t[0])<1e-5 and abs(entry[1]-t[1])<1e-5 for t in found):
                    found.append((a2,b2,r,ok,D))
        valid = [f for f in found if f[3]]
        print(f"{R:8.1f} {mode:>4} valid_count={len(valid)}  (of {len(found)} algebraic)")
        for a2,b2,r,ok,D in valid:
            print(f"         a={a2:.8f} b={b2:.8f} c={1-a2-b2:.8f} symdef={a2-(1-a2-b2):+.2e} D={D:.8f} resid={r:.1e} band={ok}")
