# -*- coding: utf-8 -*-
"""gap_n1_phase7.py: verify corrected S(w) = sin^2(phase_at_u)/I formulas."""
import numpy as np
from gap_lib import lams_fast, y_at

def make_blocks_sym(mode, R, u):
    if mode=="SUP":
        return [(u,1.0),(1-2*u,R),(u,1.0)]
    return [(u,R),(1-2*u,1.0),(u,R)]

def I_direct(blocks, w):
    x = np.linspace(0, 0.5, 40001)
    y = y_at(blocks, w, x)
    xs = [0.0]
    for L,c in blocks: xs.append(xs[-1]+L)
    rr = np.zeros(len(x))
    for i, p in enumerate(x):
        bi = max(j for j in range(len(xs)-1) if xs[j] <= p)
        rr[i] = blocks[bi][1]
    return np.trapezoid(rr*y**2, x)

def S_phase(mode, R, u, w):
    v = 0.5 - u
    if mode=="SUP":
        ph = w*u
        dPhi = np.sqrt(R)*u/(np.cos(ph)**2 + R*np.sin(ph)**2)
        dth = dPhi + np.sqrt(R)*v
        I = (R*np.sin(ph)**2 + np.cos(ph)**2)*dth/(2*w**2*np.sqrt(R))
        return np.sin(ph)**2/I
    else:
        ph = w*np.sqrt(R)*u
        dPhi = u/(np.cos(ph)**2 + np.sin(ph)**2/R)
        dth = dPhi + v
        I = (np.sin(ph)**2/R + np.cos(ph)**2)*dth/(2*w**2)
        return np.sin(ph)**2/I

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} ====")
    for u in (0.30, 0.35, 0.40, 0.45148550 if mode=="SUP" else 0.38259830, 0.45, 0.48):
        bl = make_blocks_sym(mode, R, u)
        s = lams_fast(bl, 2, npts=90000)
        S1p = S_phase(mode, R, u, s[0]); S2p = S_phase(mode, R, u, s[1])
        I1 = I_direct(bl, s[0]); I2 = I_direct(bl, s[1])
        if mode=="SUP":
            s1d = np.sin(s[0]*u)**2/I1; s2d = np.sin(s[1]*u)**2/I2
        else:
            s1d = np.sin(s[0]*np.sqrt(R)*u)**2/I1; s2d = np.sin(s[1]*np.sqrt(R)*u)**2/I2
        print(f"  u={u:.6f}: S1_phase={S1p:.6f} S1_direct={s1d:.6f} | S2_phase={S2p:.6f} S2_direct={s2d:.6f} | SC_phase={S1p-S2p:+.4f}")
