# -*- coding: utf-8 -*-
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
    for _ in range(80):
        mid = 0.5*(lo+hi)
        _, y, _ = solve_piece(xs, rhos, mid)
        nz = len(np.where((np.sign(y[:-1])*np.sign(y[1:])) < 0)[0])
        if nz < N: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
def interior_zeros(xs, rhos, lam):
    xg, y, yp = solve_piece(xs, rhos, lam)
    idx = np.where((np.sign(y[:-1])*np.sign(y[1:])) < 0)[0]
    z = 0.5*(xg[idx]+xg[idx+1])
    return z, y
xs = [0.25, 0.75, 1.0]; rhos = [1.0, 0.25, 1.0]
for n in (3, 6):
    lam = eigval_N(xs, rhos, n)
    z, y = interior_zeros(xs, rhos, lam)
    print(f"lambda_{n} = {lam:.6f}, y(1) = {y[-1]:.2e}, zeros: {[round(float(q),4) for q in z]}")
