# -*- coding: utf-8 -*-
"""gap_n1_phase3.py: verify balanced-phase identities at self-consistent points."""
import numpy as np
from gap_lib import lams_fast

def make_blocks_sym(mode, R, u):
    if mode=="SUP":
        return [(u,1.0),(1-2*u,R),(u,1.0)]
    return [(u,R),(1-2*u,1.0),(u,R)]

R = 4.0
pts = {"SUP": 0.45148550, "INF": 0.38259830}
for mode, u in pts.items():
    bl = make_blocks_sym(mode, R, u)
    s = lams_fast(bl, 3, npts=90000)
    w1, w2 = s[0], s[1]
    print(f"{mode}: u={u:.8f}")
    print(f"  w1={w1:.8f} w2={w2:.8f}")
    print(f"  w1*u={w1*u:.8f} (pi/2={np.pi/2:.8f})  w2*u={w2*u:.8f} (pi/4={np.pi/4:.8f}, pi/2={np.pi/2:.8f})")
    print(f"  w1*sqrt(R)*v={w1*np.sqrt(R)*(0.5-u):.8f}  w2*sqrt(R)*v={w2*np.sqrt(R)*(0.5-u):.8f}")
    print(f"  lam1={w1**2:.8f} lam2={w2**2:.8f} D={w2**2-w1**2:.8f}")
# scan: how does w2*u vary with u for SUP?
print()
print("SUP scan of w2*u vs u:")
for u in (0.30, 0.35, 0.40, 0.42, 0.45148550, 0.47):
    bl = make_blocks_sym("SUP", R, u)
    s = lams_fast(bl, 3, npts=90000)
    print(f"  u={u:.6f}: w2={s[1]:.6f} w2*u={s[1]*u:.6f} (pi/2={np.pi/2:.6f})")
print("INF scan of w2*u vs u:")
for u in (0.30, 0.35, 0.38259830, 0.42, 0.45, 0.48):
    bl = make_blocks_sym("INF", R, u)
    s = lams_fast(bl, 3, npts=90000)
    print(f"  u={u:.6f}: w2={s[1]:.6f} w2*u={s[1]*u:.6f} (pi/4={np.pi/4:.6f}, pi/2={np.pi/2:.6f})")
