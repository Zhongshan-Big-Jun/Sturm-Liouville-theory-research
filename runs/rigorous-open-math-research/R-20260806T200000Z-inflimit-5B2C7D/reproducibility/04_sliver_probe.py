# -*- coding: utf-8 -*-
"""04_sliver_probe.py
Boundary sliver profiles for the symmetric well [R,1,R]:
 (a) u -> 0: R*D_R(u) is large; document the light/heavy regimes and the
     crossover u ~ 1/sqrt(R).
 (b) u -> 1/2: R*D_R(u) -> 3 pi^2 from below; document the elementary bound
     R*D_R(u) >= 4 pi^2 - pi^2 R/(R - 2(R-1)v), v = 1-2u, for u >= 0.45.
Uses the exact transfer-matrix secular equation with a robust root finder.
ASCII punctuation. Run: python 04_sliver_probe.py
"""
import numpy as np
from scipy.optimize import brentq

def secular_arr(lam, u, R):
    kR = np.sqrt(lam*R); k1 = np.sqrt(lam)
    cR, sR = np.cos(kR*u), np.sin(kR*u)
    c1, s1 = np.cos(k1*(1-2*u)), np.sin(k1*(1-2*u))
    A00 = cR*c1 - sR/kR*k1*s1
    A01 = cR*s1/k1 + sR/kR*c1
    A10 = -kR*sR*c1 - cR*k1*s1
    A11 = -kR*sR*s1/k1 + cR*c1
    return A00*sR/kR + A01*cR

def eig2(u, R, lam_max=500.0, n_pts=800000):
    grid = np.linspace(1e-9, lam_max, n_pts)
    v = secular_arr(grid, u, R)
    sg = np.signbit(v)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    roots = []
    for i in idx[:2]:
        r = brentq(lambda l: secular_arr(np.array([l]), u, R)[0], grid[i], grid[i+1])
        roots.append(r)
    if len(roots) < 2:
        return None
    return roots[0], roots[1]

print("(a) u -> 0 sliver: R*D_R(u) for u = c/sqrt(R)")
for R in [1e3, 1e6]:
    print("  R =", R)
    for c in [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:
        u = c/np.sqrt(R)
        r = eig2(u, R)
        if r is None:
            print(f"    c={c}: FAIL"); continue
        l1, l2 = r
        print(f"    c={c}: u={u:.2e} R*D={R*(l2-l1):.6f}")

print("(b) u -> 1/2 sliver: R*D_R(u) vs elementary bound")
for u in [0.45, 0.47, 0.49, 0.495]:
    v = 1 - 2*u
    for R in [10.0, 1e3, 1e6]:
        r = eig2(u, R)
        if r is None:
            print(f"  u={u} R={R}: FAIL"); continue
        l1, l2 = r
        bound = 4*np.pi**2 - np.pi**2*R/(R - 2*(R-1)*v)
        print(f"  u={u} R={R:7.0e}: R*D={R*(l2-l1):.6f}  bound={bound:.6f}  OK={R*(l2-l1) >= bound}")
print("3*pi^2 =", 3*np.pi**2, " Dbar* = 24.94386613843234")