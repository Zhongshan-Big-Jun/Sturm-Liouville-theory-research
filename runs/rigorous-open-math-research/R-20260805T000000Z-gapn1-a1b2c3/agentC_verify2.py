# -*- coding: utf-8 -*-
"""Comprehensive verification of Subclaim 1: D(t) in (3pi^2/R, 3pi^2) for both orientations.
Uses direct transfer-matrix root finding (independent of phase formula)."""
import numpy as np
from scipy.optimize import brentq

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    return (np.sin(w1*t)/q1)*np.cos(w2*(1-t)) + np.cos(w1*t)*np.sin(w2*(1-t))/q2

def lams_direct(t, c1, c2, k=2, n_s=120000):
    smax = np.pi*np.sqrt(max(c1,c2))*(k+2)+10
    s = np.linspace(1e-7, smax, n_s)
    M = M01_2block(t, c1, c2, s)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0][:k]
    roots = [brentq(lambda x: M01_2block(t, c1, c2, x), s[idx[j]], s[idx[j]+1]) for j in range(k)]
    return np.array(roots)

PI2 = np.pi**2
bad_lo = bad_hi = 0
worst_lo_margin = 1.0   # min of (D - 3pi^2/R)/D ; want > 0
worst_hi_margin = 1.0   # min of (3pi^2 - D)/3pi^2
for R in [1.05, 1.2, 1.5, 2.0, 4.0, 10.0, 100.0, 1e4]:
    for t in np.linspace(0.002, 0.998, 250):
        for hl in (False, True):
            c1, c2 = (R,1.0) if hl else (1.0,R)
            s = lams_direct(t, c1, c2)
            D = s[1]**2 - s[0]**2
            lo_m = (D - 3*PI2/R)/D
            hi_m = (3*PI2 - D)/3*PI2
            if D <= 3*PI2/R: bad_lo += 1
            if D >= 3*PI2: bad_hi += 1
            worst_lo_margin = min(worst_lo_margin, lo_m)
            worst_hi_margin = min(worst_hi_margin, hi_m)
print(f"violations: lower {bad_lo}, upper {bad_hi}")
print(f"worst relative lower margin (D-3pi^2/R)/D = {worst_lo_margin:+.3e}")
print(f"worst relative upper margin (3pi^2-D)/3pi^2 = {worst_hi_margin:+.3e}")
