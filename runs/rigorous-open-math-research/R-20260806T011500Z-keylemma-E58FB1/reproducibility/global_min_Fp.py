# -*- coding: utf-8 -*-
"""global_min_Fp.py -- locate global min of -Fp over (1,inf)x(0,1/2)."""
import numpy as np
from scipy.optimize import brentq, minimize_scalar

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
def Fp(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mtil(a1,c,q)*Gfun(a1,c,q)-Mtil(a2,c,q)*Gfun(a2,c,q)

# coarse map
mn = 1e9; arg=None
for q in np.linspace(1.001, 3.0, 80):
    for c in np.linspace(0.001, 0.499, 120):
        v = -Fp(c,q)
        if v < mn: mn, arg = v, (q, c)
print(f'coarse min(-Fp) = {mn:.6f} at q={arg[0]:.4f} c={arg[1]:.4f}')
# refine around arg
q0, c0 = arg
for _ in range(4):
    qs = np.linspace(q0-0.03, q0+0.03, 40)
    best = (1e9, None)
    for q in qs:
        r = minimize_scalar(lambda c: -Fp(c,q), bounds=(max(1e-4,c0-0.03), min(0.4999,c0+0.03)), method='bounded')
        if r.fun < best[0]: best = (r.fun, (q, r.x))
    mn, arg = best
    q0, c0 = arg
print(f'refined min(-Fp) = {mn:.9f} at q={arg[0]:.6f} c={arg[1]:.6f}')
