# -*- coding: utf-8 -*-
"""Structure of D(a,b) over the triangle: for each b, where is max over a?"""
import numpy as np
from gap_lib import lams_fast

def D_of(blocks, npts=1000):
    s = lams_fast(blocks, 2, npts=npts)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

for R in (4.0, 2.0, 10.0):
    for mode in ("SUP",):
        print(f"=== R={R} {mode}: max over a for each b ===")
        print(f"{'b':>6} {'a_max':>9} {'D_max':>10} {'D_center':>10} {'D_boundary':>10} {'center-bndry':>12} {'a_max-center?':>14}")
        for b in np.linspace(0.02, 0.96, 25):
            if b > 0.97: continue
            as_ = np.linspace(0.001, 0.999-b, 120)
            Ds = np.array([D_of(make_blocks(mode, R, a, b)) for a in as_])
            imax = np.argmax(Ds)
            a_max = as_[imax]
            center = (1-b)/2
            D_center = np.interp(center, as_, Ds)
            D_bnd = max(Ds[0], Ds[-1])
            print(f"{b:6.3f} {a_max:9.4f} {Ds[imax]:10.5f} {D_center:10.5f} {D_bnd:10.5f} {D_center-D_bnd:+12.5f} {abs(a_max-center)<0.02}")
