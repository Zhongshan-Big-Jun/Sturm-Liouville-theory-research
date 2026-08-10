# -*- coding: utf-8 -*-
"""G2_decreasing.py -- dG2/dc sign on (a) (0,1/2) x q>=2 ; (b) (0,0.4] x q>1."""
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

print('=== (a) max dG2/dc over (0.01,0.49) x q in [2,100] ===')
mx = -1e9; arg=None
for q in [2.0, 2.5, 3.0, 5.0, 10.0, 50.0, 100.0]:
    for c in np.linspace(0.02, 0.49, 60):
        h=1e-5
        d = (G2(c+h,q)-G2(c-h,q))/(2*h)
        if d > mx: mx, arg = d, (q, c)
print(f'  max dG2/dc = {mx:+.4f} at {arg}')
print()
print('=== (b) max dG2/dc over (0.01,0.39) x q in (1,2] ===')
mx = -1e9; arg=None
for q in [1.001, 1.05, 1.1, 1.3, 1.5, 1.8, 2.0]:
    for c in np.linspace(0.02, 0.39, 60):
        h=1e-5
        d = (G2(c+h,q)-G2(c-h,q))/(2*h)
        if d > mx: mx, arg = d, (q, c)
print(f'  max dG2/dc = {mx:+.4f} at {arg}')
print()
print('=== G2(q,0.4) for q in (1, inf): min ===')
mn = 1e9; arg=None
for q in [1.001, 1.01, 1.05, 1.1, 1.3, 1.5, 1.8, 2.0, 3.0, 10.0, 100.0]:
    v = G2(0.4, q)
    if v < mn: mn, arg = v, q
print(f'  min G2(0.4,q) = {mn:+.6f} at q={arg}')
print('=== G2(q,1/2) for q >= 2: min ===')
mn = 1e9; arg=None
for q in [2.0, 2.01, 2.1, 2.5, 3.0, 10.0, 100.0]:
    v = G2(0.5, q)
    if v < mn: mn, arg = v, q
print(f'  min G2(0.5,q) = {mn:+.6f} at q={arg}')
