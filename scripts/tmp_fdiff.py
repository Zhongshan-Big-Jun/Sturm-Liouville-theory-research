# -*- coding: utf-8 -*-
"""Test lemma candidate: for a < c (left-biased), is f(a+b) > f(a) for 3-block (SUP and INF)?"""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=1200):
    return lams_fast(blocks, 2, npts=npts)

def f_at(blocks, x, s=None, npts=1200):
    if s is None:
        s = s_of(blocks, npts)
    lam = s**2
    x = np.atleast_1d(np.asarray(x, dtype=float))
    x = np.clip(x, 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], x)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], x)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

print("Test: sign of (f(a+b)-f(a)) for a < c  (want > 0)")
print("Also report where it fails and by how much.")
for R in (2.0, 4.0, 10.0):
    for mode in ("SUP","INF"):
        worst = (1e9, None)
        fails = 0; tot = 0
        for a in np.linspace(0.02, 0.48, 15):
            for b in np.linspace(0.02, 0.94, 15):
                c = 1-a-b
                if not (a > 0.01 and b > 0.01 and c > a + 1e-9): continue
                bl = make_blocks(mode, R, a, b)
                fv, s = f_at(bl, [a, a+b])
                tot += 1
                diff = fv[1]-fv[0]
                if diff < 0:
                    fails += 1
                    if diff < worst[0]: worst = (diff, (a,b,c))
        print(f"R={R:5.1f} {mode}: fails={fails}/{tot}  worst diff={worst[0]:.4f} at {worst[1]}")
