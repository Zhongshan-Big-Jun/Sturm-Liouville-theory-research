# -*- coding: utf-8 -*-
"""Compute z(u) = unique zero of f(x; config(u)) on (0,1/2); check z(u)-u monotonicity."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def f_of_x(mode, R, u, xs, npts=60000):
    b = 1-2*u
    bl = [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]
    s = lams_fast(bl, 2, npts=npts)
    lam = s**2
    u1 = y_at(bl, s[0], np.asarray(xs,float))/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], np.asarray(xs,float))/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s, bl

def z_of(mode, R, u, npts=60000):
    # bracket: f(eps)<0, f(0.5)>0; bisect on sign using f of x
    lo, hi = 1e-7, 0.5
    for _ in range(60):
        mid = 0.5*(lo+hi)
        fm,_,_ = f_of_x(mode, R, u, [mid], npts)
        if fm > 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R={R}: z(u) and z(u)-u ====")
    us = [0.02,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.38,0.4,0.45,0.48,0.49]
    prev = None
    mono = True
    for u in us:
        z = z_of(mode, R, u)
        diff = z - u
        if prev is not None and diff >= prev[1] - 1e-9:
            mono = False
            print(f"  u={u:.3f}: z={z:.6f} z-u={diff:+.6f}   <-- NON-MONOTONE (prev {prev[0]:.3f} -> {prev[1]:+.6f})")
        else:
            print(f"  u={u:.3f}: z={z:.6f} z-u={diff:+.6f}")
        prev = (u, diff)
    print(f"  monotone decreasing: {mono}")
    print()
