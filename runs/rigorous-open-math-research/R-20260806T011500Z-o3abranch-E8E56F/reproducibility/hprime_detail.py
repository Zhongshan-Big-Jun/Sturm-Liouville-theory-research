# -*- coding: utf-8 -*-
"""hprime_detail.py: dump g1', g2', h' rows for a given R; and large-R min h' scan."""
import sys, time, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at

def R1(a, b, R):
    if not (1e-7 < a < b < 1-1e-7): return np.nan
    return float(f_at(a, b, R, a, config(a, b, R)))
def R2(a, b, R):
    if not (1e-7 < a < b < 1-1e-7): return np.nan
    return float(f_at(a, b, R, b, config(a, b, R)))
def v_at(a, b, R, x):
    from agentB_lib import y_L
    s = config(a, b, R)[0]
    y = y_L(a, b, R, s, np.array([x]))[:, 0]
    return float(y[1]/y[0])
def root_bisect(fun, a, R, lo, hi, nbr=25, iters=80):
    bb = np.linspace(lo, hi, nbr)
    vals = [fun(a, b, R) for b in bb]
    for i in range(nbr-1):
        v0, v1 = vals[i], vals[i+1]
        if not np.isnan(v0) and not np.isnan(v1) and v0*v1 < 0:
            l, h = bb[i], bb[i+1]
            for _ in range(iters):
                md = 0.5*(l+h)
                if fun(a, md, R)*v0 < 0: h = md
                else: l = md
            return 0.5*(l+h)
    return None
def g1_at(a, R):
    b = root_bisect(R1, a, R, a+1e-6, 1-1e-6)
    if b is not None and v_at(a, b, R, a) > 0: return b
    return None
def g2_at(a, R):
    b = root_bisect(R2, a, R, a+1e-6, 1-1e-6)
    if b is not None and v_at(a, b, R, b) < 0: return b
    return None
def deriv_abc(a, b, R, h=1e-5):
    A = (R1(a+h,b,R)-R1(a-h,b,R))/(2*h)
    B = (R2(a+h,b,R)-R2(a-h,b,R))/(2*h)
    C = (R2(a,b+h,R)-R2(a,b-h,R))/(2*h)
    return A, B, C

if __name__ == "__main__":
    a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi
    mode = sys.argv[1]
    if mode == "detail":
        R = float(sys.argv[2])
        print(f"R={R}: a, g1, g2, h, g1', g2', h'")
        for a in np.linspace(a0+1e-3, b0-1e-3, 24):
            g1 = g1_at(a, R); g2 = g2_at(a, R)
            if g1 is None or g2 is None: continue
            A1, B1, C1 = deriv_abc(a, g1, R)
            A2, B2, C2 = deriv_abc(a, g2, R)
            g1p = A1/B1; g2p = -B2/C2
            print(f"{a:.5f} {g1:.6f} {g2:.6f} {g1-g2:+.5f} {g1p:+.4f} {g2p:+.4f} {g1p-g2p:+.4f}")
    elif mode == "min":
        for R in [float(x) for x in sys.argv[2:]]:
            na = 14
            rows = []
            for a in np.linspace(a0+1e-3, b0-1e-3, na):
                g1 = g1_at(a, R); g2 = g2_at(a, R)
                if g1 is None or g2 is None: continue
                A1, B1, C1 = deriv_abc(a, g1, R)
                A2, B2, C2 = deriv_abc(a, g2, R)
                rows.append((a, A1/B1, -B2/C2, A1/B1 + B2/C2))
            rows = np.array(rows)
            imin = rows[:,3].argmin()
            print(f"R={R}: min h'={rows[imin,3]:.6f} at a={rows[imin,0]:.5f} (g1'={rows[imin,1]:.4f}, g2'={rows[imin,2]:.4f})")
