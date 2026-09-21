# -*- coding: utf-8 -*-
"""Check: for symmetric [1,R,1]_u family, is f(u)==f(1-u) and dD/du==0?"""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def D_and_f(mode, R, u, npts=90000):
    b = 1-2*u
    bl = [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]
    s = lams_fast(bl, 2, npts=npts)
    lam = s**2
    n1 = norm2(bl, s[0]); n2 = norm2(bl, s[1])
    pts = np.array([u, 1.0-u])
    y1 = y_at(bl, s[0], pts)/np.sqrt(n1)
    y2 = y_at(bl, s[1], pts)/np.sqrt(n2)
    f = lam[0]*y1**2 - lam[1]*y2**2
    return lam[1]-lam[0], f, lam

for mode in ("SUP","INF"):
    R = 4.0
    print(f"==== {mode} R={R} ====")
    for u in (0.2, 0.3, 0.4, 0.45):
        D0, f, lam = D_and_f(mode, R, u)
        eps = 1e-4
        D1, _, _ = D_and_f(mode, R, u+eps)
        num_deriv = (D1-D0)/eps
        fh = (R-1)*(f[0]-f[1])   # dD/du via FH with symmetric variation
        fh2 = -2*(R-1)*f[0]      # handoff formula
        print(f"u={u}: D={D0:.6f}  num dD/du={(num_deriv):+.4f}  f(u)={f[0]:+.4f} f(1-u)={f[1]:+.4f}  FH_sym={(fh):+.4f}  FH_handoff={(fh2):+.4f}")
