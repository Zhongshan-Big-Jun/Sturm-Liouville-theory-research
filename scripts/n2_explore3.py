# -*- coding: utf-8 -*-
"""Explore D_sym(u) concavity (2nd derivative) and fixed-point geometry."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

NPT = 1500
def s_of(blocks, npts=NPT): return lams_fast(blocks, 2, npts=npts)
def D_of(blocks, s=None):
    if s is None: s = s_of(blocks)
    return s[1]**2 - s[0]**2
def f_at(blocks, x, s=None):
    if s is None: s = s_of(blocks)
    lam = s**2
    x = np.clip(np.atleast_1d(np.asarray(x, float)), 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], x)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], x)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def make_blocks(mode, R, u):
    if mode == "SUP": return [(u,1.0),(1-2*u,R),(u,1.0)]
    return [(u,R),(1-2*u,1.0),(u,R)]

print("=== D_sym(u) second-difference: concave (SUP) / convex (INF)? ===")
for R in (2.0, 4.0, 10.0, 100.0):
    for mode in ("SUP","INF"):
        us = np.linspace(0.04, 0.47, 60)
        Ds = np.array([D_of(make_blocks(mode,R,u)) for u in us])
        d2 = np.diff(Ds, 2)
        d1 = np.diff(Ds)
        # sign structure of second difference
        neg = (d2 < 0).mean(); pos = (d2 > 0).mean()
        nz = np.sum(np.abs(d2) < 1e-9)
        # locations where d1 changes sign (critical pts)
        sc = np.sum(d1[1:]*d1[:-1] < 0)
        print(f"R={R:6.1f} {mode}: D'(u) sign changes={sc};  2nd-diff neg fraction={neg:.2f} pos={pos:.2f}; min d2={d2.min():.2e} max d2={d2.max():.2e}")
