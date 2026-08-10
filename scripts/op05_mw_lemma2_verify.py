# -*- coding: utf-8 -*-
"""#5 verify MW Lemma 2 count (exact bisection)."""
import numpy as np
def solve_piece(xs, rhos, lam, y0=0.0, yp0=1.0, npts=8001):
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

for name, xs, rhos in [
    ("sym [1,0.25,1]", [0.25, 0.75, 1.0], [1.0, 0.25, 1.0]),
    ("asym [1,0.25,1,0.6]", [0.25, 0.6, 0.75, 1.0], [1.0, 0.25, 1.0, 0.6]),
    ("sym [1,0.1,1]", [0.3, 0.7, 1.0], [1.0, 0.1, 1.0]),
]:
    for k in (2, 3):
        n = k+1
        lam_n, lam_2n = eigval_N(xs, rhos, n), eigval_N(xs, rhos, 2*n)
        z0s = interior_zeros(xs, rhos, lam_n)
        z1s = interior_zeros(xs, rhos, lam_2n)
        z0 = z0s[-1]; z1 = z1s[-2]
        _, _, y2np = solve_piece(xs, rhos, lam_2n)
        xg0, _, _ = solve_piece(xs, rhos, lam_2n)
        def shoot_val(lam):
            _, yy, _ = solve_piece(xs, rhos, lam, y0=0.0, yp0=y2np[0])
            return np.interp(z0, xg0, yy)
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
        _, yt, _ = solve_piece(xs, rhos, lam_t, y0=0.0, yp0=y2np[0])
        m = (xg0 > 1e-6) & (xg0 < z0-1e-6)
        sgn = np.sign(yt[m])
        cnt = len(np.where((sgn[:-1]*sgn[1:]) < 0)[0])
        z0c = len(z0s); z1c = len(z1s)
        print(f"{name} k={k}: z0={z0:.4f}(#{z0c}) z1={z1:.4f}(#{z1c}) "
              f"case={'A:z0<=z1' if z0<=z1 else 'B:z1<z0'} lam2n/lamn={lam_2n/lam_n:.4f} "
              f"lam_t/lamn={lam_t/lam_n:.4f} zeros_tilde_in(0,z0)={cnt} (need 2k-1={2*k-1})")
