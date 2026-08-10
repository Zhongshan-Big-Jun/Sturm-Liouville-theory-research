# -*- coding: utf-8 -*-
"""G2_dc_04.py -- dG2/dc on (0,0.4) for all q: negative?"""
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

mx = -1e9; arg=None
for q in [1.001, 1.05, 1.1, 1.3, 1.5, 1.8, 2.0, 3.0, 5.0, 10.0, 100.0, 1000.0]:
    for c in np.linspace(0.01, 0.39, 80):
        h=1e-5
        d = (G2(c+h,q)-G2(c-h,q))/(2*h)
        if d > mx: mx, arg = d, (q, c)
print(f'max dG2/dc over (0.01,0.39) x q in [1.001,1000] = {mx:+.4f} at {arg}')
print()
# G2(q,0.4) as function of q: min?
mn = 1e9; arg=None
for q in np.linspace(1.0001, 50, 400):
    v = G2(0.4, q)
    if v < mn: mn, arg = v, q
print(f'min G2(0.4,q) over q in (1,50] = {mn:+.6f} at q={arg:.4f}')
# asymptotic check
for q in [100.0, 1000.0]:
    print(f'  G2(0.4,{q}) = {G2(0.4,q):+.4f}')
