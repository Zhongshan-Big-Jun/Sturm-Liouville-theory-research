# -*- coding: utf-8 -*-
"""#3: both parities, fixed semantics."""
import numpy as np
from scipy.optimize import minimize
from op03_gap_n1 import lams_blocks

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

def neg_gap(w, R, n, start_val, do_max):
    """returns -gap if do_max (so minimize maximizes), +gap if not."""
    w = np.abs(w); w = w/np.sum(w)
    nb = len(w)
    vals = np.array([start_val if i % 2 == 0 else (R if start_val == 1 else 1.0) for i in range(nb)], dtype=float)
    xs = np.concatenate(([0.0], np.cumsum(w)))
    lam = lams_fast(xs, vals, n+2)
    g = lam[n] - lam[n-1]
    return -g if do_max else g

def run(R, n, start_val, do_max, trials=6, maxiter=800):
    nb = 2*n+1
    best = (1e9, None)
    rng = np.random.default_rng(7)
    for trial in range(trials):
        w0 = rng.dirichlet(np.ones(nb))
        r = minimize(neg_gap, w0, args=(R, n, start_val, do_max), method='Nelder-Mead',
                     options={'maxiter':maxiter, 'xatol':1e-10, 'fatol':1e-12})
        if r.fun < best[0]: best = (r.fun, np.abs(r.x)/np.sum(np.abs(r.x)))
    return (-best[0] if do_max else best[0]), best[1]

if __name__ == "__main__":
    R = 4.0
    for n in (1, 2, 3):
        nb = 2*n+1
        supmax, wmax = run(R, n, 1, True)
        infmin, wmin = run(R, n, R, False)
        supmin, wmin2 = run(R, n, 1, False)   # sup within wrong parity (lower bound info)
        infmax, wmax2 = run(R, n, R, True)    # inf within wrong parity
        print(f"n={n}:")
        print(f"  [1,R,...] parity: sup={supmax:.8f} widths={np.array2string(wmax, precision=5)}")
        print(f"  [R,1,...] parity: inf={infmin:.8f} widths={np.array2string(wmin, precision=5)}")
        print(f"  cross: [1,R,..] inf={supmin:.8f} | [R,1,..] sup={infmax:.8f}")
