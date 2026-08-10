# -*- coding: utf-8 -*-
"""gap_n1_phase2.py: corrected Pruefer-phase self-consistency for symmetric family."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def make_blocks_sym(mode, R, u):
    if mode=="SUP":
        return [(u,1.0),(1-2*u,R),(u,1.0)]
    return [(u,R),(1-2*u,1.0),(u,R)]

def f_at(blocks, x):
    s = lams_fast(blocks, 2)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def lifted_arctan(t):
    """arctan with continuous lift; returns angle in (-pi/2, pi/2)"""
    return np.arctan(t)

def theta_half(mode, R, u, w):
    """Pruefer phase at 1/2 (continuous lift from 0)."""
    v = 0.5 - u
    if mode == "SUP":
        # (0,u): rho=1 -> theta=w*x; at u refract: tan(t) = sqrt(R)*tan(w*u)
        # on (u,1/2): theta advances by p*(x-u)
        base = np.arctan(np.sqrt(R)*np.tan(w*u))
        # handle branch: theta continuous
        return w*v + base
    else:
        # (0,u): rho=R -> theta=w*sqrt(R)*x; refract: tan = tan/(sqrt(R))
        base = np.arctan(np.tan(w*np.sqrt(R)*u)/np.sqrt(R))
        return w*v + base

def dtheta_dw(mode, R, u, w):
    v = 0.5 - u
    if mode == "SUP":
        den = R*np.sin(w*u)**2 + np.cos(w*u)**2
        return v + np.sqrt(R)*u/den
    else:
        den = np.sin(w*np.sqrt(R)*u)**2/R + np.cos(w*np.sqrt(R)*u)**2
        return v + u/den

def eigw(mode, R, u, which):
    """which=1: mixed (Neumann@1/2), which=2: Dirichlet@1/2.  Returns w."""
    v = 0.5 - u
    # scan phase = pi/2 (mixed) or pi (dirichlet)
    target = np.pi/2 if which==1 else np.pi
    # theta_half as function of w; find first crossing of target
    ws = np.linspace(0.01, np.pi/u - 1e-6 if np.pi/u < 50 else 50, 6000)
    if ws[-1] <= ws[0]: return None
    prev = theta_half(mode, R, u, ws[0]) - target
    prev2 = theta_half(mode, R, u, ws[0])
    # handle monotone increasing theta? not monotone due to tan branches; use sign of (theta-target)
    # simpler: theta continuous lift may jump by pi at poles; we want crossings of target modulo 2pi...
    # Use: theta mod pi == target mod pi. Track (theta-target)/pi rounding.
    def F(w):
        th = theta_half(mode, R, u, w)
        return np.sin(th) if which==1 else np.sin(th)
    # mixed: cos(th)=0; dirichlet: sin(th)=0 -> use cos(th) for mixed
    def G(w):
        th = theta_half(mode, R, u, w)
        return np.cos(th) if which==1 else np.sin(th)
    prev = G(ws[0])
    for i in range(1, len(ws)):
        cur = G(ws[i])
        if prev*cur < 0:
            return brentq(G, ws[i-1], ws[i], xtol=1e-14)
        prev = cur
    return None

def sc_phase(mode, R, u):
    w1 = eigw(mode, R, u, 1)
    w2 = eigw(mode, R, u, 2)
    if w1 is None or w2 is None: return None
    S1 = w1**2*np.sin(w1*u)**2/dtheta_dw(mode, R, u, w1)
    S2 = w2**2*np.sin(w2*u)**2/dtheta_dw(mode, R, u, w2)
    return S1 - S2, w1, w2

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} ====")
    for u in (0.30, 0.35, 0.3825983, 0.40, 0.42, 0.4514855, 0.48):
        bl = make_blocks_sym(mode, R, u)
        fdir = f_at(bl, u)
        r = sc_phase(mode, R, u)
        if r is None:
            print(f"  u={u}: direct f={fdir:+.6f}  phase N/A")
        else:
            print(f"  u={u}: direct f={fdir:+.6f}  phase SC={r[0]:+.6f}  w1={r[1]:.5f} w2={r[2]:.5f}")
