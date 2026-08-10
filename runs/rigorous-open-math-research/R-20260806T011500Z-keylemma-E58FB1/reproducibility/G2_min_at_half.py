# -*- coding: utf-8 -*-
"""G2_min_at_half.py -- is G2(q,c) >= G2(q,1/2) for all c in (0,1/2), q >= q* ?"""
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

print('=== min over c vs G2(1/2) ===')
for q in [1.87, 1.9, 2.0, 2.5, 3.0, 5.0, 10.0]:
    cs = np.linspace(1e-4, 0.4999, 2001)
    vals = np.array([G2(c,q) for c in cs])
    mn = vals.min(); arg = cs[vals.argmin()]
    g12 = G2(0.5,q)
    print(f'  q={q:<5}: min G2 = {mn:+.6f} at c={arg:.4f} | G2(1/2)={g12:+.6f} | diff={g12-mn:+.2e}')
