# -*- coding: utf-8 -*-
"""#5 MW Lemma 1-2 audit v3 (fixed build_phi_n)."""
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

def interior_zeros(xs, rhos, lam, xa=-0.5, xb=0.5):
    xg, y = solve_iv(xs, rhos, lam, 0.0, 1.0, xa, xb)
    idx = np.where((np.sign(y[:-1])*np.sign(y[1:])) < 0)[0]
    z = 0.5*(xg[idx]+xg[idx+1])
    return z[(z > xa+1e-6) & (z < xb-1e-6)]

def rho_at(rhos, xs, t):
    j = 0
    while j < len(xs) and t > xs[j]: j += 1
    return rhos[j]

def build_phi_n(rhos0, xs0, n):
    cell = 1.0/n
    xs_n = []; rhos_n = []
    for j in range(n):
        xa_c = -0.5 + j*cell
        brk = [xa_c + (x0+0.5)/n for x0 in xs0 if -0.5 < x0 < 0.5]
        brk = sorted(brk)
        pts = [xa_c] + brk + [xa_c+cell]
        for i in range(len(pts)-1):
            midx = 0.5*(pts[i]+pts[i+1])
            t = n*(midx - xa_c) - 0.5
            r = rho_at(rhos0, xs0, t)
            if pts[i] > -0.5 + 1e-12:
                xs_n.append(pts[i])
            rhos_n.append(r)
    return xs_n, rhos_n

print("=== Lemma 1: cell extension ratio identity ===")
rng = np.random.default_rng(7)
allok = True
for trial in range(8):
    ncell = int(rng.integers(2, 5))
    xs0 = np.sort(rng.uniform(-0.4, 0.4, ncell))
    rhos0 = rng.uniform(1.0, 4.0, ncell+1)
    lam1 = eigval_N(xs0, rhos0, 1); lam2 = eigval_N(xs0, rhos0, 2)
    base = lam2/lam1
    for n in (2, 3):
        xs_n, rhos_n = build_phi_n(rhos0, xs0, n)
        # sanity: phi_n in [1,4]
        assert min(rhos_n) >= 0.999 and max(rhos_n) <= 4.001
        l1 = eigval_N(xs_n, rhos_n, n); l2 = eigval_N(xs_n, rhos_n, 2*n)
        err = abs((l2/l1) - base)/base
        if err > 1e-4: allok = False
        print(f"trial{trial} n={n}: base={base:.8f} got={l2/l1:.8f} relerr={err:.2e}")
print("Lemma1 all ok:", allok)
