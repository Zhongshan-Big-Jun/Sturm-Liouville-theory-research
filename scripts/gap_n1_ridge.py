# -*- coding: utf-8 -*-
"""gap_n1_ridge.py: trace the ridge f(a)=f(a+b) and check D along it."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def D_of(blocks):
    s = lams_fast(blocks, 2)
    return s[1]**2 - s[0]**2

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

R = 4.0; mode = "SUP"
print("Ridge scan: for each b, find a with f(a)=f(a+b) (dD/da=0).")
best = (0, None)
for b in np.linspace(0.02, 0.94, 46):
    # scan a in (0, 1-b)
    aa = np.linspace(0.001, 0.999-b, 80)
    vals = []
    for a in aa:
        bl = make_blocks(mode,R,a,b)
        vals.append(f_at(bl, a) - f_at(bl, a+b))
    vals = np.array(vals)
    roots = []
    for i in range(len(aa)-1):
        if vals[i]*vals[i+1] < 0:
            r = brentq(lambda a: f_at(make_blocks(mode,R,a,b), a) - f_at(make_blocks(mode,R,a,b), a+b), aa[i], aa[i+1], xtol=1e-12)
            roots.append(r)
    for a in roots:
        bl = make_blocks(mode,R,a,b)
        D = D_of(bl)
        sym = abs(a - (1-b)/2) < 1e-6
        if D > best[0]: best = (D, (a,b))
        print(f"  b={b:.3f}: ridge a={a:.6f} c={1-a-b:.6f} D={D:.8f} {'[SYMMETRIC]' if sym else ''}")
print("BEST:", best)
