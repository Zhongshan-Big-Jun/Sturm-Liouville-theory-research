# -*- coding: utf-8 -*-
"""gap_n1_phase4.py: correct continuous-lift phase solver + verify SC formula."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast

def Phi(mode, R, u, w):
    """continuous lift of interface phase (strictly increasing)."""
    if mode == "SUP":
        # density 1 -> R at u
        x = w*u
        j = int(np.floor((x + np.pi/2)/np.pi))  # interval index such that x in (j*pi-pi/2, j*pi+pi/2)
        # for x in (j*pi - pi/2, j*pi + pi/2): Phi = j*pi + arctan(sqrt(R)*tan(x))
        return j*np.pi + np.arctan(np.sqrt(R)*np.tan(x))
    else:
        # density R -> 1 at u; phase before interface: w*sqrt(R)*u
        x = w*np.sqrt(R)*u
        j = int(np.floor((x + np.pi/2)/np.pi))
        return j*np.pi + np.arctan(np.tan(x)/np.sqrt(R))

def theta_half(mode, R, u, w):
    v = 0.5 - u
    if mode == "SUP":
        return Phi(mode,R,u,w) + w*np.sqrt(R)*v
    else:
        return Phi(mode,R,u,w) + w*v

def eigw(mode, R, u, target):
    """solve theta_half = target (target=pi/2 mixed, pi dirichlet); theta_half strictly increasing? verify."""
    v = 0.5 - u
    # domain: need theta_half strictly increasing; use robust scan
    def G(w):
        return theta_half(mode,R,u,w) - target
    # upper bound: find w with theta_half > target
    wmax = 1.0
    while G(wmax) < 0 and wmax < 100:
        wmax *= 1.5
    if G(wmax) < 0: return None
    # check monotonicity on [0.01, wmax]
    ws = np.linspace(0.01, wmax, 4000)
    th = np.array([theta_half(mode,R,u,w) for w in ws])
    mono = np.all(np.diff(th) > -1e-9)
    if not mono:
        return None
    return brentq(G, 0.01, wmax, xtol=1e-14)

def dtheta_dw(mode, R, u, w):
    v = 0.5 - u
    if mode == "SUP":
        dPhi = np.sqrt(R)*u/(np.cos(w*u)**2 + R*np.sin(w*u)**2)
        return dPhi + np.sqrt(R)*v
    else:
        dPhi = u/(np.cos(w*np.sqrt(R)*u)**2 + np.sin(w*np.sqrt(R)*u)**2/R)
        return dPhi + v

def sc_phase(mode, R, u):
    w1 = eigw(mode, R, u, np.pi/2)
    w2 = eigw(mode, R, u, np.pi)
    if w1 is None or w2 is None: return None, None
    S1 = w1**2*np.sin(w1*u)**2/dtheta_dw(mode, R, u, w1)
    S2 = w2**2*np.sin(w2*u)**2/dtheta_dw(mode, R, u, w2)
    return S1-S2, (w1, w2)

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} ====")
    for u in (0.30, 0.35, 0.40, 0.45148550 if mode=="SUP" else 0.38259830, 0.45, 0.48):
        r = sc_phase(mode, R, u)
        bl = [(u,1.0),(1-2*u,R),(u,1.0)] if mode=="SUP" else [(u,R),(1-2*u,1.0),(u,R)]
        s = lams_fast(bl, 3, npts=90000)
        if r[0] is None:
            print(f"  u={u:.6f}: phase N/A (nonmonotone?)  direct w1={s[0]:.5f} w2={s[1]:.5f}")
        else:
            w1p, w2p = r[1]
            print(f"  u={u:.6f}: SC={r[0]:+.6f}  phase(w1,w2)=({w1p:.5f},{w2p:.5f})  direct=({s[0]:.5f},{s[1]:.5f})")
