# -*- coding: utf-8 -*-
"""audit_fh_t3.py: check FH derivative formulas (true vs source) and T3 identity.
Point: (a,b,R) = (0.42,0.56,4.0) as in the tool file residual-exactness.md."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at, y_L, norm2_barrier
from clean_lib import roots2, norm_n

def lam(a, b, R):
    s1, s2 = roots2(a, b, R)
    return s1*s1, s2*s2

def u2_at(a, b, R, x):
    cfg = config(a, b, R)
    s, n, z0 = cfg
    y = y_L(a, b, R, s, np.array([x]))[:, 0]
    return (y/n)[0]**2, (y/n)[1]**2

a, b, R = 0.42, 0.56, 4.0
l1, l2 = lam(a, b, R)
u1a, u2a = u2_at(a, b, R, a)
u1b, u2b = u2_at(a, b, R, b)
print(f"lambda1={l1:.8f} lambda2={l2:.8f}")
print(f"u1(a)^2={u1a:.8f} u2(a)^2={u2a:.8f} u1(b)^2={u1b:.8f} u2(b)^2={u2b:.8f}")
R1 = l1*u1a - l2*u2a
R2 = l1*u1b - l2*u2b
print(f"R1=f(a)={R1:.8f}  R2=f(b)={R2:.8f}")
print(f"true FH dD/da = (R-1)(u2a^2-u1a^2) = {3*(u2a-u1a):.8f}")
print(f"source  dD/da = -(R-1)*R1            = {-3*R1:.8f}")
print(f"true FH dD/db = -(R-1)(u2b^2-u1b^2) = {-3*(u2b-u1b):.8f}")
print(f"source  dD/db = +(R-1)*R2            = {3*R2:.8f}")
# FD check of dD/da, dD/db
h = 1e-6
l1a, l2a = lam(a+h, b, R); l1m, l2m = lam(a-h, b, R)
Dp_a = ((l2a-l1a)-(l2m-l1m))/(2*h)
l1b, l2b = lam(a, b+h, R); l1m, l2m = lam(a, b-h, R)
Dp_b = ((l2b-l1b)-(l2m-l1m))/(2*h)
print(f"FD dD/da = {Dp_a:.8f}   FD dD/db = {Dp_b:.8f}")
# T3 check
R1_b = (f_at(a, b+h, R, a, None) - f_at(a, b-h, R, a, None))/(2*h)
R2_a = (f_at(a+h, b, R, b, None) - f_at(a-h, b, R, b, None))/(2*h)
print(f"T3: dR1/db = {R1_b:.6f}  -dR2/da = {-R2_a:.6f}  sum = {R1_b + R2_a:.2e}")
# source's claimed relation: -3R1 vs FD dD/da
print(f"source claim check: -(R-1)R1 = {-3*R1:.6f} vs FD dD/da = {Dp_a:.6f}")
