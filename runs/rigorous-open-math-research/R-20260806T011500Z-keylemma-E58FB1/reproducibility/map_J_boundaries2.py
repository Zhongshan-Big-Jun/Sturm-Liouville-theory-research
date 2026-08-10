# -*- coding: utf-8 -*-
"""map_J_boundaries2.py -- robust boundary comparison: c_G2 vs c_J2."""
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
def Gc(a, c, q):
    Ph = Phi(a,q); W = Wfun(a); s=np.sin(a); co=np.cos(a); den=q+c*Ph
    return Ph*Ph*W/den**2 + 2*a*Ph*(q*q-1)*s*co*(q-c*Ph)/den**3
def Ga(a, c, q):
    Ph=Phi(a,q); Php=2*(q*q-1)*np.sin(a)*np.cos(a); W=Wfun(a); Wp=2*(np.sin(a)*np.cos(a)-a)/np.sin(a)**2
    s=np.sin(a); co=np.cos(a); den=q+c*Ph
    A=Ph*W; Ap=Php*W+Ph*Wp; Dp=c*Php
    B=2*c*a*Ph*(q*q-1)*s*co
    Bp=2*c*(q*q-1)*((Ph+a*Php)*s*co + a*Ph*(co*co-s*s))
    return -(Ap*den-A*Dp)/den**2 + (Bp*den-2*B*Dp)/den**3
def Gprime(a, c, q):
    Ph=Phi(a,q); ap=-a*Ph/(q+c*Ph)
    return Ga(a,c,q)*ap + Gc(a,c,q)
def J(a, c, q):
    g=Gfun(a,c,q); return g*g+Gprime(a,c,q)
def find_zero(f, lo, hi, n=200):
    prev = f(lo); plo = lo
    for k in range(1, n+1):
        cc = lo + (hi-lo)*k/n; v = f(cc)
        if np.isfinite(v) and np.isfinite(prev) and (prev < 0) != (v < 0):
            return brentq(f, plo, cc)
        prev, plo = v, cc
    return None

print('=== c_G2 vs c_J2 (only if both exist) ===')
for q in [1.001, 1.01, 1.05, 1.1, 1.2, 1.3, 1.5, 1.7, 1.8, 1.85, 1.9, 2.0]:
    def g2(c): return Gfun(alpha2(c,q),c,q)
    def j2(c): return J(alpha2(c,q),c,q)
    cG = find_zero(g2, 0.30, 0.5) if g2(0.5) < 0 else None
    cJ = find_zero(j2, 0.01, 0.5) if j2(0.5) < 0 else None
    a0 = 2*np.arcsin(1/np.sqrt(2*(q+1)))
    print(f'  q={q:<5}: alpha0={a0:.4f}  c_G2={cG if cG is None else round(cG,5)}  c_J2={cJ if cJ is None else round(cJ,5)}'
          f'  (c_G2 <= c_J2 ? {cG is not None and (cJ is None or cG <= cJ)})')
