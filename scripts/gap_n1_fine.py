# -*- coding: utf-8 -*-
"""gap_n1_fine.py: fine scan around symmetric point vs other candidates."""
import numpy as np
from gap_lib import lams_fast

def D_of(blocks):
    s = lams_fast(blocks, 2)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

R = 4.0
print("SUP symmetric point [1,4,1] u=0.4514855:")
print("  D =", D_of([(0.4514855,1.0),(0.097029,4.0),(0.4514855,1.0)]))
print("INF symmetric point [4,1,4] u=0.3825983:")
print("  D =", D_of([(0.3825983,4.0),(0.2348034,1.0),(0.3825983,4.0)]))

for mode in ("SUP","INF"):
    # fine grid over central region
    N = 200
    aa = np.linspace(0.25, 0.75, N)
    bb = np.linspace(0.005, 0.40, N) if mode=="SUP" else np.linspace(0.005, 0.45, N)
    vals = np.full((N,N), np.nan)
    for i,a in enumerate(aa):
        for j,b in enumerate(bb):
            if a+b > 0.999: continue
            vals[i,j] = D_of(make_blocks(mode,R,a,b))
    g = np.where(~np.isnan(vals))
    imax = np.unravel_index(np.nanargmax(vals), vals.shape)
    imin = np.unravel_index(np.nanargmin(vals), vals.shape)
    print(f"mode={mode} fine grid: max={vals[imax]:.8f} at a={aa[imax[0]]:.4f} b={bb[imax[1]]:.4f} c={1-aa[imax[0]]-bb[imax[1]]:.4f}")
    print(f"                    min={vals[imin]:.8f} at a={aa[imin[0]]:.4f} b={bb[imin[1]]:.4f} c={1-aa[imin[0]]-bb[imin[1]]:.4f}")
