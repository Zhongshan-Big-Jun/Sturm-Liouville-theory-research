# -*- coding: utf-8 -*-
"""Compare coarse vs precise eigenfunction machinery on identical inputs."""
import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise
from op03_gap_n1 import eigfuns_at

R = 4.0
u = 0.4515
blocks = [(u,1.0),(1-2*u,R),(u,1.0)]
s = lams_precise(blocks, 3)
lam = s**2
pts = np.array([u])
vc = eigfuns_at(blocks, lam[:2], pts)
vp = eigfuns_precise(blocks, s[:2], pts)
print("s^2:", lam[:2])
print("coarse y(u):", vc[:,0], "  norms implied:", (vc[:,0]**2))
print("precise y(u):", vp[:,0], "  norms implied:", (vp[:,0]**2))

# Raw (unnormalized) y values: y(x) = M01 for initial (0,1)
def raw_y(x, ss):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    x0 = 0.0
    for L, c in blocks:
        x1 = x0 + L
        w = ss*np.sqrt(c)
        if x <= x1:
            d = x - x0
            cw = np.cos(w*d); sw = np.sin(w*d)/w
            return M00*cw + M01*sw
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        x0 = x1
print("raw y(u) check:", raw_y(u, s[0]), raw_y(u, s[1]))
# norm via exact per-block
def exact_norm(ss):
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    norm = 0.0
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    for bi, (L, c) in enumerate(blocks):
        w = ss*np.sqrt(c)
        A = M01; B = M11/w
        Icos = 0.5*(L + np.sin(2*w*L)/(2*w))
        Isin = 0.5*(L - np.sin(2*w*L)/(2*w))
        Icross = np.sin(w*L)**2/(2*w)
        norm += c*(A*A*Icos + B*B*Isin + 2*A*B*Icross)
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return norm
for k in range(2):
    print(f"k={k}: raw y(u)={raw_y(u, s[k]):.8f} exact norm={exact_norm(s[k]):.8f} -> normalized^2={raw_y(u,s[k])**2/exact_norm(s[k]):.8f}")
