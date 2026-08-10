# -*- coding: utf-8 -*-
import math, numpy as np, sys
sys.path.insert(0, r"F:\LaTeX\BVE research\misc")
from _explore1 import components

def BD(q, c):
    return components(q, c)[3]

# 1) zero set of B-D: for each q, find c where BD crosses 0 (if negative region exists)
print("B-D zero crossing (c where BD=0), if any:")
for q in [1.001, 1.01, 1.05, 1.1, 1.5, 2, 4, 10, 100, 1e4]:
    cs = np.linspace(1e-4, 0.5-1e-6, 2000)
    vals = np.array([BD(q, c) for c in cs])
    neg = np.nonzero(vals < 0)[0]
    if len(neg) == 0:
        print("q=%.0e: B-D >= 0 for all c" % q)
    else:
        # crossing from + to -
        c0 = None
        for i in range(len(vals)-1):
            if vals[i] >= 0 and vals[i+1] < 0:
                c0 = cs[i]; break
        print("q=%.0e: B-D<0 for c in (%.4f, 0.5)" % (q, c0))
# 2) where is d(BD)/dq < 0 ?
print("d(BD)/dq < 0 region (c, q) samples:")
for c in [0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.48]:
    for q in [1.05, 1.5, 10, 1e3, 1e5]:
        h = 1e-4*max(1.0, q)
        d = (BD(q+h, c)-BD(q, c))/h
        if d < -1e-6:
            print("  d(BD)/dq<0 at c=%.3f q=%.0e: %.3e" % (c, q, d))
print("done")