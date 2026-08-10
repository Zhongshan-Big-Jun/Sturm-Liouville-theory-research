# -*- coding: utf-8 -*-
"""SUP R->inf structure: lam1, lam2 at u*~0.5."""
import numpy as np
from scipy.optimize import brentq

def sec_DN(u, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    a = s*q1*u; b = s*q2*(0.5-u)
    return np.cos(a)*np.cos(b)/q2 - np.sin(a)*np.sin(b)/q1

def sec_DD(u, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    a = s*q1*u; b = s*q2*(0.5-u)
    return np.sin(a)*np.cos(b)/q1 + np.cos(a)*np.sin(b)/q2

for R, u in [(1e4, 0.4988060), (1e6, 0.4998801)]:
    g = np.linspace(1e-8, 25, 200000)
    for which, f in [('DN', lambda s: sec_DN(u, 1.0, R, s)), ('DD', lambda s: sec_DD(u, 1.0, R, s))]:
        v = np.array([f(ss) for ss in g])
        sg = np.signbit(v)
        idx = np.nonzero(sg[1:] != sg[:-1])[0]
        s = brentq(f, g[idx[0]], g[idx[0]+1])
        print(f"R={R}: {which} s={s:.10f} lam={s**2:.10f}")
