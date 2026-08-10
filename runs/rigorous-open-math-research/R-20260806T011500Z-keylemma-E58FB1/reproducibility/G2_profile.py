# -*- coding: utf-8 -*-
"""G2_profile.py -- profile G2(c) for q in {2, 10, 100}."""
import numpy as np
from scipy.optimize import brentq

def Phi(a, q): return np.cos(a)**2 + q*q*np.sin(a)**2
def Wfun(a): return 3 + 2*a/np.tan(a)
def O_curve(a, q):
    a = np.asarray(a, dtype=float); out = np.empty_like(a)
    hi = a > np.pi/2; eq = a == np.pi/2
    out[eq] = np.pi/2
    out[hi] = np.arctan(-q*np.tan(a[hi]))
    out[~hi & ~eq] = np.pi - np.arctan(q*np.tan(a[~hi & ~eq]))
    return out
def alpha2(c, q): return brentq(lambda a: O_curve(a,q)-c*a, np.pi/2 + 1e-13, np.pi - 1e-13)
def G2(c,q):
    a2 = alpha2(c,q)
    Ph = Phi(a2,q)
    return -Ph*Wfun(a2)/(q+c*Ph) + 2*c*a2*Ph*(q*q-1)*np.sin(a2)*np.cos(a2)/(q+c*Ph)**2

for q in [2.0, 10.0, 100.0]:
    cs = np.linspace(0.01, 0.5, 50)
    vals = [G2(c,q) for c in cs]
    print(f'q={q}: G2 at c=0.01..0.5:')
    for c, v in zip(cs[::7], vals[::7]):
        print(f'    c={c:.3f}: {v:+.5f}')
    # min location
    i = int(np.argmin(vals))
    print(f'    -> min at c={cs[i]:.3f}: {vals[i]:+.5f}')
    # derivative scan
    h=1e-5
    ds = [(G2(c+h,q)-G2(c-h,q))/(2*h) for c in cs]
    print(f'    dG2/dc range: [{min(ds):+.3f}, {max(ds):+.3f}]')
