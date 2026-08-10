# -*- coding: utf-8 -*-
"""gap_n1_symshape.py: D(u) and SC(u) shape for symmetric family."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast

def make_blocks_sym(mode, R, u):
    if mode=="SUP":
        return [(u,1.0),(1-2*u,R),(u,1.0)]
    return [(u,R),(1-2*u,1.0),(u,R)]

def theta_half(mode, R, u, w):
    v = 0.5 - u
    if mode=="SUP":
        x = w*u
        j = int(np.floor((x+np.pi/2)/np.pi))
        Phi = j*np.pi + np.arctan(np.sqrt(R)*np.tan(x))
        return Phi + w*np.sqrt(R)*v
    else:
        x = w*np.sqrt(R)*u
        j = int(np.floor((x+np.pi/2)/np.pi))
        Phi = j*np.pi + np.arctan(np.tan(x)/np.sqrt(R))
        return Phi + w*v

def eigw(mode, R, u, target):
    def G(w): return theta_half(mode,R,u,w) - target
    wmax = 1.0
    while G(wmax) < 0 and wmax < 200: wmax *= 1.4
    if G(wmax) < 0: return None
    return brentq(G, 0.01, wmax, xtol=1e-13)

def SC(mode, R, u):
    w1 = eigw(mode, R, u, np.pi/2)
    w2 = eigw(mode, R, u, np.pi)
    if w1 is None or w2 is None: return None
    if mode=="SUP":
        d1 = np.sqrt(R)*u/(np.cos(w1*u)**2+R*np.sin(w1*u)**2) + np.sqrt(R)*(0.5-u)
        d2 = np.sqrt(R)*u/(np.cos(w2*u)**2+R*np.sin(w2*u)**2) + np.sqrt(R)*(0.5-u)
        S1 = np.sin(w1*u)**2*2*w1**2*np.sqrt(R)/((R*np.sin(w1*u)**2+np.cos(w1*u)**2)*d1)
        S2 = np.sin(w2*u)**2*2*w2**2*np.sqrt(R)/((R*np.sin(w2*u)**2+np.cos(w2*u)**2)*d2)
    else:
        d1 = u/(np.cos(w1*np.sqrt(R)*u)**2+np.sin(w1*np.sqrt(R)*u)**2/R) + (0.5-u)
        d2 = u/(np.cos(w2*np.sqrt(R)*u)**2+np.sin(w2*np.sqrt(R)*u)**2/R) + (0.5-u)
        S1 = np.sin(w1*np.sqrt(R)*u)**2*2*w1**2/((np.sin(w1*np.sqrt(R)*u)**2/R+np.cos(w1*np.sqrt(R)*u)**2)*d1)
        S2 = np.sin(w2*np.sqrt(R)*u)**2*2*w2**2/((np.sin(w2*np.sqrt(R)*u)**2/R+np.cos(w2*np.sqrt(R)*u)**2)*d2)
    return S1-S2, w1, w2

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} ====")
    us = np.linspace(0.06, 0.49, 44)
    for u in us:
        bl = make_blocks_sym(mode, R, u)
        s = lams_fast(bl, 3, npts=60000)
        D = s[1]**2 - s[0]**2
        r = SC(mode, R, u)
        print(f"  u={u:.3f}: D={D:.5f}  SC={r[0]:+.4f}" if r[0] is not None else f"  u={u:.3f}: D={D:.5f}")
