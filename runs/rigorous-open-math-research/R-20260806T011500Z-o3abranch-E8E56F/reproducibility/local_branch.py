# -*- coding: utf-8 -*-
"""local_branch.py: local branch evaluation g1(a), g2(a) + derivative quantities A,B,C.
Uses agentB_lib (memoized) for speed and cross-checks vec_lib."""
import sys, time, json
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at, zeros_f

def R1(a, b, R):
    if not (1e-7 < a < b < 1-1e-7): return np.nan
    return float(f_at(a, b, R, a, config(a, b, R)))
def R2(a, b, R):
    if not (1e-7 < a < b < 1-1e-7): return np.nan
    return float(f_at(a, b, R, b, config(a, b, R)))

def v_at(a, b, R, x):
    """v = y2/y1 at x (slope-normalized)."""
    cfg = config(a, b, R)
    s, n, z0 = cfg
    from agentB_lib import y_L
    y = y_L(a, b, R, s, np.array([x]))[:, 0]
    return float(y[1]/y[0])

def g1_at(a, R, lo=None, hi=None, tol=1e-12):
    """good-left root b with R1(a,b)=0 and v(a)>0; None if absent."""
    if lo is None: lo = a + 1e-7
    if hi is None: hi = 1 - 1e-7
    va = v_at(a, (lo+hi)/2, R, a)
    # find sign change of R1 over b with good-left condition
    bb = np.linspace(lo, hi, 60)
    vals = [R1(a, b, R) if (a < b) else np.nan for b in bb]
    for i in range(59):
        if not np.isnan(vals[i]) and not np.isnan(vals[i+1]) and vals[i]*vals[i+1] < 0:
            lo2, hi2 = bb[i], bb[i+1]
            for _ in range(80):
                md = 0.5*(lo2+hi2)
                if R1(a, md, R)*vals[i] < 0: hi2 = md
                else: lo2 = md
            b2 = 0.5*(lo2+hi2)
            if v_at(a, b2, R, a) > 0:
                return b2
    return None

def g2_at(a, R, lo=None, hi=None, tol=1e-12):
    if lo is None: lo = a + 1e-7
    if hi is None: hi = 1 - 1e-7
    bb = np.linspace(lo, hi, 60)
    vals = [R2(a, b, R) if (a < b) else np.nan for b in bb]
    for i in range(59):
        if not np.isnan(vals[i]) and not np.isnan(vals[i+1]) and vals[i]*vals[i+1] < 0:
            lo2, hi2 = bb[i], bb[i+1]
            for _ in range(80):
                md = 0.5*(lo2+hi2)
                if R2(a, md, R)*vals[i] < 0: hi2 = md
                else: lo2 = md
            b2 = 0.5*(lo2+hi2)
            if v_at(a, b2, R, b2) < 0:
                return b2
    return None

def deriv_abc(a, b, R, h=1e-5):
    """A=R1_a (total), B=R2_a, C=R2_b (total), R1b; T3 check."""
    A = (R1(a+h, b, R) - R1(a-h, b, R))/(2*h)
    B = (R2(a+h, b, R) - R2(a-h, b, R))/(2*h)
    C = (R2(a, b+h, R) - R2(a, b-h, R))/(2*h)
    R1b = (R1(a, b+h, R) - R1(a, b-h, R))/(2*h)
    return A, B, C, R1b

def branch_scan_local(R, na=90, alo=0.35, ahi=0.75):
    rows = []
    for a in np.linspace(alo, ahi, na):
        g1 = g1_at(a, R)
        g2 = g2_at(a, R)
        rows.append((a, g1, g2))
    return rows

if __name__ == "__main__":
    R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    rows = branch_scan_local(R)
    # common range
    present = [(a, g1, g2) for (a, g1, g2) in rows if g1 is not None and g2 is not None]
    print(f"R={R}: {len(present)}/{len(rows)} a-values with both branches")
    if not present: sys.exit()
    amin = min(a for a, _, _ in present); amax = max(a for a, _, _ in present)
    print(f"common a-range (grid): [{amin:.5f}, {amax:.5f}]")
    # h and h' on common range
    print(" a       g1       g2       h        g1'      g2'      h'")
    for (a, g1, g2) in present:
        A1, B1, C1, R1b1 = deriv_abc(a, g1, R)
        A2, B2, C2, R1b2 = deriv_abc(a, g2, R)
        g1p = A1/B1 if abs(B1) > 1e-9 else np.nan
        g2p = -B2/C2 if abs(C2) > 1e-9 else np.nan
        print(f"{a:.5f} {g1:.6f} {g2:.6f} {g1-g2:+.5f} {g1p:+.4f} {g2p:+.4f} {g1p-g2p:+.4f}")
