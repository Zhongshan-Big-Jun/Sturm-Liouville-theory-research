# -*- coding: utf-8 -*-
"""explore_2.py: test NEW convexity mechanisms.
Claim W: D_ww(w,0) < 0 on the axis (b = 1-a), i.e. d''(a) > 0 for d(a)=D(a,1-a).
Claim T: D_tt(w,t) < 0 on the whole triangle, D_tt = (D_aa+2D_ab+D_bb)/4."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1_lib as L
from explore_1 import roots2_adaptive, cfg2, R1R2, partials2, hessian2, Dval

def scan_axis(R, n=61):
    """d(a) = D(a,1-a) on a in (0.01, 0.49); d'', D_ww."""
    out = []
    for a in np.linspace(0.02, 0.49, n):
        b = 1.0 - a
        Daa, Dab, Dbb, p = hessian2(a, b, R)
        Dww = (Daa - 2*Dab + Dbb)/4.0
        Dtt = (Daa + 2*Dab + Dbb)/4.0
        # d''(a): d(a)=D(a,1-a); d' = Da - Db; d'' = Daa - 2Dab + Dbb = 4*Dww
        out.append((a, Dww, Dtt, Daa, Dab, Dbb))
    return out

def scan_triangle(R, n=40):
    """D_tt over the triangle grid."""
    worst = (1e99, None); worst_ww = (1e99, None)
    min_tt = 1e99; max_tt = -1e99
    for a in np.linspace(0.05, 0.93, n):
        for b in np.linspace(a+0.02, 0.98, n):
            if b >= 1.0: continue
            Daa, Dab, Dbb, p = hessian2(a, b, R)
            Dww = (Daa - 2*Dab + Dbb)/4.0
            Dtt = (Daa + 2*Dab + Dbb)/4.0
            min_tt = min(min_tt, Dtt); max_tt = max(max_tt, Dtt)
            if Dtt < worst[0]: worst = (Dtt, (a,b))
            if Dww < worst_ww[0]: worst_ww = (Dww, (a,b))
    return min_tt, max_tt, worst, worst_ww

if __name__ == "__main__":
    for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e6]:
        ax = scan_axis(R, n=41)
        dww = [x[1] for x in ax]; dtt = [x[2] for x in ax]
        print(f"R={R:9g}: axis D_ww min={min(dww):+.4e} max={max(dww):+.4e} | "
              f"axis D_tt min={min(dtt):+.4e} max={max(dtt):+.4e}")
