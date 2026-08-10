# -*- coding: utf-8 -*-
"""audit2.py: careful verification of eigenvalues, norms, and FH derivatives."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at, y_L, norm2_barrier, secular_roots
from clean_lib import roots2, norm_n, sec

a, b, R = 0.42, 0.56, 4.0
print("=== roots2 gives:", roots2(a, b, R))
print("=== secular_roots gives:", secular_roots(a, b, R, 4))
# scan sec(s) to count roots below 3pi
s = np.linspace(1e-8, 3*np.pi, 12001)
M = np.array([sec(si, a, b, R) for si in s])
ch = np.signbit(M[1:]) != np.signbit(M[:-1])
idx = np.nonzero(ch)[0]
print("sign changes of sec at:", [round(float(s[i]),5) for i in idx])
# evaluate y(1) at candidate roots to confirm true eigenvalues
for k in idx[:6]:
    lo, hi = s[k], s[k+1]
    for _ in range(80):
        md = 0.5*(lo+hi)
        if np.signbit(sec(md, a, b, R)) == np.signbit(sec(lo, a, b, R)): lo = md
        else: hi = md
    r = 0.5*(lo+hi)
    # check y(1) via transfer: use y_L at x=1
    yv = y_L(a, b, R, np.array([r]), np.array([1.0]))[0,0]
    print(f"  root s={r:.8f}  s^2={r*r:.6f}  y(1)={yv:.3e}")
# norms cross-check
cfg = config(a, b, R)
s, n, z0 = cfg
print("config s:", s, "n:", n, "z0:", z0)
for sk in s:
    print(f"  s={sk:.8f}: norm2_barrier={norm2_barrier(a,b,R,sk):.10f} norm_n={norm_n(sk,a,b,R):.10f}")
# FD of lambda1, lambda2, D individually
h = 1e-6
for (da, db) in [(h,0),(0,h)]:
    s1p, s2p = roots2(a+da, b+db, R)
    s1m, s2m = roots2(a-da, b-db, R)
    dl1 = (s1p**2 - s1m**2)/(2*da if db==0 else 2*db)
    dl2 = (s2p**2 - s2m**2)/(2*da if db==0 else 2*db)
    print(f"d/da{da:g} or d/db: dl1={dl1:.6f} dl2={dl2:.6f} dD={dl2-dl1:.6f}")
