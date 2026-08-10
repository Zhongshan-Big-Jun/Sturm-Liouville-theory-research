# -*- coding: utf-8 -*-
"""map_r2.py: full zero set of R2(a,b)=0 over a coarse grid; classify v(b) sign.
Uses a fast eigenvalue solver via scipy brentq on sec with adaptive scan."""
import sys, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
from c1_lib import sec, y_at, norm_n, roots2

def r2_fast(a, b, R):
    s1, s2 = roots2(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1 ** 2 * y_at(s1, a, b, R, b) ** 2 / n1 - s2 ** 2 * y_at(s2, a, b, R, b) ** 2 / n2

def v_at(a, b, R, x):
    s1, s2 = roots2(a, b, R)
    return y_at(s2, a, b, R, x) / y_at(s1, a, b, R, x)

# grid scan for R=100: for each a in a grid, find roots of R2 in b
R = 100.0
a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi
rows = []
for a in np.linspace(0.001, 0.99, 40):
    roots = []
    # scan b
    bs = np.linspace(a + 1e-6, 1 - 1e-6, 300)
    vals = np.array([r2_fast(a, bb, R) for bb in bs])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    for i in np.nonzero(ch)[0]:
        bb = brentq(lambda t: r2_fast(a, t, R), bs[i], bs[i+1], xtol=1e-12)
        vb = v_at(a, bb, R, bb - 1e-9)
        roots.append((bb, float(vb)))
    rows.append((a, roots))

for a, roots in rows:
    good = [f"b={r[0]:.4f}(v{'+' if r[1]>0 else '-'}{abs(r[1]):.2f})" for r in roots]
    print(f"a={a:.4f}: {len(roots)} roots: {good}")
