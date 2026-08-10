# -*- coding: utf-8 -*-
"""endpoint_asym.py: h(a0), h(b0), G(a0) at large R from tracew data; fit asymptotics."""
import json, numpy as np, os
HERE = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260807T163000Z-c1center-9C4E2A\reproducibility"
data = {}
for R in [1000.0, 5000.0, 10000.0, 100000.0, 1000000.0]:
    p = os.path.join(HERE, "tracew_%g.json" % R)
    if os.path.exists(p):
        data[R] = json.load(open(p, encoding="utf-8"))
print("R        h(a0)        h(b0)       G(a0)      G(b0)      sqrtR*h(a0)  sqrtR*h(b0)")
for R in sorted(data):
    rows = data[R]["rows"]
    valid = [r for r in rows if np.isfinite(r[7])]
    h0, h1 = valid[0][6], valid[-1][6]
    G0, G1 = valid[0][2], valid[-1][2]
    s = np.sqrt(R)
    print("%-7.0f %12.6e %12.6e %10.6f %10.6f %12.5f %12.5f" % (R, h0, h1, G0, G1, s*h0, s*h1))
