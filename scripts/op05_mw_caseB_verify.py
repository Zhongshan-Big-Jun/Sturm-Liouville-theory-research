# -*- coding: utf-8 -*-
"""#5 case-B verify: z1 < z0; truncate [z0, 1], right shooting; count zeros in (z0,1)."""
import numpy as np
def solve_piece(xs, rhos, lam, y0=0.0, yp0=1.0, npts=8001, rev=False):
    xg = np.linspace(0, 1, npts)
    y = np.zeros_like(xg); yp = np.zeros_like(xg)
    yy, yyp = y0, yp0
    x = 0.0
    for i, x1 in enumerate(xs):
        w = np.sqrt(lam*rhos[i])
        seg = np.linspace(x, x1, 200)
        ys = yy*np.cos(w*(seg-x)) + yyp/w*np.sin(w*(seg-x))
        yps = -w*yy*np.sin(w*(seg-x)) + yyp*np.cos(w*(seg-x))
        idx = (xg >= seg[0]-1e-12) & (xg <= seg[-1]+1e-12)
        y[idx] = np.interp(xg[idx], seg, ys); yp[idx] = np.interp(xg[idx], seg, yps)
        yy, yyp = ys[-1], yps[-1]; x = x1
    return xg, y, yp
def eigval_N(xs, rhos, N):
    lo, hi = 0.0, (N+5)**2*np.pi**2*max(1.0/min(rhos),1.0)
    for _ in range(90):
        mid = 0.5*(lo+hi)
        _, y, _ = solve_piece(xs, rhos, mid)
        nz = len(np.where((np.sign(y[:-1])*np.sign(y[1:])) < 0)[0])
        if nz < N: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
def interior_zeros(xs, rhos, lam):
    xg, y, _ = solve_piece(xs, rhos, lam)
    idx = np.where((np.sign(y[:-1])*np.sign(y[1:])) < 0)[0]
    z = 0.5*(xg[idx]+xg[idx+1])
    return z[(z > 1e-6) & (z < 1-1e-6)]

for name, xs, rhos, k in [
    ("asym [1,0.25,1,0.6]", [0.25, 0.6, 0.75, 1.0], [1.0, 0.25, 1.0, 0.6], 2),
    ("asym [1,0.25,1,0.6]", [0.25, 0.6, 0.75, 1.0], [1.0, 0.25, 1.0, 0.6], 3),
    ("sym [1,0.1,1]", [0.3, 0.7, 1.0], [1.0, 0.1, 1.0], 2),
]:
    n = k+1
    lam_n, lam_2n = eigval_N(xs, rhos, n), eigval_N(xs, rhos, 2*n)
    z0s = interior_zeros(xs, rhos, lam_n); z1s = interior_zeros(xs, rhos, lam_2n)
    z0 = z0s[-1]; z1 = z1s[-2]
    if z1 >= z0:
        print(f"{name} k={k}: NOT case B (z0={z0:.4f} z1={z1:.4f})"); continue
    # right shooting: solve backwards from x=1
    # y(1)=0, y'(1)= y'_2n(1); need yp at end. solve forward to get y2n then derivative at 1.
    xg0, y2n, y2np = solve_piece(xs, rhos, lam_2n)
    yp1 = y2np[-1]
    # backward propagation: transform x -> 1-x, rho(x) -> rho(1-x)
    def shoot_val(lam):
        # solve on [z0,1] from right: y(1)=0, y'(1)=yp1. Use reflected coordinates.
        xs_r = [1.0 - x for x in xs][::-1]
        rhos_r = rhos[::-1]
        # initial data at reflected x=0 (original x=1): y=0, y'=yp1 (derivative sign flips)
        _, yy, _ = solve_piece(xs_r, rhos_r, lam, y0=0.0, yp0=-yp1)
        # yy at reflected coordinate t = 1 - x; evaluate at t = 1 - z0
        return np.interp(1.0 - z0, np.linspace(0,1,len(yy)), yy)
    v0 = shoot_val(lam_2n)
    lam = lam_2n; prev = v0; lam_t = None
    for _ in range(40000):
        lam += 1.0
        v = shoot_val(lam)
        if prev*v < 0:
            lo, hi = lam-1.0, lam
            for _ in range(50):
                mid = 0.5*(lo+hi)
                if shoot_val(lo)*shoot_val(mid) <= 0: hi = mid
                else: lo = mid
            lam_t = 0.5*(lo+hi); break
        prev = v
        if lam > 2e5: break
    # count zeros of tilde-y in (z0, 1) via reflected solution
    xs_r = [1.0 - x for x in xs][::-1]; rhos_r = rhos[::-1]
    tr, yt, _ = solve_piece(xs_r, rhos_r, lam_t, y0=0.0, yp0=-yp1)
    m = (tr > 1e-6) & (tr < 1.0-z0-1e-6)
    sgn = np.sign(yt[m])
    cnt = len(np.where((sgn[:-1]*sgn[1:]) < 0)[0])
    print(f"{name} k={k}: z0={z0:.4f} z1={z1:.4f} caseB: lam2n/lamn={lam_2n/lam_n:.4f} "
          f"lam_t/lamn={lam_t/lam_n:.4f} zeros_tilde_in(z0,1)={cnt} (expect 1)")
