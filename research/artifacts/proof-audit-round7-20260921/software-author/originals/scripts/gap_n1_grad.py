# -*- coding: utf-8 -*-
"""gap_n1_grad.py: verify FH gradient identity and check suspected saddle region."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def D_of(blocks):
    s = lams_fast(blocks, 2)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def f_vals(blocks, x_pts):
    s = lams_fast(blocks, 2)
    lam = s**2
    out = []
    for x in x_pts:
        u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
        u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
        out.append(lam[0]*u1**2 - lam[1]*u2**2)
    return np.array(out)

def num_grad(mode, R, a, b, h=1e-6):
    bl = make_blocks(mode, R, a, b)
    D0 = D_of(bl)
    bl2 = make_blocks(mode, R, a+h, b)
    Da = D_of(bl2)
    bl3 = make_blocks(mode, R, a, b+h)
    Db = D_of(bl3)
    return (Da-D0)/h, (Db-D0)/h

R = 4.0
# check gradient identity at several points
for mode in ("SUP","INF"):
    print(f"==== {mode} ====")
    for (a,b) in [(0.3,0.4),(0.2,0.3),(0.45,0.10),(0.38,0.23),(0.1,0.1),(0.5,0.2)]:
        bl = make_blocks(mode,R,a,b)
        f = f_vals(bl, [a, a+b])
        gnum = num_grad(mode,R,a,b)
        # FH prediction
        gFH = ((R-1)*(f[1]-f[0]), (R-1)*f[1])
        print(f"  (a,b)=({a},{b}): grad_num=({gnum[0]:+.4f},{gnum[1]:+.4f}) grad_FH=({gFH[0]:+.4f},{gFH[1]:+.4f}) |f(a)|={abs(f[0]):.3e}")
