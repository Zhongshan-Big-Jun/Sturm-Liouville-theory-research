# -*- coding: utf-8 -*-
"""#3: precise scan of f(u) for n=1 configs [1,R,1] and [R,1,R]."""
import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
for sup in (True, False):
    tag = "SUP [1,R,1]" if sup else "INF [R,1,R]"
    print(f"=== {tag} ===")
    prev = None
    for u in np.linspace(0.05, 0.495, 90):
        v = 1-2*u
        blocks = [(u,1.0),(v,R),(u,1.0)] if sup else [(u,R),(v,1.0),(u,R)]
        s = lams_precise(blocks, 3)
        lam = s**2
        vp = eigfuns_precise(blocks, s[:2], np.array([u]))
        f = lam[0]*vp[0,0]**2 - lam[1]*vp[1,0]**2
        D = lam[1]-lam[0]
        if prev is not None and prev[1]*f < 0:
            print(f"  root between u={prev[0]:.4f} (f={prev[1]:+.3e}, D={prev[2]:.4f}) and u={u:.4f} (f={f:+.3e}, D={D:.4f})")
        prev = (u, f, D)
