# -*- coding: utf-8 -*-
"""Global search over 3-block family: find ALL interior critical points and global max/min of D."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=1500):
    return lams_fast(blocks, 2, npts=npts)

def f_at(blocks, x, s=None, npts=1500):
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
    if not (1e-9 < a and 1e-9 < b and a+b < 1-1e-9):
        return np.array([1e3, 1e3])
    bl = make_blocks(mode, R, a, b)
    fv, s = f_at(bl, [a, a+b])
    return fv

def D_of(blocks):
    s = s_of(blocks)
    return s[1]**2 - s[0]**2

def find_all_roots(mode, R, n=40):
    aa = np.linspace(0.02, 0.97, n); bb = np.linspace(0.02, 0.97, n)
    found = []
    for a in aa:
        for b in bb:
            if not (0.03 < a+b < 0.97): continue
            bl0 = make_blocks(mode, R, a, b)
            s0 = s_of(bl0, npts=700)
            fv0, _ = f_at(bl0, [a, a+b], s=s0, npts=700)
            if np.max(np.abs(fv0)) > 8.0: continue
            res = least_squares(lambda ab: resid(mode, R, ab), [a,b],
                                xtol=1e-11, ftol=1e-11, gtol=1e-11, max_nfev=150)
            a2, b2 = res.x
            if not (1e-6 < a2 < 1 and 1e-6 < b2 and a2+b2 < 1-1e-6): continue
            r = np.linalg.norm(res.fun)
            if r < 1e-6:
                # check sign structure (band match): f>0 on (a,a+b) for SUP, f<0 for INF?
                bl2 = make_blocks(mode, R, a2, b2)
                fv2, s2 = f_at(bl2, [a2, a2+b2])
                # sample f inside middle block
                xm = np.linspace(a2+1e-3, a2+b2-1e-3, 7)
                fvm, _ = f_at(bl2, xm, s=s2)
                ok = np.all(fvm > 0) if mode=="SUP" else np.all(fvm < 0)
                entry = (round(a2,8), round(b2,8), r, ok)
                if not any(abs(entry[0]-t[0])<1e-5 and abs(entry[1]-t[1])<1e-5 for t in found):
                    found.append(entry)
    return found

for R in (1.5, 2.0, 4.0, 10.0, 100.0):
    for mode in ("SUP","INF"):
        roots = find_all_roots(mode, R, n=30)
        print(f"mode={mode} R={R}: {len(roots)} interior critical points")
        for a,b,r,ok in roots:
            bl = make_blocks(mode, R, a, b)
            print(f"   a={a:.8f} b={b:.8f} c={1-a-b:.8f} sym_def={a-(1-a-b):+.2e} resid={r:.1e} band_ok={ok} D={D_of(bl):.10f}")
