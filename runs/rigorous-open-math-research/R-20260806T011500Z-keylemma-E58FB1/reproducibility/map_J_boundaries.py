# -*- coding: utf-8 -*-
"""map_J_boundaries.py -- compare boundaries: G2=0 vs J2=0 vs J1=0; profile J on ranges."""
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

print('=== boundaries: c_G2 (G2=0), c_J2 (J(a2)=0), c_J1 (J(a1)=0) ===')
for q in [1.01, 1.1, 1.3, 1.5, 1.7, 1.85, 2.0]:
    def g2zero(c): return Gfun(alpha2(c,q),c,q)
    def j2zero(c): return J(alpha2(c,q),c,q)
    def j1zero(c): return J(alpha1(c,q),c,q)
    cG = None; cJ2 = None; cJ1 = None
    try:
        if g2zero(0.5) < 0: cG = brentq(g2zero, 0.30, 0.5)
    except ValueError: pass
    try:
        if j2zero(0.5) < 0:
            # find bracket
            lo=0.0; hi=0.5
            # scan for sign change
            prev = j2zero(0.0); clo = 0.0
            for k in range(1, 101):
                cc = 0.5*k/100; v = j2zero(cc)
                if (prev<0)!=(v<0):
                    lo, hi = clo, cc; break
                prev, clo = v, cc
            cJ2 = brentq(j2zero, lo, hi)
    except ValueError: pass
    try:
        v0 = j1zero(0.0); v5 = j1zero(0.5)
        if v0 < 0 or v5 < 0:
            prev = v0; clo = 0.0
            for k in range(1, 101):
                cc = 0.5*k/100; v = j1zero(cc)
                if (prev<0)!=(v<0):
                    cJ1 = brentq(j1zero, clo, cc); break
                prev, clo = v, cc
    except ValueError: pass
    print(f'  q={q:<5}: c_G2={cG if cG is None else round(cG,4)}  c_J2={cJ2 if cJ2 is None else round(cJ2,4)}  c_J1={cJ1 if cJ1 is None else round(cJ1,4)}')

print()
print('=== J(alpha) profile: q=1.5, c in {0.46, 0.49, 0.499} ===')
q = 1.5
a0 = 2*np.arcsin(1/np.sqrt(2*(q+1)))
print(f'  alpha0 = {a0:.4f}, pi-alpha0 = {np.pi-a0:.4f}')
for c in [0.46, 0.49, 0.499]:
    row = []
    for a in [a0, 1.2, np.pi/2, 2.0, np.pi-a0, 2.6, 3.0]:
        row.append(f'{J(a,c,q):+8.3f}')
    print(f'  c={c}: J at [a0,1.2,pi/2,2.0,pi-a0,2.6,3.0] = ' + ' '.join(row))
