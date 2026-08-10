# -*- coding: utf-8 -*-
"""Verify FH derivative sign: D'_sym = ?*2(R-1)*f_sym  for SUP/INF. R=4."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def blocks_of(mode, R, u):
    b = 1-2*u
    return [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]

def D_of(bl):
    s = lams_fast(bl, 2, npts=60000)
    return s[1]**2 - s[0]**2, s

def f_sym(mode, R, u):
    bl = blocks_of(mode, R, u)
    s = lams_fast(bl, 2, npts=60000)
    lam = s**2
    u1 = y_at(bl, s[0], np.array([u]))[0]/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], np.array([u]))[0]/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R=4 ====")
    for u in (0.1, 0.2, 0.3, 0.4, 0.4515, 0.47):
        f = f_sym(mode, R, u)
        h = 1e-5
        Dp, _ = D_of(blocks_of(mode, R, u+h))
        Dm, _ = D_of(blocks_of(mode, R, u-h))
        dD = (Dp-Dm)/(2*h)
        print(f"  u={u:.4f}: f_sym={f:+.6f}  dD/du={dD:+.4f}  +2(R-1)f={2*(R-1)*f:+.4f}  -2(R-1)f={-2*(R-1)*f:+.4f}")
