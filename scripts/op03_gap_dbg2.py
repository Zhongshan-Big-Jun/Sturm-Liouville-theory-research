# -*- coding: utf-8 -*-
"""Independent normalization check via scipy quad."""
import numpy as np
from scipy.integrate import quad
from op03_gap_precise import lams_precise

R = 4.0
u = 0.4515
blocks = [(u,1.0),(1-2*u,R),(u,1.0)]
s = lams_precise(blocks, 3)

def y(x, s, blocks):
    # propagate from 0
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    x0 = 0.0
    for L, c in blocks:
        x1 = x0 + L
        if x <= x1:
            w = s*np.sqrt(c); d = x - x0
            cw = np.cos(w*d); sw = np.sin(w*d)/w
            return M00*cw + M01*sw
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        x0 = x1
    raise ValueError

def rho(x):
    if x < u: return 1.0
    if x < 1-u: return R
    return 1.0

for k in range(2):
    norm, _ = quad(lambda x: rho(x)*y(x, s[k], blocks)**2, 0, 1, epsabs=1e-13, limit=300)
    yj = y(u, s[k], blocks)
    print(f"k={k}: norm={norm:.10f}  y(u)={yj:.8f}  normalized y(u)^2 = {yj**2/norm:.8f}")
# compare with precise routine values
from op03_gap_precise import eigfuns_precise
vp = eigfuns_precise(blocks, s[:2], np.array([u]))
print("precise routine u1^2, u2^2 at u:", vp[0,0]**2, vp[1,0]**2)
