# -*- coding: utf-8 -*-
"""Debug: compare f(u) from precise vs coarse routines for [1,R,1] and [R,1,R]."""
import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise
from op03_gap_n1 import lams_blocks, eigfuns_at

R = 4.0

def blocks_from(u, R, sup):
    v = 1-2*u
    if sup:
        return [(u,1.0),(v,R),(u,1.0)]
    return [(u,R),(v,1.0),(u,R)]

for sup, uvals, label in [(True, [0.4515, 0.4597], "SUP [1,R,1]"), (False, [0.3826, 0.45], "INF [R,1,R]")]:
    for u in uvals:
        blocks = blocks_from(u, R, sup)
        s_coarse = np.sqrt(lams_blocks(blocks, k=3))
        s_prec = lams_precise(blocks, 3)
        print(f"{label} u={u}:")
        print(f"   s^2 coarse = {s_coarse**2}, precise = {s_prec**2}")
        pts = np.array([u, 0.5, 1-u])
        vc = eigfuns_at(blocks, s_coarse[:2]**2, pts)
        vp = eigfuns_precise(blocks, s_prec[:2], pts)
        fc = s_coarse[0]**2*vc[0]**2 - s_coarse[1]**2*vc[1]**2
        fp = s_prec[0]**2*vp[0]**2 - s_prec[1]**2*vp[1]**2
        print(f"   f at junction: coarse={fc[0]:.6e}  precise={fp[0]:.6e}")
        print(f"   u1^2,u2^2 coarse: {vc[0,0]:.6f},{vc[1,0]:.6f} | precise: {vp[0,0]:.6f},{vp[1,0]:.6f}")
