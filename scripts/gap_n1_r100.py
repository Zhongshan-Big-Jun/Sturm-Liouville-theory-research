# -*- coding: utf-8 -*-
"""gap_n1_r100.py: precise symmetric self-consistent roots for R=100 (SUP and INF)."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def f_at(blocks, x):
    s = lams_fast(blocks, 2, npts=120000)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def D_of(blocks):
    s = lams_fast(blocks, 2, npts=120000)
    return s[1]**2 - s[0]**2

for R in (1.5, 2.0, 3.0, 4.0, 10.0, 100.0):
    line = f"R={R:6.1f}:"
    for mode in ("SUP","INF"):
        if mode=="SUP":
            bl = lambda u: [(u,1.0),(1-2*u,R),(u,1.0)]
        else:
            bl = lambda u: [(u,R),(1-2*u,1.0),(u,R)]
        # find root of f(u)=0 in (0, 0.5) by scanning
        us = np.linspace(0.01, 0.49, 200)
        vals = np.array([f_at(bl(u), u) for u in us])
        roots = []
        for i in range(len(us)-1):
            if vals[i]*vals[i+1] < 0:
                roots.append(brentq(lambda u: f_at(bl(u), u), us[i], us[i+1], xtol=1e-13))
        if not roots:
            line += f" {mode}: NO ROOT FOUND"
        else:
            u = roots[0]
            D = D_of(bl(u))
            line += f" {mode}: u={u:.8f} D={D:.8f}"
    print(line)
