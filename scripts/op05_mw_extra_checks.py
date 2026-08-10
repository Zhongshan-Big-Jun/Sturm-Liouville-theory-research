# -*- coding: utf-8 -*-
"""#5 extra checks: (1) C^1 cell pasting structure; (2) zero motion monotonicity."""
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

def rho_at(rhos, xs, t):
    j = 0
    while j < len(xs) and t > xs[j]: j += 1
    return rhos[j]

def build_phi_n(rhos0, xs0, n):
    cell = 1.0/n
    xs_n = []; rhos_n = []
    for j in range(n):
        xa_c = -0.5 + j*cell
        brk = sorted([xa_c + (x0+0.5)/n for x0 in xs0 if -0.5 < x0 < 0.5])
        pts = [xa_c] + brk + [xa_c+cell]
        for i in range(len(pts)-1):
            midx = 0.5*(pts[i]+pts[i+1])
            t = n*(midx - xa_c) - 0.5
            r = rho_at(rhos0, xs0, t)
            if pts[i] > -0.5 + 1e-12:
                xs_n.append(pts[i])
            rhos_n.append(r)
    return xs_n, rhos_n

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

print("=== Check 1: C^1 cell pasting (f_n restricted to cell j = const_j * y_1(cell map)) ===")
rng = np.random.default_rng(3)
ok1 = True
for trial in range(6):
    ncell = int(rng.integers(2, 4))
    xs0 = np.sort(rng.uniform(-0.4, 0.4, ncell))
    rhos0 = rng.uniform(1.0, 4.0, ncell+1)
    n = 3
    xs_n, rhos_n = build_phi_n(rhos0, xs0, n)
    # y_1 of phi_0, y_2 of phi_0
    lam1 = eigval_N(xs0, rhos0, 1); lam2 = eigval_N(xs0, rhos0, 2)
    # f_n, f_2n of phi_n
    lam_fn = eigval_N(xs_n, rhos_n, n); lam_f2n = eigval_N(xs_n, rhos_n, 2*n)
    # verify f_n is the y_1-paste: on each cell, ratio f_n(x)/y1(cell map) constant
    xg, fn = solve_iv(xs_n, rhos_n, lam_fn, 0.0, 1.0, -0.5, 0.5)
    cell = 1.0/n
    maxerr = 0.0
    for j in range(n):
        xa_c = -0.5 + j*cell
        m = (xg >= xa_c+1e-10) & (xg <= xa_c+cell-1e-10)
        xs_sel = xg[m]
        # y1 at cell-mapped argument: y1(u), u = n*(x - xa_c) - 1/2
        ratios = []
        for x in xs_sel[::7]:
            u = n*(x - xa_c) - 0.5
            y1u = yval(xs0, rhos0, lam1, 0.0, 1.0, -0.5, 0.5, u)
            if abs(y1u) > 1e-10:
                ratios.append(fn[m][list(xs_sel).index(x)]/y1u)
        r = np.array(ratios)
        spread = (r.max()-r.min())/(abs(r).max()+1e-30)
        maxerr = max(maxerr, spread)
    if maxerr > 1e-6:
        ok1 = False
        print(f"trial{trial}: f_n paste spread {maxerr:.2e}")
    print(f"trial{trial}: f_n cell-ratio spread = {maxerr:.2e} ; lam_n = {lam_fn:.6f} vs n^2*lam1 = {n*n*lam1:.6f} ; lam_2n = {lam_f2n:.6f} vs n^2*lam2 = {n*n*lam2:.6f}")
print("Check1 (C^1 pasting) all ok:", ok1)

print()
print("=== Check 2: zero motion monotonicity (left IVP: zeros move left as lam increases) ===")
ok2 = True
for trial in range(5):
    ncell = int(rng.integers(2, 4))
    xs = np.sort(rng.uniform(-0.45, 0.45, ncell))
    rhos = rng.uniform(1.0, 4.0, ncell+1)
    lam = 30.0 + 10.0*trial
    def zpos(lam):
        xg, y = solve_iv(xs, rhos, lam, 0.0, 1.0, -0.5, 0.5, npts=20000)
        idx = np.where((np.sign(y[:-1])*np.sign(y[1:])) < 0)[0]
        return 0.5*(xg[idx]+xg[idx+1])
    zA = zpos(lam); zB = zpos(lam*1.05)
    if len(zA) != len(zB):
        ok2 = False; print(f"trial{trial}: count mismatch"); continue
    if not np.all(zB < zA + 1e-9):
        ok2 = False; print(f"trial{trial}: monotonicity violated")
        print("zA:", zA, "zB:", zB)
print("Check2 (zero motion) all ok:", ok2)
