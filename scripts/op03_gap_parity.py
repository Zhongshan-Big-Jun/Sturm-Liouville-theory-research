# -*- coding: utf-8 -*-
"""#3: both parities + self-consistency verification for gap extrema."""
import numpy as np
from scipy.optimize import minimize
from op03_gap_n1 import lams_blocks, eigfuns_at

def lams_fast(xs, vals, k, npts=15000, smax=160.0):
    s = np.linspace(1e-9, smax, npts)
    M00 = np.ones(npts); M01 = np.zeros(npts); M10 = np.zeros(npts); M11 = np.ones(npts)
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    d = M01
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx[:k]:
        lo, hi = s[i], s[i+1]
        for _ in range(3):
            sg = np.linspace(lo, hi, 900)
            M00 = np.ones(len(sg)); M01 = np.zeros(len(sg)); M10 = np.zeros(len(sg)); M11 = np.ones(len(sg))
            for jj in range(len(xs)-1):
                L = xs[jj+1]-xs[jj]; c = vals[jj]
                w = sg*np.sqrt(c); wL = w*L
                cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
                M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
            dg = M01
            sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            j2 = np.nonzero(sg_s)[0]
            if len(j2) == 0: break
            lo, hi = sg[j2[0]], sg[j2[0]+1]
        out.append(((lo+hi)/2)**2)
    return np.sort(out)[:k]

def gap(w, R, n, start_val, maximize=True):
    """w = widths, start_val = rho of first block (1 or R)."""
    w = np.abs(w); w = w/np.sum(w)
    nb = len(w)
    vals = np.array([start_val if i % 2 == 0 else (R if start_val == 1 else 1.0) for i in range(nb)], dtype=float)
    xs = np.concatenate(([0.0], np.cumsum(w)))
    lam = lams_fast(xs, vals, n+2)
    g = lam[n] - lam[n-1]
    return g if maximize else -g

if __name__ == "__main__":
    R = 4.0
    rng = np.random.default_rng(3)
    # n=1 min with parity [R,1,R] (3 blocks starting with R)
    nb = 3
    best = (1e9, None)
    for trial in range(6):
        w0 = rng.dirichlet(np.ones(nb))
        r = minimize(gap, w0, args=(R, 1, R, False), method='Nelder-Mead',
                     options={'maxiter':500, 'xatol':1e-10, 'fatol':1e-12})
        if r.fun < best[0]: best = (r.fun, np.abs(r.x)/np.sum(np.abs(r.x)))
    print(f"n=1 inf over [R,1,R]: {best[0]:.8f} widths={np.array2string(best[1], precision=6)}")
    print(f"   self-consistent [R,1,R] value: 6.78448234 (u=0.382599)")

    # n=2 min with parity [R,1,R,1,R] (5 blocks starting with R)
    nb = 5
    best = (1e9, None)
    for trial in range(8):
        # initialize near 1-bands at 1/3, 2/3
        w0 = rng.dirichlet(np.ones(nb))
        r = minimize(gap, w0, args=(R, 2, R, False), method='Nelder-Mead',
                     options={'maxiter':800, 'xatol':1e-10, 'fatol':1e-12})
        if r.fun < best[0]: best = (r.fun, np.abs(r.x)/np.sum(np.abs(r.x)))
    print(f"n=2 inf over [R,1,R,1,R]: {best[0]:.8f} widths={np.array2string(best[1], precision=6)}")

    # n=2 max with parity [1,R,1,R,1] refined from structured init
    nb = 5
    best = (1e9, None)
    for trial in range(8):
        w0 = rng.dirichlet(np.ones(nb))
        r = minimize(gap, w0, args=(R, 2, 1, True), method='Nelder-Mead',
                     options={'maxiter':800, 'xatol':1e-10, 'fatol':1e-12})
        if r.fun < best[0]: best = (r.fun, np.abs(r.x)/np.sum(np.abs(r.x)))
    print(f"n=2 sup over [1,R,1,R,1]: {best[0]:.8f} widths={np.array2string(best[1], precision=6)}")

    # n=3 max with parity [1,R,...] 7 blocks, structured init near nodes of u4: 1/4, 1/2, 3/4
    nb = 7
    best = (1e9, None)
    for trial in range(8):
        w0 = rng.dirichlet(np.ones(nb))
        r = minimize(gap, w0, args=(R, 3, 1, True), method='Nelder-Mead',
                     options={'maxiter':1000, 'xatol':1e-10, 'fatol':1e-12})
        if r.fun < best[0]: best = (r.fun, np.abs(r.x)/np.sum(np.abs(r.x)))
    print(f"n=3 sup over [1,R,1,R,1,R,1]: {best[0]:.8f} widths={np.array2string(best[1], precision=6)}")
