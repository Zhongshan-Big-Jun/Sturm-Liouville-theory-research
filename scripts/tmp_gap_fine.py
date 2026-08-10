# -*- coding: utf-8 -*-
"""Fine structure: z(u), h(u), V0(u) for large R; check INF R->inf V0->1? and h single crossing."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def blocks_of(mode, R, u):
    b = 1-2*u
    return [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]

def data(mode, R, u, npts=90000):
    bl = blocks_of(mode, R, u)
    s = lams_fast(bl, 2, npts=npts)
    lam = s**2
    n1 = norm2(bl, s[0]); n2 = norm2(bl, s[1])
    A = np.sqrt(n1/n2)  # u2'(0)/u1'(0) = sqrt(N1/N2)
    V0 = np.sqrt(lam[1]/lam[0])*A
    return lam, A, V0, bl, s

def f_of_x(mode, R, u, xs, npts=90000):
    lam,A,V0,bl,s = data(mode, R, u, npts)
    xs = np.atleast_1d(np.asarray(xs,float))
    u1 = y_at(bl, s[0], xs)/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], xs)/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def z_of(mode, R, u, npts=90000):
    lo, hi = 1e-8, 0.5
    for _ in range(55):
        mid = 0.5*(lo+hi)
        fm = f_of_x(mode, R, u, [mid], npts)[0]
        if fm > 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)

print("=== INF: V0(u) near its min, as R grows (V0 -> 1?) ===")
for R in (1e2, 1e3, 1e4, 1e5, 1e6):
    us = np.linspace(0.25, 0.40, 25)
    V0s = [data("INF", R, float(u))[2] for u in us]
    i = int(np.argmin(V0s))
    print(f"R={R:8.0f}: min V0 = {min(V0s):.6f} at u~{us[i]:.4f}")
print()
print("=== INF R=1000: fine z(u), h(u), increments ===")
R=1000.0
us = np.linspace(0.15, 0.45, 61)
prev=None; worst=(0,0); signs=0
for u in us:
    z = z_of("INF", R, float(u))
    h = z - u
    d = None if prev is None else h - prev[1]
    if prev is not None and prev[1]*h < 0: signs += 1
    if d is not None and (worst[1] is None or d > worst[1]): worst=(u,d)
    prev=(u,h)
print(f"  h sign changes: {signs}; max increment of h (should be <=0 if monotone): {worst}")
# print table in the interesting region
for u in np.linspace(0.28, 0.36, 17):
    z = z_of("INF", R, float(u)); print(f"    u={u:.4f} z={z:.6f} h={z-u:+.6f}")
print()
print("=== SUP R=1000: fine scan near crossing ===")
R=1000.0
us = np.linspace(0.40, 0.50, 41)
prev=None; signs=0
for u in us:
    z = z_of("SUP", R, float(u))
    h = z - u
    if prev is not None and prev[1]*h < 0: signs += 1
    prev=(u,h)
print(f"  h sign changes: {signs}")
for u in np.linspace(0.47, 0.50, 13):
    z = z_of("SUP", R, float(u)); print(f"    u={u:.4f} z={z:.6f} h={z-u:+.6f}")

