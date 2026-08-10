# -*- coding: utf-8 -*-
import math, numpy as np, sys
sys.path.insert(0, r"F:\LaTeX\BVE research\misc")
from _explore1 import components

def dq_components(q, c, h=1e-5):
    a1, g, AC, BD, S = components(q, c)
    a1b, gb, ACb, BDb, Sb = components(q+h, c)
    return (ACb-AC)/h, (BDb-BD)/h, (Sb-S)/h

# where is d(BD)/dq < 0 ?  (failure region of B-D q-monotonicity)
print("scan d(BD)/dq < 0 region:")
for c in [0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.48, 0.495]:
    row = []
    for q in [1.01, 1.1, 1.5, 2, 4, 10, 100, 1e3, 1e4, 1e5]:
        dAC, dBD, dS = dq_components(q, c)
        row.append("%+.1e" % dBD)
    print("c=%.2f: dBD/dq: %s" % (c, " ".join(row)))