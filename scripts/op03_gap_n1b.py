# -*- coding: utf-8 -*-
"""#3 n=1 gap: refine self-consistent extrema for R=4.
Max config [1,R,1]: f(x)=lam1*u1^2-lam2*u2^2, self-consistency f(junction)=0.
Min config [R,1,R]: same condition.
Also check f(x) profile on a fine grid to confirm exactly two zeros.
"""
import numpy as np
from op03_gap_n1 import lams_blocks, eigfuns_at

def f_at_junction(blocks, lam):
    """f at first junction point x = blocks[0][0]."""
    u = blocks[0][0]
    pts = np.array([u])
    vals = eigfuns_at(blocks, lam[:2], pts)
    return lam[0]*vals[0][0]**2 - lam[1]*vals[1][0]**2

def solve_u(R, heavy_middle):
    """bisection on f(u)=0 for [1,R,1] (heavy_middle=True) or [R,1,R]."""
    lo, hi = 0.05, 0.49
    for _ in range(60):
        u = 0.5*(lo+hi)
        v = 1-2*u
        if heavy_middle:
            blocks = [(u,1.0),(v,R),(u,1.0)]
        else:
            blocks = [(u,R),(v,1.0),(u,R)]
        lam = lams_blocks(blocks, k=3)
        f = f_at_junction(blocks, lam)
        if f < 0:
            lo = u
        else:
            hi = u
    return 0.5*(lo+hi)

def f_profile(blocks, lam, npts=400):
    xs = np.linspace(1e-4, 1-1e-4, npts)
    pts = np.array(sorted(set(np.round(xs, 8))))
    vals = eigfuns_at(blocks, lam[:2], pts)
    f = lam[0]*vals[0]**2 - lam[1]*vals[1]**2
    return pts, f

R = 4.0
for heavy_middle in (True, False):
    u = solve_u(R, heavy_middle)
    v = 1-2*u
    if heavy_middle:
        blocks = [(u,1.0),(v,R),(u,1.0)]
        tag = "MAX [1,R,1]"
    else:
        blocks = [(u,R),(v,1.0),(u,R)]
        tag = "MIN [R,1,R]"
    lam = lams_blocks(blocks, k=3)
    D = lam[1]-lam[0]
    pts, f = f_profile(blocks, lam)
    nz = np.sum(np.signbit(f[1:]) != np.signbit(f[:-1]))
    print(f"{tag}: u={u:.10f} v={v:.10f} lam1={lam[0]:.8f} lam2={lam[1]:.8f} D={D:.8f}")
    print(f"   sign changes of f on (0,1): {nz}, f at ends: {f[0]:+.3e}, {f[-1]:+.3e}")
    # check f>0 inside central band, f<0 outside for max
    inside = (pts > u) & (pts < 1-u)
    print(f"   f>0 on central band: {np.all(f[inside] > 0)}  f<0 on ends: {np.all(f[~inside] < 0)}")
print(f"constant rho=1: D = {3*np.pi**2:.6f};  constant rho=R: D = {3*np.pi**2/R:.6f}")
