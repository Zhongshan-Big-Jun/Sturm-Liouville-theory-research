# -*- coding: utf-8 -*-
"""crosscheck_hp.py: independent check using prior-run agentB_lib solver."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at, z0_of

def R1(a, b, R):
    return float(f_at(a, b, R, a, config(a, b, R)))
def R2(a, b, R):
    return float(f_at(a, b, R, b, config(a, b, R)))

def v_at(a, b, R, x):
    from agentB_lib import y_L
    s = config(a, b, R)[0]
    y = y_L(a, b, R, s, np.array([x]))[:, 0]
    return float(y[1]/y[0])

def branch(a, R, which):
    from scipy.optimize import brentq
    bb = np.linspace(a+1e-5, 1-1e-5, 50)
    f = (lambda b: R1(a, b, R)) if which=='g1' else (lambda b: R2(a, b, R))
    vals = [f(b) for b in bb]
    for i in range(len(bb)-1):
        if vals[i]*vals[i+1] < 0:
            try:
                b0 = brentq(f, bb[i], bb[i+1], xtol=1e-12)
            except Exception:
                continue
            if which=='g1' and v_at(a, b0, R, a) > 0: return b0
            if which=='g2' and v_at(a, b0, R, b0) < 0: return b0
    return None

for R in [1000.0, 10000.0, 100000.0]:
    a = 0.57364
    g1 = branch(a, R, 'g1'); g2 = branch(a, R, 'g2')
    print(f"R={R}: g1={g1} g2={g2} h={g1-g2 if g1 and g2 else None}")
    if g1 and g2:
        h = 1e-5
        g1p = (branch(a+h, R, 'g1') - branch(a-h, R, 'g1'))/(2*h)
        g2p = (branch(a+h, R, 'g2') - branch(a-h, R, 'g2'))/(2*h)
        print(f"   g1'={g1p:+.6f} g2'={g2p:+.6f} h'={g1p-g2p:+.6f}  (agentB_lib cross-check)")
