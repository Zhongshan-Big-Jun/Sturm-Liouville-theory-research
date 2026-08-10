# -*- coding: utf-8 -*-
"""direct_bounds.py -- min |G1|, max |G2|, min H on Region B."""
import numpy as np
from scipy.optimize import brentq

def Phi(a, q): return np.cos(a)**2 + q*q*np.sin(a)**2
def Wfun(a): return 3 + 2*a/np.tan(a)
def E_curve(a, q): return np.arctan(1.0/(q*np.tan(a)))
def O_curve(a, q):
    a = np.asarray(a, dtype=float); out = np.empty_like(a)
    hi = a > np.pi/2; eq = a == np.pi/2
    out[eq] = np.pi/2
    out[hi] = np.arctan(-q*np.tan(a[hi]))
    out[~hi & ~eq] = np.pi - np.arctan(q*np.tan(a[~hi & ~eq]))
    return out
def alpha1(c, q): return brentq(lambda a: E_curve(a,q)-c*a, 1e-12, np.pi/2 - 1e-13)
def alpha2(c, q): return brentq(lambda a: O_curve(a,q)-c*a, np.pi/2 + 1e-13, np.pi - 1e-13)
def Gfun(a, c, q):
    Ph = Phi(a,q); return -Ph*Wfun(a)/(q+c*Ph) + 2*c*a*Ph*(q*q-1)*np.sin(a)*np.cos(a)/(q+c*Ph)**2
def cG2(q):
    if Gfun(alpha2(0.5,q),0.5,q) >= 0: return None
    return brentq(lambda c: Gfun(alpha2(c,q),c,q), 0.40, 0.5)

mnG1 = 1e9; mxG2 = -1e9; mnH = 1e9
arg1 = arg2 = arg3 = None
for qi in range(1, 90):
    q = 1.0 + 0.87*qi/89
    cb = cG2(q)
    if cb is None: continue
    for k in range(101):
        c = cb + (0.5-cb)*k/100
        a1=alpha1(c,q); a2=alpha2(c,q)
        g1=Gfun(a1,c,q); g2=Gfun(a2,c,q)
        if g2 >= 0: continue
        if -g1 < mnG1: mnG1, arg1 = -g1, (q,c)
        if -g2 > mxG2: mxG2, arg2 = -g2, (q,c)
        if g2-g1 < mnH: mnH, arg3 = g2-g1, (q,c)
print(f'min |G1| on Region B = {mnG1:.6f} at {arg1}')
print(f'max |G2| on Region B = {mxG2:.6f} at {arg2}')
print(f'min H on Region B    = {mnH:.6f} at {arg3}')
