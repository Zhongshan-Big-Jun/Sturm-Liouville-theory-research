# -*- coding: utf-8 -*-
"""Explore 2-block monotonicity + symmetric family structure (session 15). Efficient."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

NPT = 900

def s_of(blocks, npts=NPT):
    return lams_fast(blocks, 2, npts=npts)

def D_of(blocks, s=None):
    if s is None:
        s = s_of(blocks)
    return s[1]**2 - s[0]**2

def f_at(blocks, x, s=None):
    if s is None:
        s = s_of(blocks)
    lam = s**2
    x = np.clip(np.atleast_1d(np.asarray(x, float)), 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], x)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], x)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

print("=== 2-block [1,R]: D(t) monotone increasing? dD/dt = -(R-1) f(t), want f(t)<0 ===")
for R in (1.5, 2.0, 4.0, 10.0, 100.0):
    ts = np.linspace(0.02, 0.98, 25)
    Ds = [D_of([(t,1.0),(1-t,R)]) for t in ts]
    diffs = np.diff(Ds)
    mono = np.all(diffs > 0)
    fs = [f_at([(t,1.0),(1-t,R)], t)[0] for t in ts]
    print(f"R={R:6.1f}: mono_incr={mono}  min dD={diffs.min():.3e}  max f(t)={max(fs):+.3e}")

print("=== 2-block [R,1]: D(t) monotone decreasing? want f(t)>0 ===")
for R in (1.5, 2.0, 4.0, 10.0):
    ts = np.linspace(0.02, 0.98, 25)
    Ds = [D_of([(t,R),(1-t,1.0)]) for t in ts]
    diffs = np.diff(Ds)
    mono = np.all(diffs < 0)
    fs = [f_at([(t,R),(1-t,1.0)], t)[0] for t in ts]
    print(f"R={R:6.1f}: mono_decr={mono}  max dD={diffs.max():.3e}  min f(t)={min(fs):+.3e}")

print()
print("=== symmetric family: D(u), D'(u) sign structure ===")
def make_blocks(mode, R, u):
    if mode == "SUP":
        return [(u,1.0),(1-2*u,R),(u,1.0)]
    return [(u,R),(1-2*u,1.0),(u,R)]

for R in (2.0, 4.0, 10.0):
    for mode in ("SUP","INF"):
        us = np.linspace(0.03, 0.48, 15)
        vals = []
        for u in us:
            bl = make_blocks(mode, R, u)
            s = s_of(bl)
            vals.append((D_of(bl, s), f_at(bl, u, s)[0]))
        Ds = [v[0] for v in vals]; fs = [v[1] for v in vals]
        peak = max(Ds); trough = min(Ds)
        # count sign changes of D'(u) ~ -f(u): D' = (R-1)(lam2 u2^2 - lam1 u1^2) = -(R-1) f
        sc = sum(1 for i in range(len(fs)-1) if fs[i]*fs[i+1] < 0)
        print(f"R={R:4.1f} {mode}: D range [{min(Ds):.4f},{max(Ds):.4f}]  f sign changes: {sc}  f(endpoints): {fs[0]:+.3e}, {fs[-1]:+.3e}")
