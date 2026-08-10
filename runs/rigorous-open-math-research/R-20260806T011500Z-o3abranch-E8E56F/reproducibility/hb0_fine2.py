# -*- coding: utf-8 -*-
"""hb0_fine2.py: h(b0) at very large R with guarded config."""
import sys, numpy as np, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at
from scipy.optimize import brentq

def R1(a, b, R):
    try:
        return float(np.ravel(f_at(a, b, R, a, config(a, b, R)))[0])
    except Exception:
        return np.nan
def v_at(a, b, R, x):
    try:
        from agentB_lib import y_L
        s = config(a, b, R)[0]
        y = y_L(a, b, R, s, np.array([x]))[:, 0]
        return float(y[1]/y[0])
    except Exception:
        return np.nan

def g1_at(a, R, bw=0.02, nb=150):
    bb = np.linspace(a+1e-6, a+bw, nb)
    vals = [R1(a, b, R) for b in bb]
    for i in range(len(bb)-1):
        v0, v1 = vals[i], vals[i+1]
        if np.isfinite(v0) and np.isfinite(v1) and v0*v1 < 0:
            try:
                b0 = brentq(lambda b: R1(a, b, R), bb[i], bb[i+1], xtol=1e-12)
            except Exception:
                continue
            if v_at(a, b0, R, a) > 0:
                return b0
    return None

b0v = np.arccos(-0.25)/np.pi
print("=== h(b0), guarded fine scan ===")
out = {}
for R in [1e5, 3e5, 1e6, 3e6, 1e7]:
    g1 = g1_at(b0v-1e-7, R)
    if g1:
        h = g1 - b0v
        out[str(int(R))] = dict(g1=g1, h=h, h_sqrtR=h*np.sqrt(R))
        print(f"  R={R:.0e}: h(b0)={h:+.6e}  h*sqrt(R)={h*np.sqrt(R):.4f}")
    else:
        print(f"  R={R:.0e}: not found")
json.dump(out, open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\hb0_fine2.json","w"), indent=1)
