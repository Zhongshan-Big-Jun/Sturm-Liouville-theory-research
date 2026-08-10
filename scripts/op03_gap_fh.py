# -*- coding: utf-8 -*-
"""Test dD/du = (1-R)*f(u) for [1,R,1] (SUP) numerically."""
import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
def Df_at(u):
    v = 1-2*u
    blocks = [(u,1.0),(v,R),(u,1.0)]
    s = lams_precise(blocks, 3)
    lam = s**2
    vp = eigfuns_precise(blocks, s[:2], np.array([u]))
    f = lam[0]*vp[0,0]**2 - lam[1]*vp[1,0]**2
    return lam[1]-lam[0], f

for u in (0.40, 0.43, 0.45, 0.458):
    D, f = Df_at(u)
    eps = 1e-5
    Dp, _ = Df_at(u+eps)
    Dm, _ = Df_at(u-eps)
    num = (Dp-Dm)/(2*eps)
    print(f"u={u:.4f}: D={D:.6f} f={f:+.4e}  dD/du_num={num:+.4e}  (1-R)f={ (1-R)*f:+.4e}")
