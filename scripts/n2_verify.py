# -*- coding: utf-8 -*-
"""n2_verify.py: reproduce n=1 gap extremal structure (session 14). Fast version."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=1500):
    return lams_fast(blocks, 2, npts=npts)

def D_of(blocks, npts=1500):
    s = s_of(blocks, npts)
    return s[1]**2 - s[0]**2

def f_at(blocks, x, s=None, npts=1500):
    if s is None:
        s = s_of(blocks, npts)
    lam = s**2
    x = np.atleast_1d(np.asarray(x, dtype=float))
    x = np.clip(x, 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], x)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], x)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def resid(mode, R, ab):
    a, b = ab
    if not (1e-9 < a and 1e-9 < b and a+b < 1-1e-9):
        return np.array([1e3, 1e3])
    bl = make_blocks(mode, R, a, b)
    return f_at(bl, [a, a+b])

def find_roots(mode, R, n=22):
    aa = np.linspace(0.03, 0.95, n); bb = np.linspace(0.03, 0.95, n)
    seeds = []
    for a in aa:
        for b in bb:
            if 0.05 < a+b < 0.95:
                seeds.append((a, b))
    roots = []
    for seed in seeds:
        # pre-screen: cheap resid on coarse s
        bl0 = make_blocks(mode, R, *seed)
        s0 = s_of(bl0, npts=800)
        r0 = f_at(bl0, [seed[0], seed[0]+seed[1]], s=s0, npts=800)
        if np.max(np.abs(r0)) > 5.0:
            continue
        res = least_squares(lambda ab: resid(mode, R, ab), seed,
                            xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=200)
        a, b = res.x
        if not (1e-6 < a < 1 and 1e-6 < b and a+b < 1-1e-6):
            continue
        r = np.linalg.norm(res.fun)
        if r < 1e-7:
            entry = (round(a,7), round(b,7))
            if not any(abs(entry[0]-t[0])<1e-5 and abs(entry[1]-t[1])<1e-5 for t in roots):
                roots.append(entry + (r,))
    return roots

if __name__ == "__main__":
    for R in (2.0, 4.0, 10.0):
        for mode in ("SUP", "INF"):
            roots = find_roots(mode, R)
            print(f"mode={mode} R={R}: {len(roots)} self-consistent roots")
            for a, b, r in roots:
                bl = make_blocks(mode, R, a, b)
                print(f"   a={a:.8f} b={b:.8f} c={1-a-b:.8f} sym_def={a-(1-a-b):+.3e} resid={r:.1e} D={D_of(bl):.10f}")
            D1 = 3*np.pi**2; DR = 3*np.pi**2/R
            print(f"   constants: D(rho=1)={D1:.8f}  D(rho=R)={DR:.8f}")
