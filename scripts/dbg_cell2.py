# -*- coding: utf-8 -*-
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

xs2 = [-0.25, 0.25]; rhos2 = [1.0, 2.0, 1.0]
for N in (1,2,3,4):
    print(N, eigval_N(xs2, rhos2, N))
# check what nz gives around lam4=113.7473
for lam in (113.0, 113.7473, 114.0, 110.0):
    _, y = solve_iv(xs2, rhos2, lam, 0.0, 1.0)
    print(lam, nz(y), y[-1])
