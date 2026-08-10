# -*- coding: utf-8 -*-
"""Verify D_sym(u), f_sym(u), dD/du vs FH sign, endpoints. R=4."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=60000):
    return lams_fast(blocks, 2, npts=npts)

def D_and_f(mode, R, u, npts=60000):
    b = 1-2*u
    bl = [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]
    s = s_of(bl, npts)
    lam = s**2
    u1 = y_at(bl, s[0], np.array([u]))[0]/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], np.array([u]))[0]/np.sqrt(norm2(bl, s[1]))
    return lam[1]-lam[0], lam[0]*u1**2 - lam[1]*u2**2, lam

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} R={R} ====")
    us = [0.005,0.02,0.05,0.1,0.2,0.3,0.35,0.4,0.45,0.47,0.49,0.495]
    prev=None
    for u in us:
        D,f,lam = D_and_f(mode,R,u)
        dDdu = None
        if prev is not None:
            du = u-prev[0]
            dDdu = (D-prev[1])/du
        sign = np.sign(dDdu) if dDdu is not None else None
        fh = -2*(R-1)*f if mode=="INF" else 2*(R-1)*f
        print(f"  u={u:.4f}: D={D:10.6f} f={f:+10.4f} dD/du~{dDdu if dDdu is None else round(dDdu,4)}  FH-2(R-1)f={fh:+.4f}")
        prev=(u,D)
    # find u* via brentq on f
    from scipy.optimize import brentq
    ua,ub = 0.01,0.49
    r = brentq(lambda u: D_and_f(mode,R,u)[1], ua, ub, xtol=1e-12)
    D,f,lam = D_and_f(mode,R,r)
    print(f"  u*={r:.10f} D*={D:.10f} lam1={lam[0]:.8f} lam2={lam[1]:.8f}")
    print()
