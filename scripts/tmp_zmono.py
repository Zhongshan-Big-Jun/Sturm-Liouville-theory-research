# -*- coding: utf-8 -*-
"""Sweep R: check z(u)-u strictly decreasing for SUP and INF."""
import numpy as np
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
    lo, hi = 1e-7, 0.5
    for _ in range(50):
        mid = 0.5*(lo+hi)
        fm,_,_ = f_of_x(mode, R, u, [mid], npts)
        if fm > 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)

for R in (1.1, 1.5, 2.0, 3.0, 6.0, 10.0, 30.0, 100.0, 1000.0):
    for mode in ("SUP","INF"):
        us = np.linspace(0.01, 0.49, 40)
        prev = None; ok = True; mindiff = 1e9
        for u in us:
            z = z_of(mode, R, float(u))
            d = z - u
            if prev is not None and d > prev + 1e-10:
                ok = False
            mindiff = min(mindiff, prev-d if prev is not None else 1e9)
            prev = d
        print(f"R={R:7.0f} {mode}: z(u)-u strictly decreasing on grid: {ok} (min decrement {mindiff:.4e})")
