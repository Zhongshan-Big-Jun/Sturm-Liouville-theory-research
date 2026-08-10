# -*- coding: utf-8 -*-
"""n2_landscape.py: D(a,b) landscape + 2-block boundary curves + symmetric 1D section."""
import numpy as np
from gap_lib import lams_fast

def s_of(blocks, npts=1200):
    return lams_fast(blocks, 2, npts=npts)

def D_of(blocks, npts=1200):
    s = s_of(blocks, npts)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def D2(blocks_list):
    return D_of(blocks_list)

if __name__ == "__main__":
    R = 4.0
    print("=== 2-block boundary curves, R=4 ===")
    print("t, D([1,R]_t), D([R,1]_t), 3pi^2=29.6088, 3pi^2/R=7.4022")
    for t in np.linspace(0.02, 0.98, 25):
        b1 = [(t,1.0),(1-t,R)]
        b2 = [(t,R),(1-t,1.0)]
        print(f"  {t:.3f}  {D2(b1):.6f}  {D2(b2):.6f}")
    # find max of [1,R] and min of [R,1] by scan
    ts = np.linspace(1e-4, 1-1e-4, 2000)
    v1 = np.array([D2([(t,1.0),(1-t,R)]) for t in ts])
    v2 = np.array([D2([(t,R),(1-t,1.0)]) for t in ts])
    i1 = np.argmax(v1); i2 = np.argmin(v2)
    print(f"  max_t D([1,R]_t) = {v1[i1]:.8f} at t={ts[i1]:.5f}  (vs 3pi^2 = {3*np.pi**2:.6f})")
    print(f"  min_t D([R,1]_t) = {v2[i2]:.8f} at t={ts[i2]:.5f}  (vs 3pi^2/R = {3*np.pi**2/R:.6f})")

    print("=== symmetric family D(u), R=4 ===")
    print("u, D_SUP(u), D_INF(u)")
    for u in np.linspace(0.05, 0.495, 12):
        b_sup = [(u,1.0),(1-2*u,R),(u,1.0)]
        b_inf = [(u,R),(1-2*u,1.0),(u,R)]
        print(f"  {u:.4f}  {D2(b_sup):.8f}  {D2(b_inf):.8f}")

    print("=== D(a,b) landscape near interior, R=4 (SUP) ===")
    print("a,b,D_SUP (only near stationary region)")
    for a in np.linspace(0.30, 0.60, 9):
        row = []
        for b in np.linspace(0.06, 0.40, 9):
            row.append(D2(make_blocks("SUP", R, a, b)))
        print("  a=%.2f:" % a, " ".join(f"{v:8.4f}" for v in row))
