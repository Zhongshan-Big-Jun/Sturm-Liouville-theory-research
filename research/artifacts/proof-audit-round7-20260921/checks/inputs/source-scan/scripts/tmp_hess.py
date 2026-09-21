# -*- coding: utf-8 -*-
"""Test Hessian definiteness of D(a,b) on the 3-block family (SUP/INF)."""
import numpy as np
from gap_lib import lams_fast

def D_of(blocks, npts=60000):
    s = lams_fast(blocks, 2, npts=npts)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def hess(mode, R, a, b, h=1e-4, npts=30000):
    D = lambda x,y: D_of(make_blocks(mode,R,x,y), npts=npts)
    f00 = D(a,b)
    fa = D(a+h,b); fb = D(a,b+h); fab = D(a+h,b+h); famb = D(a-h,b+h)
    faa = (D(a+h,b) - 2*f00 + D(a-h,b))/h**2
    fbb = (D(a,b+h) - 2*f00 + D(a,b-h))/h**2
    fab2 = (fab - fa - fb + f00)/h**2
    return np.array([[faa, fab2],[fab2, fbb]])

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R={R}: eigenvalues of Hessian ====")
    worst = (1e9, None)
    for a in np.linspace(0.06, 0.90, 12):
        for b in np.linspace(0.05, 0.90, 12):
            if a+b > 0.96: continue
            H = hess(mode, R, a, b)
            ev = np.linalg.eigvalsh(H)
            if mode=="SUP":
                m = ev.max()
                if m < worst[0]: worst = (m, (a,b))
            else:
                m = ev.min()
                if m > worst[0]: worst = (m, (a,b))
    print(f"  SUP: worst (closest to 0) max-eig = {worst[0]:.4f} at (a,b)={worst[1]}") if mode=="SUP" else None
    print(f"  INF: worst (closest to 0) min-eig = {worst[0]:.4f} at (a,b)={worst[1]}") if mode=="INF" else None
