# -*- coding: utf-8 -*-
"""#5 MW Lemma 2 MIN-case audit v2 (shooting-down truncation).
For every phi: lambda_{2(k+1)}/lambda_{k+1} >= mu(a).
Case A (c0>=2 zeros of y_2m in (z0,1/2)): truncate (z0,1/2), shoot DOWN from right to the
  crossing where count 2->1: lam_t = 2nd eigenvalue of (z0,1/2)-problem, lam_t <= lam_2m.
Case B (z_2k<z0): truncate (-1/2,z0), shoot DOWN from left to first crossing:
  lam_t = (2k)-th eigenvalue of (-1/2,z0)-problem, lam_t <= lam_2m, ratio is (2k):k.
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

def shoot_down_left(xs, rhos, lam0, z0, ncross_target=1):
    """largest lam <= lam0 s.t. left-IVP (slope 1) has y(z0)=0, with the crossing index
    given by ncross_target (1 = first crossing from the right side of z0)."""
    def f(lam):
        return yval(xs, rhos, lam, 0.0, 1.0, -0.5, 0.5, z0)
    # count zeros of y_2m strictly inside (-1/2, z0) at lam0
    zt = zeros_refined(xs, rhos, lam0, -0.5, z0)
    j = len(zt)
    # zeros move right as lam decreases; crossing number j-ncross_target+1 ... we want the
    # (j - ncross_target + 1)-th crossing (the one after removing ncross_target zeros).
    # simpler: scan lam downward from lam0, count sign changes of f.
    lam = lam0; prev = f(lam0); crossings = 0
    step = max(1e-4, lam0*0.03)
    for _ in range(4000):
        lam -= step
        v = f(lam)
        if prev*v < 0:
            crossings += 1
            if crossings == ncross_target:
                lo, hi = lam, lam+step
                for _ in range(70):
                    mid = 0.5*(lo+hi)
                    if f(lo)*f(mid) <= 0: hi = mid
                    else: lo = mid
                return 0.5*(lo+hi), crossings
        prev = v
        step *= 1.15
        if lam < 1e-6: return None, crossings
    return None, crossings

def shoot_down_right(xs, rhos, lam0, yp_right, z0, ncross_target=1):
    """largest lam <= lam0 s.t. right-IVP (y(1/2)=0, slope yp_right) has y(z0)=0,
    ncross_target-th crossing (moving down). Reflection used."""
    xs_b, rhos_b = slice_rho(xs, rhos, z0, 0.5)
    xs_r = [0.5 - p for p in xs_b][::-1]
    rhos_r = rhos_b[::-1]
    def f(lam):
        return yval(xs_r, rhos_r, lam, 0.0, -yp_right, 0.0, 0.5-z0, 0.5-z0)
    lam = lam0; prev = f(lam0); crossings = 0
    step = max(1e-4, lam0*0.03)
    for _ in range(4000):
        lam -= step
        v = f(lam)
        if prev*v < 0:
            crossings += 1
            if crossings == ncross_target:
                lo, hi = lam, lam+step
                for _ in range(70):
                    mid = 0.5*(lo+hi)
                    if f(lo)*f(mid) <= 0: hi = mid
                    else: lo = mid
                return 0.5*(lo+hi), crossings
        prev = v
        step *= 1.15
        if lam < 1e-6: return None, crossings
    return None, crossings

rng = np.random.default_rng(777)
allok = True; nA = nB = 0
for trial in range(30):
    ncell = int(rng.integers(2, 5))
    xs = np.sort(rng.uniform(-0.45, 0.45, ncell))
    rhos = rng.uniform(1.0, 4.0, ncell+1)
    k = int(rng.integers(1, 4))
    m = k+1
    lam_m = eigval_N(xs, rhos, m); lam_2m = eigval_N(xs, rhos, 2*m)
    z0s = zeros_refined(xs, rhos, lam_m)
    z1s = zeros_refined(xs, rhos, lam_2m)
    if len(z0s) != m-1 or len(z1s) != 2*m-1: continue
    z0 = z0s[-1]; z_2k = z1s[-2]
    if not (0.05 < z0 < 0.95): continue
    # count zeros of y_2m strictly inside (z0, 1/2)
    c0 = len(z1s[z1s > z0])
    if c0 >= 2:
        nA += 1
        # right-end slope of y_2m (normalized slope 1 at -1/2)
        xs_in = [x for x in xs if -0.5 < x < 0.5]
        segs = [-0.5] + xs_in + [0.5]
        yy, yyp = 0.0, 1.0; cur = -0.5
        for i in range(len(segs)-1):
            x1 = segs[i+1]
            w = np.sqrt(lam_2m*rhos[i]); d = x1-cur
            y1 = yy*np.cos(w*d) + yyp/w*np.sin(w*d)
            yp1 = -w*yy*np.sin(w*d) + yyp*np.cos(w*d)
            yy, yyp = y1, yp1; cur = x1
        yp_right = yyp
        # crossings moving down: count goes c0 -> c0-1 -> ... ; the crossing where count 2->1
        # is the (c0-1)-th crossing (removes c0-1 zeros, leaving 1)
        ncross = c0 - 1
        lam_t, nc = shoot_down_right(xs, rhos, lam_2m, yp_right, z0, ncross_target=ncross)
        if lam_t is None:
            print(f"trial{trial} k={k} caseA(c0={c0}): shoot failed"); allok=False; continue
        # verify: lam_t = 2nd eigenvalue of (z0,1/2)-problem
        xs_b, rhos_b = slice_rho(xs, rhos, z0, 0.5)
        e2 = eigval_N(xs_b, rhos_b, 2, z0, 0.5)
        ok = abs(e2-lam_t)/lam_t < 1e-4 and lam_t <= lam_2m + 1e-6
        if not ok: allok=False
        print(f"trial{trial} k={k} caseA(c0={c0}): e2={e2:.5f} lam_t={lam_t:.5f} lam_2m={lam_2m:.5f} "
              f"e2/lam_m={e2/lam_m:.5f} ok={ok}")
    else:
        nB += 1
        # first crossing moving down from left: count 2k -> 2k-1
        lam_t, nc = shoot_down_left(xs, rhos, lam_2m, z0, ncross_target=1)
        if lam_t is None:
            print(f"trial{trial} k={k} caseB: shoot failed"); allok=False; continue
        xs_a, rhos_a = slice_rho(xs, rhos, -0.5, z0)
        e_2k = eigval_N(xs_a, rhos_a, 2*k, -0.5, z0)
        ok = abs(e_2k-lam_t)/lam_t < 1e-4 and lam_t <= lam_2m + 1e-6
        if not ok: allok=False
        print(f"trial{trial} k={k} caseB: e_2k={e_2k:.5f} lam_t={lam_t:.5f} lam_2m={lam_2m:.5f} "
              f"e_2k/lam_m={e_2k/lam_m:.5f} (2k:k ratio) ok={ok}")
print(f"MIN-case v2 done: nA={nA} nB={nB} allok={allok}")
