# -*- coding: utf-8 -*-
"""gap_n1_landscape2.py: full landscape of D(a,b) over SUP/INF families; locate all local extrema."""
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

if __name__ == "__main__":
    R = 4.0
    for mode in ("SUP","INF"):
        N = 120
        aa = np.linspace(0.001, 0.998, N)
        bb = np.linspace(0.001, 0.998, N)
        vals = np.zeros((N,N))
        for i,a in enumerate(aa):
            for j,b in enumerate(bb):
                if a+b > 0.999: vals[i,j] = np.nan; continue
                vals[i,j] = D_of(make_blocks(mode,R,a,b))
        g = np.where(~np.isnan(vals))
        print(f"mode={mode}: min={np.nanmin(vals):.6f} at a={aa[g[0][np.nanargmin(vals)]]:.4f} b={bb[g[1][np.nanargmin(vals)]]:.4f}")
        print(f"           max={np.nanmax(vals):.6f} at a={aa[g[0][np.nanargmax(vals)]]:.4f} b={bb[g[1][np.nanargmax(vals)]]:.4f}")
        # boundary values
        print("  boundary: rho=1:", D_of([(1.0,1.0)]), " rho=R:", D_of([(1.0,R)]))
        Dmax2 = 0; argmax2 = None
        for t in np.linspace(0.001,0.999,400):
            for bl in ([(t,1.0),(1-t,R)],[(t,R),(1-t,1.0)]):
                d = D_of(bl)
                if d > Dmax2: Dmax2, argmax2 = d, (bl, t)
        print(f"  max over 2-block boundary: D={Dmax2:.6f} at t={argmax2[1]:.4f} blocks={[ (round(L,3),int(c)) for L,c in argmax2[0]]}")
