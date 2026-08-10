# -*- coding: utf-8 -*-
"""#5 MW Lemma 2 MIN-case truncation structure audit.
Mirror setup: z0 = LEFTMOST zero of y_{k+1}; z1 = SECOND-from-LEFT zero of y_{2(k+1)}.
Case A' (z0<=z1): new problem (-1/2,z0): eig1 = lam_{k+1}, eig2 = lam_{2(k+1)}.
Case B' (z1<z0):  new problem (z0,1/2): eig_k = lam_{k+1}, eig_{2k} = lam_{2(k+1)}.
"""
import numpy as np

def solve_iv(xs, rhos, lam, y0, yp0, xa, xb, npts=8000):
    xs_in = [x for x in xs if xa < x < xb]
    segs = [xa] + xs_in + [xb]
    xg = np.linspace(xa, xb, npts)
    y = np.zeros(npts)
    yy, yyp = y0, yp0
    cur = xa
    for i in range(len(segs)-1):
        x1 = segs[i+1]
        r = rhos[i]
        w = np.sqrt(lam*r)
        seg = np.linspace(cur, x1, max(20, int(200*(x1-cur))))
        ys = yy*np.cos(w*(seg-cur)) + yyp/w*np.sin(w*(seg-cur))
        m = (xg >= seg[0]-1e-12) & (xg <= seg[-1]+1e-12)
        y[m] = np.interp(xg[m], seg, ys)
        d = seg[-1]-cur
        yyp = -w*yy*np.sin(w*d) + yyp*np.cos(w*d)
        yy = ys[-1]
        cur = x1
    return xg, y

def nz(y):
    s = np.sign(y)
    return len(np.where((s[:-1]*s[1:]) < 0)[0])

def eigval_N(xs, rhos, N, xa=-0.5, xb=0.5):
    rmin = min(rhos)
    lo, hi = 1e-8, (N+3)**2*np.pi**2/rmin + 10
    while True:
        _, y = solve_iv(xs, rhos, hi, 0.0, 1.0, xa, xb)
        if nz(y) >= N: break
        hi *= 4
    for _ in range(120):
        mid = 0.5*(lo+hi)
        _, y = solve_iv(xs, rhos, mid, 0.0, 1.0, xa, xb)
        if nz(y) < N: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

def zeros_refined(xs, rhos, lam, xa=-0.5, xb=0.5, eps=1e-9):
    xg, y = solve_iv(xs, rhos, lam, 0.0, 1.0, xa, xb, npts=12000)
    idx = np.where((np.sign(y[:-1])*np.sign(y[1:])) < 0)[0]
    out = []
    for i in idx:
        lo, hi = xg[i], xg[i+1]
        for _ in range(60):
            mid = 0.5*(lo+hi)
            if yval(xs, rhos, lam, 0.0, 1.0, xa, xb, lo)*yval(xs, rhos, lam, 0.0, 1.0, xa, xb, mid) <= 0:
                hi = mid
            else:
                lo = mid
        out.append(0.5*(lo+hi))
    return np.array([z for z in out if xa+eps < z < xb-eps])

def yval(xs, rhos, lam, y0, yp0, xa, xb, x):
    xs_in = [p for p in xs if xa < p < xb and p < x]
    segs = [xa] + xs_in + [x]
    yy, yyp = y0, yp0
    cur = xa
    for i in range(len(segs)-1):
        x1 = segs[i+1]
        w = np.sqrt(lam*rhos[i]); d = x1-cur
        y1 = yy*np.cos(w*d) + yyp/w*np.sin(w*d)
        yp1 = -w*yy*np.sin(w*d) + yyp*np.cos(w*d)
        yy, yyp = y1, yp1; cur = x1
    return yy

def slice_rho(xs, rhos, xa, xb):
    xs_in = [x for x in xs if xa < x < xb]
    pts = [xa] + xs_in + [xb]
    out_r = []
    for i in range(len(pts)-1):
        midx = 0.5*(pts[i]+pts[i+1])
        j = 0
        while j < len(xs) and midx > xs[j]: j += 1
        out_r.append(rhos[j])
    return xs_in, out_r

rng = np.random.default_rng(555)
allok = True; nA = nB = 0
for trial in range(40):
    ncell = int(rng.integers(2, 5))
    xs = np.sort(rng.uniform(-0.45, 0.45, ncell))
    rhos = rng.uniform(1.0, 4.0, ncell+1)
    k = int(rng.integers(1, 4))
    m = k+1
    lam_m = eigval_N(xs, rhos, m); lam_2m = eigval_N(xs, rhos, 2*m)
    z0s = zeros_refined(xs, rhos, lam_m)
    z1s = zeros_refined(xs, rhos, lam_2m)
    if len(z0s) != m-1 or len(z1s) != 2*m-1: continue
    z0 = z0s[0]; z1 = z1s[1]   # LEFTMOST zero of y_m; SECOND-from-LEFT zero of y_2m
    if not (-0.95 < z0 < -0.05): continue
    if z0 <= z1:
        nA += 1
        xs_a, rhos_a = slice_rho(xs, rhos, -0.5, z0)
        e1 = eigval_N(xs_a, rhos_a, 1, -0.5, z0)
        e2 = eigval_N(xs_a, rhos_a, 2, -0.5, z0)
        ok = abs(e1-lam_m)/lam_m < 1e-5 and abs(e2-lam_2m)/lam_2m < 1e-5
        if not ok: allok=False
        print(f"trial{trial} k={k} caseA': z0={z0:.4f} z1={z1:.4f} e1={e1:.5f}({lam_m:.5f}) e2={e2:.5f}({lam_2m:.5f}) ok={ok}")
    else:
        nB += 1
        xs_b, rhos_b = slice_rho(xs, rhos, z0, 0.5)
        ek = eigval_N(xs_b, rhos_b, k, z0, 0.5)
        e2k = eigval_N(xs_b, rhos_b, 2*k, z0, 0.5)
        ok = abs(ek-lam_m)/lam_m < 1e-5 and abs(e2k-lam_2m)/lam_2m < 1e-5
        if not ok: allok=False
        print(f"trial{trial} k={k} caseB': z0={z0:.4f} z1={z1:.4f} e_k={ek:.5f}({lam_m:.5f}) e_2k={e2k:.5f}({lam_2m:.5f}) ok={ok}")
print(f"MIN-case done: nA={nA} nB={nB} allok={allok}")
