# -*- coding: utf-8 -*-
"""threshold.py: find R* where h'(0.57364) crosses zero; also direct 2-param scan R=1e4."""
import sys, numpy as np, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at
from scipy.optimize import brentq

def R1(a, b, R):
    return float(np.ravel(f_at(a, b, R, a, config(a, b, R)))[0])
def R2(a, b, R):
    return float(np.ravel(f_at(a, b, R, b, config(a, b, R)))[0])
def v_at(a, b, R, x):
    from agentB_lib import y_L
    s = config(a, b, R)[0]
    y = y_L(a, b, R, s, np.array([x]))[:, 0]
    return float(y[1]/y[0])

def branch(a, R, which, lo=None, hi=None):
    f = (lambda b: R1(a, b, R)) if which=='g1' else (lambda b: R2(a, b, R))
    if lo is not None and hi is not None and lo > a:
        try:
            b0 = brentq(f, lo, hi, xtol=1e-12)
            c = v_at(a, b0, R, a) if which=='g1' else v_at(a, b0, R, b0)
            if (which=='g1' and c > 0) or (which=='g2' and c < 0): return b0
        except Exception: pass
    bb = np.linspace(a+1e-5, 1-1e-5, 40)
    vals = [f(b) for b in bb]
    for i in range(len(bb)-1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i+1]) and vals[i]*vals[i+1] < 0:
            try: b0 = brentq(f, bb[i], bb[i+1], xtol=1e-12)
            except Exception: continue
            c = v_at(a, b0, R, a) if which=='g1' else v_at(a, b0, R, b0)
            if (which=='g1' and c > 0) or (which=='g2' and c < 0): return b0
    return None

print("=== h'(0.57364) vs R (threshold search) ===")
a = 0.57364; ha = 1e-4
for R in [1200.0, 1500.0, 2000.0, 3000.0, 5000.0, 7000.0]:
    g1p = (branch(a+ha,R,'g1') - branch(a-ha,R,'g1'))/(2*ha)
    g2p = (branch(a+ha,R,'g2') - branch(a-ha,R,'g2'))/(2*ha)
    print(f"  R={R:.0f}: g1'={g1p:+.5f} g2'={g2p:+.5f} h'={g1p-g2p:+.5f}")
