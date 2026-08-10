# -*- coding: utf-8 -*-
"""Check: does symmetrization (keeping R-mass b-a fixed) increase D?
D(a,b) vs D(as, 1-as) with as = (1-b+a)/2. R=4."""
import numpy as np
from gap_lib import lams_fast

R = 4.0
def D_of(a, b):
    if b <= a: return np.nan
    s = lams_fast([(a,1.0),(b-a,R),(1-b,1.0)], 3)**2
    return s[1]-s[0]

bad = 0; tot = 0
for a in np.linspace(0.05, 0.45, 13):
    for b in np.linspace(a+0.05, 0.95, 15):
        as_ = (1 - b + a)/2
        if as_ <= 0 or as_ >= 0.5: continue
        D1 = D_of(a, b); D2 = D_of(as_, 1-as_)
        tot += 1
        if not (D2 >= D1 - 1e-9):
            bad += 1
            if bad < 6: print(f"violation: a={a:.3f} b={b:.3f} D={D1:.5f} vs sym D={D2:.5f}")
print(f"total={tot} violations={bad}")
# also check: fix width w=b-a, is D maximized when centered? sample widths
print("--- fix width, vary center ---")
for w in (0.05, 0.1, 0.15, 0.2):
    best = (-1e9, None)
    for a in np.linspace(0.01, 1-w-0.01, 30):
        D = D_of(a, a+w)
        if D > best[0]: best = (D, a)
    print(f"width w={w}: best D={best[0]:.5f} at a={best[1]:.4f} (center={best[1]+w/2:.4f})")
