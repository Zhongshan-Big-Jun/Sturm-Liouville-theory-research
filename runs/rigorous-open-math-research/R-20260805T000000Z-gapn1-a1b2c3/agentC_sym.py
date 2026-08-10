# -*- coding: utf-8 -*-
"""Agent C: symmetric 3-block SUP/INF families: D(u), u*, endpoint behavior."""
import numpy as np
from scipy.optimize import brentq

def M_block(L, c, s):
    w = s*np.sqrt(c); q = np.sqrt(c)
    return np.array([[np.cos(w*L), np.sin(w*L)/q], [-q*np.sin(w*L), np.cos(w*L)]])

def M01_sym(u, R, s, sup):
    # 3 blocks: [u, c1], [1-2u, c2], [u, c1]; sup: c1=1,c2=R ; inf: c1=R,c2=1
    c1, c2 = (1.0, R) if sup else (R, 1.0)
    M = M_block(u, c1, s) @ M_block(1-2*u, c2, s) @ M_block(u, c1, s)
    return M[0,1]

def lams_sym(u, R, sup, k=3):
    smax = np.pi*np.sqrt(max(1.0, R))*(k+2)+10
    s = np.linspace(1e-9, smax, 120000)
    d = np.array([M01_sym(u, R, x, sup) for x in s])
    sg = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(sg)[0]
    roots = []
    for i in idx[:k]:
        roots.append(brentq(lambda x: M01_sym(u, R, x, sup), s[i], s[i+1]))
    return np.array(roots)

print("=== SUP family (R=4): D(u) vs 3pi^2 ===")
R = 4.0
for u in [1e-4, 0.1, 0.2, 0.3, 0.4, 0.45, 0.45148546584, 0.46, 0.48, 0.49, 0.499, 0.4999, 0.5-1e-6]:
    s = lams_sym(u, R, True)
    D = s[1]**2 - s[0]**2
    print(f"  u={u:.12f}: D={D:.10f}  D-3pi^2={D-3*np.pi**2:+.6e}")

print("=== INF family (R=4): D(u) vs 3pi^2/R ===")
for u in [1e-4, 0.1, 0.2, 0.3, 0.35, 0.3825982568, 0.4, 0.45, 0.49, 0.4999]:
    s = lams_sym(u, R, False)
    D = s[1]**2 - s[0]**2
    print(f"  u={u:.12f}: D={D:.10f}  D-3pi^2/R={D-3*np.pi**2/R:+.6e}")

print("=== R=1.05 check ===")
R = 1.05
for u in [0.45, 0.45148546584, 0.49]:
    s = lams_sym(u, R, True)
    print(f"  SUP u={u}: D={s[1]**2-s[0]**2:.8f}  D-3pi^2={s[1]**2-s[0]**2-3*np.pi**2:+.3e}")
