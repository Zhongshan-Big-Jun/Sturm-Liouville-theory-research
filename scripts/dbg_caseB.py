# -*- coding: utf-8 -*-
import numpy as np
# debug case B shooting
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

rng = np.random.default_rng(123)
# reproduce trial 9 (k=2 caseB shoot failed)
# regenerate trials 0..9 same as audit: we need same sequence; simpler: loop trials and break at 9
xs = rhos = None
for trial in range(10):
    ncell = int(rng.integers(2, 5))
    xs = np.sort(rng.uniform(-0.45, 0.45, ncell))
    rhos = rng.uniform(1.0, 4.0, ncell+1)
    k = int(rng.integers(1, 4))
    if trial == 9: break
m = k+1
lam_m = eigval_N(xs, rhos, m); lam_2m = eigval_N(xs, rhos, 2*m)
z0s = interior_zeros(xs, rhos, lam_m); z1s = interior_zeros(xs, rhos, lam_2m)
z0 = z0s[-1]; z1 = z1s[-2]
print("k=",k,"xs=",xs,"rhos=",rhos)
print("lam_m=",lam_m,"lam_2m=",lam_2m,"z0=",z0,"z1=",z1)
# yp at right end via transfer
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
print("yp_right=", yp_right)
xs_b, rhos_b = slice_rho(xs, rhos, z0, 0.5)
xs_r = [0.5 - p for p in xs_b][::-1]; rhos_r = rhos_b[::-1]
print("xs_b=", xs_b, "rhos_b=", rhos_b)
print("xs_r=", xs_r, "rhos_r=", rhos_r)
def f(lam):
    xg, y = solve_iv(xs_r, rhos_r, lam, 0.0, -yp_right, 0.0, 0.5-z0)
    return np.interp(0.5-z0, xg, y)
print("f(lam_2m)=", f(lam_2m))
# also y_{2m}(z0) directly
xg2, y2 = solve_iv(xs, rhos, lam_2m, 0.0, 1.0, -0.5, 0.5)
print("y_2m(z0)=", np.interp(z0, xg2, y2))
for lam in np.linspace(lam_2m, lam_2m*1.1, 21):
    print(f"  lam={lam:.4f} f={f(lam):+.6e}")
