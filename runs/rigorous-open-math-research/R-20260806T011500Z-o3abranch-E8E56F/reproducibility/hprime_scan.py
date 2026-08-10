# -*- coding: utf-8 -*-
"""hprime_scan.py: h, h' on the common range across R (lib-based, memoized)."""
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

def h_hp_on_range(R, amin, amax, na=48):
    rows = []
    for a in np.linspace(amin, amax, na):
        g1 = g1_at(a, R); g2 = g2_at(a, R)
        if g1 is None or g2 is None: continue
        A1, B1, C1 = deriv_abc(a, g1, R)
        A2, B2, C2 = deriv_abc(a, g2, R)
        g1p = A1/B1; g2p = -B2/C2
        rows.append((a, g1, g2, g1-g2, g1p, g2p, g1p-g2p))
    return rows

if __name__ == "__main__":
    a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi
    # a_max1(R) table from endpoints3 run (hard-code the computed values)
    amax1 = {1.02:0.422191, 1.05:0.426034, 1.2:0.443781, 1.5:0.473521, 2.0:0.511727,
             3.0:0.564572, 4.0:0.600845, 5.0:0.628047, 10.0:0.706048, 20.0:0.772641, 100.0:0.882408}
    Rs = [float(x) for x in sys.argv[1:]] or [1.05, 2.0, 4.0, 10.0, 100.0]
    for R in Rs:
        if R in amax1:
            cmax = min(amax1[R], b0)
        else:
            cmax = b0  # assume R large enough
        t0 = time.time()
        rows = h_hp_on_range(R, a0+1e-4, cmax-1e-4, na=40)
        if not rows: 
            print(f"R={R}: no rows"); continue
        rows = np.array(rows)
        imin = rows[:,6].argmin()
        print(f"R={R}: min h'={rows[imin,6]:.5f} at a={rows[imin,0]:.5f}; h'(fp-ish) rows: h_L={rows[0,3]:+.5f} h_R={rows[-1,3]:+.5f} t={time.time()-t0:.0f}s")
        # also h' near left/right ends
        print(f"   h'(left)={rows[0,6]:.4f} h'(right)={rows[-1,6]:.4f}")
