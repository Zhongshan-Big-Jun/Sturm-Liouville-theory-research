# -*- coding: utf-8 -*-
"""Subclaim 2: verify first-order constant c and R->inf limits.
Half-problem solver (DN/DD roots on [0,1/2]) imported from agentC_sub2c.py
(grid-based first-root finding; robust at extreme R)."""
import numpy as np
from agentC_sub2c import roots_half as _roots_half, ustar as _ustar

def roots_half(u, c1, c2):
    s0, s1 = _roots_half(np.array([u]), c1, c2)
    return float(s0[0]), float(s1[0])

def ustar(R, sup, npts=300):
    return _ustar(R, sup, npts)[0]


# first-order constant
u0 = np.arccos(0.25)/np.pi
I = (3/2)*u0 + 9*np.sqrt(15)/(64*np.pi) - 3/4
c_theory = 4*np.pi**2*I
print(f"u0 = {u0:.10f}, I = {I:.10f}, c_theory = {c_theory:.10f}")

print("\nR -> 1+ : (D_SUP-3pi^2)/eps and (3pi^2/R - D_INF)/eps should -> c_theory")
for eps in [0.02, 0.005, 0.001, 0.0002]:
    R = 1+eps
    zs = ustar(R, True); us = zs[0]
    s0, s1 = roots_half(us, 1.0, R)
    Dsup = s1**2 - s0**2
    zt = ustar(R, False); ui = zt[0]
    t0, t1 = roots_half(ui, R, 1.0)
    Dinf = t1**2 - t0**2
    print(f"  eps={eps:9.5f}: SUP (D-3pi^2)/eps = {(Dsup-3*np.pi**2)/eps:.6f}   INF (3pi^2/R-D)/eps = {(3*np.pi**2/R - Dinf)/eps:.6f}")

print("\nR -> inf: D_SUP -> 4 pi^2 =", 4*np.pi**2, "; D_INF*R -> 24.943866...")
for R in [1e2, 1e4, 1e6]:
    zs = ustar(R, True); us = zs[0]
    s0, s1 = roots_half(us, 1.0, R)
    Dsup = s1**2 - s0**2
    zt = ustar(R, False); ui = zt[0]
    t0, t1 = roots_half(ui, R, 1.0)
    Dinf = t1**2 - t0**2
    print(f"  R={R:8.0f}: SUP u*={us:.7f} D_SUP={Dsup:.7f} (4pi^2-D={4*np.pi**2-Dsup:+.3e}) | INF u*={ui:.7f} D_INF*R={Dinf*R:.7f}")
