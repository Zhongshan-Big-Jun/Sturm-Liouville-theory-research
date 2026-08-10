# -*- coding: utf-8 -*-
"""#3: faster global optimization of lambda_{n+1}-lambda_n over alternating configs."""
import numpy as np
from scipy.optimize import minimize

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

def neg_gap(w, R, n, maximize=True):
    w = np.abs(w); w = w/np.sum(w)
    nb = 2*n+1
    vals = np.array([R if i % 2 == 1 else 1.0 for i in range(nb)], dtype=float)
    xs = np.concatenate(([0.0], np.cumsum(w)))
    lam = lams_fast(xs, vals, n+2)
    g = lam[n] - lam[n-1]
    return -g if maximize else g

if __name__ == "__main__":
    R = 4.0
    rng = np.random.default_rng(11)
    for n in (1, 2, 3):
        nb = 2*n+1
        best_max = (1e9, None); best_min = (1e9, None)
        for trial in range(4):
            w0 = rng.dirichlet(np.ones(nb))
            r1 = minimize(neg_gap, w0, args=(R, n, True), method='Nelder-Mead',
                          options={'maxiter':400, 'xatol':1e-9, 'fatol':1e-11})
            r2 = minimize(neg_gap, w0, args=(R, n, False), method='Nelder-Mead',
                          options={'maxiter':400, 'xatol':1e-9, 'fatol':1e-11})
            if r1.fun < best_max[0]: best_max = (r1.fun, np.abs(r1.x)/np.sum(np.abs(r1.x)))
            if r2.fun < best_min[0]: best_min = (r2.fun, np.abs(r2.x)/np.sum(np.abs(r2.x)))
        print(f"n={n}: sup gap = {-best_max[0]:.8f} widths={np.array2string(best_max[1], precision=5)}")
        print(f"n={n}: inf gap = {best_min[0]:.8f} widths={np.array2string(best_min[1], precision=5)}")
        print(f"   (2n+1)*pi^2 = {(2*n+1)*np.pi**2:.6f}, (2n+1)*pi^2/R = {(2*n+1)*np.pi**2/R:.6f}")
