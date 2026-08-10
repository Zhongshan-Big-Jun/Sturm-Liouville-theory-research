# -*- coding: utf-8 -*-
"""Fast curve scan for self-consistency (SUP/INF)."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def f_at(blocks, x):
    s = lams_fast(blocks, 2, npts=15000)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R={R} ====")
    print("  b :  a-roots f(a)=0   vs   a-roots f(a+b)=0")
    for b in np.linspace(0.06, 0.92, 12):
        aa = np.linspace(0.005, 0.995-b, 50)
        rootsL, rootsR = [], []
        for i in range(len(aa)-1):
            a0, a1 = aa[i], aa[i+1]
            try:
                fl0 = f_at(make_blocks(mode,R,a0,b), a0); fl1 = f_at(make_blocks(mode,R,a1,b), a1)
            except Exception:
                continue
            if fl0*fl1 < 0:
                # bisection
                lo, hi = a0, a1
                for _ in range(30):
                    mid = 0.5*(lo+hi)
                    if f_at(make_blocks(mode,R,mid,b), mid)*fl0 < 0: hi = mid
                    else: lo = mid
                rootsL.append(0.5*(lo+hi))
            try:
                fr0 = f_at(make_blocks(mode,R,a0,b), a0+b); fr1 = f_at(make_blocks(mode,R,a1,b), a1+b)
            except Exception:
                continue
            if fr0*fr1 < 0:
                lo, hi = a0, a1
                for _ in range(30):
                    mid = 0.5*(lo+hi)
                    if f_at(make_blocks(mode,R,mid,b), mid+b)*fr0 < 0: hi = mid
                    else: lo = mid
                rootsR.append(0.5*(lo+hi))
        sL = ",".join(f"{r:.3f}" for r in rootsL)
        sR = ",".join(f"{r:.3f}" for r in rootsR)
        print(f"  {b:.3f}: [{sL}]  vs  [{sR}]")
