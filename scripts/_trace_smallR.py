# -*- coding: utf-8 -*-
"""Small-R trace v2: main-sheet Gamma_1 from fp, find branch end (evidence only)."""
import numpy as np
src = open(r"F:\LaTeX\BVE research\scripts\explore_e1.py", encoding="utf-8").read()
exec(src.split('a0 = np.arccos')[0])
a0 = np.arccos(0.25)/np.pi; b0 = 1-a0

def fp(R, lo, hi):
    for _ in range(80):
        m = 0.5*(lo+hi)
        R1,_ = residual_both(m, 1-m, R)
        R1l,_ = residual_both(lo, 1-lo, R)
        if np.signbit(R1) == np.signbit(R1l): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def find_b(a, b_guess, R):
    b = b_guess
    for _ in range(40):
        R1,_ = residual_both(a, b, R)
        h = 1e-6
        R1p,_ = residual_both(a, b+h, R); R1m,_ = residual_both(a, b-h, R)
        db = -R1/((R1p-R1m)/(2*h))
        b += db
        if abs(db) < 1e-12: break
    return b

for R in [1.02, 1.05, 1.1, 1.2, 1.5, 2.0, 3.0, 4.0]:
    af = fp(R, (a0 if R<2 else 0.40), (0.44 if R<2 else 0.5))
    bf = 1-af
    a, b = af, bf
    amax, bmax = af, bf
    reason = "grid-end"
    for step in range(300):
        a_new = a + 0.0015
        if a_new >= 0.999:
            break
        b_new = find_b(a_new, b, R)
        xm, xp = band(a_new, b_new, R)
        if xm != xm or abs(a_new-xm) > 2e-3:
            reason = "no-xminus-root"; break
        if b_new > 1-1e-5:
            reason = "b~1"; break
        a, b = a_new, b_new
        amax, bmax = a, b
    print(f"R={R:g}: fp={af:.6f} a_max1={amax:.6f} b_end={bmax:.6f} b0={b0:.6f} beta={min(amax,b0):.6f} end={reason}")