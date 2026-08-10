# -*- coding: utf-8 -*-
"""G2_cmono.py -- dG2/dc for q in {2,3,10}: sign and tight spots."""
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

print('=== dG2/dc for q >= 2 ===')
for q in [2.0, 2.5, 3.0, 5.0, 10.0, 100.0]:
    mn = 1e9; arg=None
    for c in np.linspace(0.01, 0.49, 100):
        h = 1e-5
        d = (G2(c+h,q)-G2(c-h,q))/(2*h)
        if d < mn: mn, arg = d, c
    # value at c=0.01 and c=0.5
    print(f'  q={q:<6}: min dG2/dc={mn:+.4f} at c={arg:.3f} | G2(0.5)={G2(0.5,q):+.5f} G2(0.05)={G2(0.05,q):+.6f}')
