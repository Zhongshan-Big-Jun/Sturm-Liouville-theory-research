# -*- coding: utf-8 -*-
"""Trace main-sheet Gamma_1 from the symmetric fp at R=4 (evidence only)."""
import numpy as np
src = open(r"F:\LaTeX\BVE research\scripts\explore_e1.py", encoding="utf-8").read()
exec(src.split('a0 = np.arccos')[0])
a0 = np.arccos(0.25)/np.pi; b0 = 1-a0
R = 4.0

def fp(R, lo=0.40, hi=0.5):
    for _ in range(80):
        m = 0.5*(lo+hi)
        R1,_ = residual_both(m, 1-m, R)
        R1l,_ = residual_both(lo, 1-lo, R)
        if np.signbit(R1) == np.signbit(R1l): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def find_b(a, b_guess, R):
    """solve R1(a,b)=0 with a=x_- near b_guess via Newton on R1."""
    b = b_guess
    for _ in range(60):
        R1,_ = residual_both(a, b, R)
        # numerical dR1/db
        h = 1e-6
        R1p,_ = residual_both(a, b+h, R)
        R1m,_ = residual_both(a, b-h, R)
        db = -R1/((R1p-R1m)/(2*h))
        b += db
        if abs(db) < 1e-12: break
    return b

af = fp(R); bf = 1-af
print(f"fp = ({af:.6f}, {bf:.6f})")
# trace forward in a
a = af; b = bf
print("forward trace:")
for step in range(12):
    a_new = a + 0.012
    if a_new >= 0.995: break
    b_new = find_b(a_new, b + (b - (bf)) * 0.012/(af - a0) if False else b, R)
    # better guess: linear extrapolation
    R1,_ = residual_both(a_new, b_new, R)
    xm, xp = band(a_new, b_new, R)
    sc = "x-" if (xm==xm and abs(a_new-xm) < 2e-3) else ("x+" if (xp==xp and abs(a_new-xp) < 2e-3) else "?")
    print(f"  a={a_new:.5f}: b={b_new:.5f} R1={R1:+.2e} sheet={sc}")
    a, b = a_new, b_new