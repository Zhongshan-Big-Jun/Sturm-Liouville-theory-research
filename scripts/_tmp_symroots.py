# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def f_at_u(blocks, x):
    s = lams_fast(blocks, 3)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def D_of(blocks):
    s = lams_fast(blocks, 3)
    return s[1]**2 - s[0]**2

def sym_roots(R, mode):
    f = lambda u: f_at_u([(u,1.0),(1-2*u,R),(u,1.0)] if mode=="SUP" else [(u,R),(1-2*u,1.0),(u,R)], u)
    # scan sign changes
    us = np.linspace(0.02, 0.48, 500)
    vals = np.array([f(u) for u in us])
    roots = []
    for i in range(len(us)-1):
        if vals[i]*vals[i+1] < 0:
            roots.append(brentq(f, us[i], us[i+1], xtol=1e-14))
    return roots

for R in (1.5, 2.0, 3.0, 4.0, 10.0, 100.0):
    line = f"R={R}"
    for mode in ("SUP","INF"):
        roots = sym_roots(R, mode)
        for u in roots:
            bl = [(u,1.0),(1-2*u,R),(u,1.0)] if mode=="SUP" else [(u,R),(1-2*u,1.0),(u,R)]
            D = D_of(bl)
            line += f" | {mode}: u={u:.6f} D={D:.6f}"
    print(line)
