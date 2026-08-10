# -*- coding: utf-8 -*-
"""#3: broad global search for gap extrema (5 and 7 blocks, both parities), R=4."""
import numpy as np
from scipy.optimize import minimize
from op03_gap_fixed import lams_precise

def lams_fast(xs, vals, k, npts=15000, smax=150.0):
    s = np.linspace(1e-9, smax, npts)
    M00 = np.ones(npts); M01 = np.zeros(npts); M10 = np.zeros(npts); M11 = np.ones(npts)
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
    d = M01
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx[:k]:
        lo, hi = s[i], s[i+1]
        for _ in range(3):
            sg = np.linspace(lo, hi, 700)
            M00 = np.ones(len(sg)); M01 = np.zeros(len(sg)); M10 = np.zeros(len(sg)); M11 = np.ones(len(sg))
            for jj in range(len(xs)-1):
                L = xs[jj+1]-xs[jj]; c = vals[jj]
                w = sg*np.sqrt(c); wL = w*L
                cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
                M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
            dg = M01
            sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            j2 = np.nonzero(sg_s)[0]
            if len(j2) == 0: break
            lo, hi = sg[j2[0]], sg[j2[0]+1]
        out.append(((lo+hi)/2)**2)
    return np.sort(out)[:k]

def gap_of(w, R, n, start_val, nb):
    w = np.abs(w); w = w/np.sum(w)
    vals = np.array([start_val if i % 2 == 0 else (R if start_val == 1 else 1.0) for i in range(nb)], dtype=float)
    xs = np.concatenate(([0.0], np.cumsum(w)))
    lam = lams_fast(xs, vals, n+2)
    return lam[n] - lam[n-1]

R = 4.0
rng = np.random.default_rng(29)
print("=== INF search with 7-block configs (more freedom), n=1,2,3 ===")
ref = {1: 6.78448234, 2: 9.02303787, 3: 9.02933654}
for n in (1, 2, 3):
    nb = 2*n+3   # one more pair than minimal
    best = (1e9, None)
    for t in range(10):
        w0 = rng.dirichlet(np.ones(nb))
        r = minimize(gap_of, w0, args=(R, n, R, nb), method='Nelder-Mead',
                     options={'maxiter':600, 'xatol':1e-8, 'fatol':1e-10})
        if r.fun < best[0]: best = (r.fun, np.abs(r.x)/np.sum(np.abs(r.x)))
    print(f"n={n}: 7-block INF best = {best[0]:.6f} (ref self-consistent {ref[n]:.6f}) widths={np.array2string(best[1], precision=4)}")
print("=== SUP search with 7-block configs, n=2,3 ===")
refS = {2: 63.09319883, 3: 102.62554631}
for n in (2, 3):
    nb = 2*n+3
    best = (-1e9, None)
    for t in range(10):
        w0 = rng.dirichlet(np.ones(nb))
        r = minimize(lambda w: -gap_of(w, R, n, 1, nb), w0, method='Nelder-Mead',
                     options={'maxiter':600, 'xatol':1e-8, 'fatol':1e-10})
        if -r.fun > best[0]: best = (-r.fun, np.abs(r.x)/np.sum(np.abs(r.x)))
    print(f"n={n}: 7-block SUP best = {best[0]:.6f} (ref {refS[n]:.6f}) widths={np.array2string(best[1], precision=4)}")
