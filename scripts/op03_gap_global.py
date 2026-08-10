# -*- coding: utf-8 -*-
"""#3: global optimality check for n=1,2 (free bang-bang configs) + large-R limits."""
import numpy as np
from scipy.optimize import minimize
from op03_gap_fixed import lams_precise

def lams_fast(xs, vals, k, npts=20000, smax=120.0):
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
            sg = np.linspace(lo, hi, 800)
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

def neg_gap(w, R, n, start_val, do_max, nb):
    w = np.abs(w); w = w/np.sum(w)
    vals = np.array([start_val if i % 2 == 0 else (R if start_val == 1 else 1.0) for i in range(nb)], dtype=float)
    xs = np.concatenate(([0.0], np.cumsum(w)))
    lam = lams_fast(xs, vals, n+2)
    g = lam[n] - lam[n-1]
    return -g if do_max else g

R = 4.0
rng = np.random.default_rng(17)
for n in (1, 2):
    nb = 2*n+1
    print(f"=== n={n} R=4 global check over {nb}-block alternating families ===")
    for start_val, do_max, label in [(1,True,"SUP [1,R,...]"), (R,False,"INF [R,1,...]")]:
        best = (1e9, None)
        for t in range(8):
            w0 = rng.dirichlet(np.ones(nb))
            r = minimize(neg_gap, w0, args=(R, n, start_val, do_max, nb), method='Nelder-Mead',
                         options={'maxiter':500, 'xatol':1e-9, 'fatol':1e-11})
            if r.fun < best[0]: best = (r.fun, np.abs(r.x)/np.sum(np.abs(r.x)))
        val = -best[0] if do_max else best[0]
        print(f"  {label}: {val:.6f} widths={np.array2string(best[1], precision=4)}")
print("reference: n=1 SUP 32.613984 INF 6.784482; n=2 SUP 63.093199 INF 9.023038")
