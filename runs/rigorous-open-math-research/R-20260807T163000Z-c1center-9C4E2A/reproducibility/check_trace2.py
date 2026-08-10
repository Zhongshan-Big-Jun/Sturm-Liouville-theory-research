# -*- coding: utf-8 -*-
import json, numpy as np, os
HERE = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260807T163000Z-c1center-9C4E2A\reproducibility"
d = json.load(open(os.path.join(HERE, "trace2_1e+06.json"), encoding="utf-8"))
rows = d["rows"]
print("fp=", d["fp"], " nrows=", len(rows))
for a0 in [0.42, 0.44, 0.46, 0.48, 0.49, 0.50, 0.51, 0.53, 0.55, 0.57]:
    idx = np.argsort(np.abs(np.array([r[0] for r in rows]) - a0))[:3]
    for i in idx:
        r = rows[i]
        print("  a=%.6f b=%.8f G=%.6f u=%.6f Gu=%.6f Phi=%.6f h=%.8f hp=%.6f" % tuple(r))
