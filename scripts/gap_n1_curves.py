# -*- coding: utf-8 -*-
"""gap_n1_curves.py: trace curves f(a)=0 and f(a+b)=0 in (a,b) plane."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def f_at(blocks, x):
    s = lams_fast(blocks, 2)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

R = 4.0
mode = "SUP"
# For each b, find roots of f(a)=0 and f(a+b)=0 in a.
print("SUP R=4: roots of f(a)=0 (left) and f(a+b)=0 (right) vs b")
for b in np.linspace(0.05, 0.93, 18):
    aa = np.linspace(0.001, 0.999-b, 120)
    fL = np.array([f_at(make_blocks(mode,R,a,b), a) for a in aa])
    fR = np.array([f_at(make_blocks(mode,R,a,b), a+b) for a in aa])
    rootsL, rootsR = [], []
    for i in range(len(aa)-1):
        if fL[i]*fL[i+1] < 0:
            rootsL.append(brentq(lambda a: f_at(make_blocks(mode,R,a,b), a), aa[i], aa[i+1], xtol=1e-11))
        if fR[i]*fR[i+1] < 0:
            rootsR.append(brentq(lambda a: f_at(make_blocks(mode,R,a,b), a+b), aa[i], aa[i+1], xtol=1e-11))
    sL = ",".join(f"{r:.3f}" for r in rootsL)
    sR = ",".join(f"{r:.3f}" for r in rootsR)
    print(f"  b={b:.3f}: f(a)=0 at a in [{sL}]   f(a+b)=0 at a in [{sR}]")
