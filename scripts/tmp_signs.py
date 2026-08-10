# -*- coding: utf-8 -*-
"""Minimal fast scan: sign of f(a) and f(a+b) on (a,b) grid."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def f_vals(blocks, xs):
    s = lams_fast(blocks, 2, npts=6000)
    lam = s**2
    out = []
    for x in xs:
        u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
        u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
        out.append(lam[0]*u1**2 - lam[1]*u2**2)
    return np.array(out)

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R={R} : sign(f(a)),sign(f(a+b)) grid ====")
    for b in np.linspace(0.1, 0.9, 9):
        row = []
        for a in np.linspace(0.05, 0.95-b, 12):
            if a+b > 0.99: continue
            fv = f_vals(make_blocks(mode,R,a,b), [a, a+b])
            row.append(f"{'+' if fv[0]>0 else '-'}{'+' if fv[1]>0 else '-'}")
        print(f"  b={b:.2f}: " + " ".join(row))
