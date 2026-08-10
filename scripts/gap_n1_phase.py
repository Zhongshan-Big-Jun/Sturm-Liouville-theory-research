# -*- coding: utf-8 -*-
"""gap_n1_phase.py: verify Pruefer-phase formulas for symmetric SUP family self-consistency."""
import numpy as np
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

def phase_sc(mode, R, u):
    """self-consistency residual via phase formulas on half interval."""
    # half-interval: density [1,R] widths u, v=1/2-u on (0,1/2)
    v = 0.5 - u
    # solve mixed (Neumann@1/2) for w1: tan(w*sqrt(R)*v) = cot(w*u)/sqrt(R)
    # solve Dirichlet@1/2 for w2: tan(w*sqrt(R)*v) = -sqrt(R)*tan(w*u)
    # use scipy root finders on interval (0, pi/u)-ish
    from scipy.optimize import brentq
    def F1(w):
        return np.tan(w*np.sqrt(R)*v) - np.cos(w*u)/(np.sqrt(R)*np.sin(w*u))
    def F2(w):
        return np.tan(w*np.sqrt(R)*v) + np.sqrt(R)*np.tan(w*u)
    # first root of each
    ws = np.linspace(0.01, min(np.pi/u - 0.01, np.pi/(np.sqrt(R)*v) - 0.01)*0.999, 3000)
    w1 = None
    prev = F1(ws[0])
    for i in range(1, len(ws)):
        cur = F1(ws[i])
        if prev*cur < 0:
            w1 = brentq(F1, ws[i-1], ws[i]); break
        prev = cur
    w2 = None
    prev = F2(ws[0])
    for i in range(1, len(ws)):
        cur = F2(ws[i])
        if prev*cur < 0:
            w2 = brentq(F2, ws[i-1], ws[i]); break
        prev = cur
    if w1 is None or w2 is None:
        return None, None
    # normalization identity: N^2 over full [0,1] = cos^2(theta(1/2))*dtheta/dw / w^2  (half) *2?
    # For half interval mixed problem: y'(1/2)=0 => theta(1/2) = pi/2 (mod pi)
    # theta(1/2) = w*v + arctan(sqrt(R)*tan(w*u))  (phase at 1/2 for mixed)
    def dtheta_dw(w):
        # theta(x) = w*v + arctan(sqrt(R)*tan(w*u))  for mixed (continuous phase from 0)
        t = np.arctan(np.sqrt(R)*np.tan(w*u))
        dt_dw = np.sqrt(R)*(u/np.cos(w*u)**2)/(1 + R*np.tan(w*u)**2)
        return v + dt_dw
    # SC1 residual: sin^2(w1*u)/dtheta1 = sin^2(w2*u)/dtheta2  (using cos^2 theta = 1... need care)
    r = np.sin(w1*u)**2/dtheta_dw(w1) - np.sin(w2*u)**2/dtheta_dw(w2)
    return (w1, w2), r

R = 4.0
for mode in ("SUP","INF"):
    print(f"==== {mode} ====")
    for u in (0.35, 0.42, 0.4514855, 0.48):
        bl = make_blocks_sym(mode, R, u)
        fdir = f_at(bl, u)  # direct self-consistency residual
        ph = phase_sc(mode, R, u)
        if ph[0] is None:
            print(f"  u={u}: direct f(u)={fdir:+.6f}  phase: N/A")
        else:
            w1, w2 = ph[0]
            print(f"  u={u}: direct f(u)={fdir:+.6f}  phase-resid={ph[1]:+.6f}  w1={w1:.6f} w2={w2:.6f}")
