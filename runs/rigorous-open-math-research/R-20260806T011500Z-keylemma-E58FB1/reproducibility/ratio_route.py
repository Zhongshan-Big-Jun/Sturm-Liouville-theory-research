# -*- coding: utf-8 -*-
"""ratio_route.py -- |G1|/|G2| vs M2t/M1t on Region B; find tight spots."""
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
def Mtil(a, c, q): return a*a*np.sin(a)**2/(q + c*Phi(a,q))
def Gfun(a, c, q):
    Ph = Phi(a,q); return -Ph*Wfun(a)/(q+c*Ph) + 2*c*a*Ph*(q*q-1)*np.sin(a)*np.cos(a)/(q+c*Ph)**2
def cG2(q):
    if Gfun(alpha2(0.5,q),0.5,q) >= 0: return None
    return brentq(lambda c: Gfun(alpha2(c,q),c,q), 0.40, 0.5)

print('=== Region B: min |G1|/|G2|, max M2t/M1t, and margin ===')
mn_ratio = 1e9; mx_rho = -1e9; worst = None
for qi in range(1, 45):
    q = 1.0 + 0.87*qi/44
    cb = cG2(q)
    if cb is None: continue
    for k in range(101):
        c = cb + (0.5-cb)*k/100
        a1=alpha1(c,q); a2=alpha2(c,q)
        g1=Gfun(a1,c,q); g2=Gfun(a2,c,q)
        if g2 >= 0: continue
        ratio = (-g1)/(-g2)
        rho = Mtil(a2,c,q)/Mtil(a1,c,q)
        if ratio < mn_ratio: mn_ratio, worst = ratio, ('ratio', q, c, ratio, rho)
        if rho > mx_rho: mx_rho, worst2 = rho, ('rho', q, c, ratio, rho)
print(f'  min |G1|/|G2| = {mn_ratio:.4f} at {worst}')
print(f'  max M2t/M1t  = {mx_rho:.4f} at {worst2}')
print(f'  margin (min ratio - max rho) = {mn_ratio - mx_rho:.4f}')
