# -*- coding: utf-8 -*-
"""Examine the self-consistency curves f(a)=0 and f(a+b)=0 for SUP and INF."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def f_at(blocks, x):
    s = lams_fast(blocks, 2, npts=120000)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def T_ratio(blocks):
    """T2/T1 = |u2'(1)/u2'(0)| / |u1'(1)/u1'(0)| via finite diff of y_at."""
    s = lams_fast(blocks, 2, npts=120000)
    h = 1e-7
    out = []
    for si in s:
        y0 = y_at(blocks, si, np.array([0.0, h]))[0]
        y1 = y_at(blocks, si, np.array([1.0-h, 1.0]))[1]
        sl0 = y_at(blocks, si, np.array([0.0, h]))[1]/h   # y'(0) ~ y(h)/h
        sl1 = (y_at(blocks, si, np.array([1.0-h, 1.0]))[1] - y_at(blocks, si, np.array([1.0-h, 1.0]))[0])/h * (-1)
        # simpler: y(1-h) ~ -y'(1)*h => y'(1) ~ -y(1-h)/h
        sl1 = -y_at(blocks, si, np.array([1.0-h]))[0]/h
        out.append(abs(sl1/sl0))
    return out[1]/out[0]

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R={R} ====")
    print("  b :  a-roots of f(a)=0            a-roots of f(a+b)=0")
    for b in np.linspace(0.05, 0.93, 20):
        aa = np.linspace(0.001, 0.999-b, 150)
        fL = np.array([f_at(make_blocks(mode,R,a,b), a) for a in aa])
        fR = np.array([f_at(make_blocks(mode,R,a,b), a+b) for a in aa])
        rootsL, rootsR = [], []
        for i in range(len(aa)-1):
            if fL[i]*fL[i+1] < 0:
                rootsL.append(brentq(lambda a: f_at(make_blocks(mode,R,a,b), a), aa[i], aa[i+1], xtol=1e-10))
            if fR[i]*fR[i+1] < 0:
                rootsR.append(brentq(lambda a: f_at(make_blocks(mode,R,a,b), a+b), aa[i], aa[i+1], xtol=1e-10))
        sL = ",".join(f"{r:.3f}" for r in rootsL)
        sR = ",".join(f"{r:.3f}" for r in rootsR)
        print(f"  {b:.3f}: [{sL}]  vs  [{sR}]")
