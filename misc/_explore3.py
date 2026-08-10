# -*- coding: utf-8 -*-
import math, numpy as np, sys
sys.path.insert(0, r"F:\LaTeX\BVE research\misc")
from _explore1 import components

best = {"AC": (1e9, None), "BD": (1e9, None), "SUM": (1e9, None)}
n = 0
for q in np.geomspace(1.000001, 1e6, 400):
    for c in np.concatenate([np.linspace(1e-5, 0.49, 150), np.linspace(0.49, 0.5-1e-6, 120)]):
        a1, g, AC, BD, S = components(float(q), float(c))
        n += 1
        if AC < best["AC"][0]: best["AC"] = (AC, (float(q), float(c)))
        if BD < best["BD"][0]: best["BD"] = (BD, (float(q), float(c)))
        if S < best["SUM"][0]: best["SUM"] = (S, (float(q), float(c)))
print("grid points:", n)
for k in ["AC","BD","SUM"]:
    print(k, "min = %.6f at (q,c) = %s" % (best[k][0], best[k][1]))
print("corner limits: AC 2.8061288, BD -0.3877329, SUM 2.4183959")