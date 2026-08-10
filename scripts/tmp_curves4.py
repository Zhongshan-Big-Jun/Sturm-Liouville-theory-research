# -*- coding: utf-8 -*-
"""Efficient curve tracing for C1: f(a;a,b)=0 and C2: f(a+b;a,b)=0."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def f2(blocks, x1, x2):
    s = lams_fast(blocks, 2, npts=8000)
    lam = s**2
    u1a = y_at(blocks, s[0], np.array([x1]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2a = y_at(blocks, s[1], np.array([x1]))[0]/np.sqrt(norm2(blocks, s[1]))
    u1b = y_at(blocks, s[0], np.array([x2]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2b = y_at(blocks, s[1], np.array([x2]))[0]/np.sqrt(norm2(blocks, s[1]))
    return (lam[0]*u1a**2-lam[1]*u2a**2, lam[0]*u1b**2-lam[1]*u2b**2)

def bisect(mode, R, which, a0, a1, b, fa0, fa1):
    lo, hi = a0, a1
    flo = fa0
    for _ in range(40):
        mid = 0.5*(lo+hi)
        bl = make_blocks(mode,R,mid,b)
        if which==1: fm = f2(bl, mid, mid+b)[0]
        else:        fm = f2(bl, mid, mid+b)[1]
        if flo*fm < 0: hi = mid
        else: lo, flo = mid, fm
    return 0.5*(lo+hi)

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R={R}: roots of C1: f(a)=0 | C2: f(a+b)=0 ====")
    for b in np.linspace(0.05, 0.90, 14):
        aa = np.linspace(0.01, 0.99-b, 60)
        rows = np.array([f2(make_blocks(mode,R,a,b), a, a+b) for a in aa])
        c1, c2 = [], []
        for i in range(len(aa)-1):
            if rows[i,0]*rows[i+1,0] < 0: c1.append(bisect(mode,R,1,aa[i],aa[i+1],b,rows[i,0],rows[i+1,0]))
            if rows[i,1]*rows[i+1,1] < 0: c2.append(bisect(mode,R,2,aa[i],aa[i+1],b,rows[i,1],rows[i+1,1]))
        s1 = ",".join(f"{r:.3f}" for r in c1)
        s2 = ",".join(f"{r:.3f}" for r in c2)
        print(f"  b={b:.3f}: C1=[{s1}]  C2=[{s2}]")
