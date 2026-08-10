# -*- coding: utf-8 -*-
"""#3: asymmetric [1,R,1] / [R,1,R] grid scan (vectorized)."""
import numpy as np
from op03_gap_fixed import lams_precise

R = 4.0
def lams_vec(blocks, k, npts=8000, smax=60.0):
    s = np.linspace(1e-9, smax, npts)
    M00 = np.ones(npts); M01 = np.zeros(npts); M10 = np.zeros(npts); M11 = np.ones(npts)
    for L, c in blocks:
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
    d = M01
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    return (s[idx[:k]]**2)

for sup, ref, tag in [(True, 32.61398362, "[1,R,1] SUP"), (False, 6.78448234, "[R,1,R] INF")]:
    a = R if not sup else 1.0
    b = 1.0 if not sup else R
    best = (1e9, None)
    grid = np.linspace(0.15, 0.48, 26)
    for uL in grid:
        for uR in grid:
            if uL + uR > 0.97: continue
            blocks = [(uL, a), (1-uL-uR, b), (uR, a)]
            lam = lams_vec(blocks, 3)
            D = lam[1]-lam[0]
            if D < best[0]: best = (D, (uL, uR))
    print(f"{tag}: grid best D={best[0]:.6f} at uL,uR={best[1]} (symmetric ref={ref:.6f})")
