# -*- coding: utf-8 -*-
import math, numpy as np
from _explore1 import components, solve_phases  # reuse? simpler to reimport via path
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\misc")
from _explore1 import components

qs = [1.0001, 1.001, 1.01, 1.02, 1.05, 1.1, 1.2, 1.5, 2, 3, 4, 7, 10, 30, 100, 1e3, 1e4, 1e5, 1e6]
cs = np.linspace(1e-4, 0.5-1e-5, 60)
best = {"AC": (1e9, None), "BD": (1e9, None), "SUM": (1e9, None), "G2mG1_via_sum_neg": 0}
w = []
for q in qs:
    for c in cs:
        a1, g, AC, BD, S = components(q, float(c))
        if AC < best["AC"][0]: best["AC"] = (AC, (q, float(c)))
        if BD < best["BD"][0]: best["BD"] = (BD, (q, float(c)))
        if S < best["SUM"][0]: best["SUM"] = (S, (q, float(c)))
for k in ["AC","BD","SUM"]:
    print(k, "min = %.6f at (q, c) = %s" % (best[k][0], best[k][1]))
print("corner: 2.80613 / -0.38773 / 2.41840")
# check separate lower bounds
print("AC >= 2.80613 ?", all(components(q, float(c))[2] >= 2.80612 for q in qs for c in cs))
print("BD >= -0.38773 ?", all(components(q, float(c))[3] >= -0.38772 for q in qs for c in cs))