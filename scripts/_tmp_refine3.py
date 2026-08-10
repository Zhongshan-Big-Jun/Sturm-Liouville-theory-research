# -*- coding: utf-8 -*-
"""Refine candidate self-consistent points and check residual + Hessian."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

R = 4.0

def fvals(ab):
    a, b = ab
    blocks = [(a,1.0),(b-a,R),(1-b,1.0)]
    s = lams_fast(blocks, 3)
    lam = s**2
    out = []
    for k in (0,1):
        y = y_at(blocks, s[k], np.array([a, b]))
        u = y/np.sqrt(norm2(blocks, s[k]))
        out.append(u)
    u1, u2 = out
    return np.array([lam[0]*u1[0]**2 - lam[1]*u2[0]**2, lam[0]*u1[1]**2 - lam[1]*u2[1]**2])

def D_of(ab):
    a, b = ab
    blocks = [(a,1.0),(b-a,R),(1-b,1.0)]
    s = lams_fast(blocks, 3)**2
    return s[1]-s[0]

cands = [(0.442,0.529),(0.452,0.558),(0.461,0.576),(0.4515,0.5485)]
for c in cands:
    sol = least_squares(fvals, c, bounds=([0.01,0.51],[0.49,0.99]), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=200)
    ab = sol.x
    res = np.max(np.abs(fvals(ab)))
    D = D_of(ab)
    print(f"from {c}: refined (a,b)=({ab[0]:.6f},{ab[1]:.6f}) res={res:.2e} D={D:.6f}")
