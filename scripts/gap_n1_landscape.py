# -*- coding: utf-8 -*-
"""gap_n1_landscape.py: n=1 gap self-consistency landscape for box class [1,R,1] (SUP) and [R,1,R] (INF).
For config with jumps at a, a+b: self-consistency = f(a)=0 and f(a+b)=0 (f = lam1*u1^2 - lam2*u2^2).
Also check gradient of D via FH: dD/da = (R-1)*f(a), dD/dc = -(R-1)*f(1-c).
"""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def get_s_and_f(blocks, x_pts):
    s = lams_fast(blocks, 2)
    lam = s**2
    vals = []
    for x in x_pts:
        u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
        u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
        vals.append(lam[0]*u1**2 - lam[1]*u2**2)
    return s, np.array(vals)

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
    mode = "SUP"
    # coarse grid scan for self-consistent candidates
    N = 60
    aa = np.linspace(0.03, 0.94, N)
    bb = np.linspace(0.03, 0.94, N)
    cands = []
    for a in aa:
        for b in bb:
            if a+b >= 0.985: continue
            bl = make_blocks(mode, R, a, b)
            s, fv = get_s_and_f(bl, [a, a+b])
            resid = abs(fv[0]) + abs(fv[1])
            if resid < 2.0:
                cands.append((a,b,resid,fv[0],fv[1]))
    print(f"mode={mode} R={R}: coarse candidates with resid<2:", len(cands))
    for c in sorted(cands, key=lambda t:t[2])[:15]:
        print(f"  a={c[0]:.4f} b={c[1]:.4f} resid={c[2]:.4f} f(a)={c[3]:+.4f} f(a+b)={c[4]:+.4f}")
