# -*- coding: utf-8 -*-
import sys, math
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import numpy as np
from gap_lib import lams_fast, y_at, norm2

R = 4.0
u = 0.1
blocks = [(u,1.0),(1-2*u,R),(u,1.0)]
s = lams_fast(blocks, 2, npts=40000)
print("s:", s, "lam:", s**2)
# eigenfunction symmetry check at x=u and x=1-u
for k in range(2):
    y = y_at(blocks, s[k], np.array([u, 1-u]))
    n2 = norm2(blocks, s[k])
    uk = y/np.sqrt(n2)
    print("k=%d: u_k(u)=%.6f u_k(1-u)=%.6f  |diff|=%.2e" % (k, uk[0], uk[1], abs(uk[0]-uk[1])))
# finite-difference dlam/du
for h in [1e-4, 1e-5]:
    u2 = u + h
    blocks2 = [(u2,1.0),(1-2*u2,R),(u2,1.0)]
    s2 = lams_fast(blocks2, 2, npts=40000)
    print("h=%.0e: dlam1/du=%.4f  dlam2/du=%.4f  dD/du=%.4f" % (h, (s2[0]**2-s[0]**2)/h, (s2[1]**2-s[1]**2)/h, (s2[1]**2-s2[0]**2-s[1]**2+s[0]**2)/h))