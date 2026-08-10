# -*- coding: utf-8 -*-
"""wide_mono.py -- q-monotonicity on wide grid; R2 check (G2>=0 for c<=0.4)."""
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
def H(c,q):
    return Gfun(alpha2(c,q),c,q)-Gfun(alpha1(c,q),c,q)

h = 1e-4
print('=== dJ1/dq, dJ2/dq, dHp/dq on wide grid (q,c) ===')
worst = {'dJ1': 1e9, 'dJ2': -1e9, 'dHp': -1e9}
for q in [1.01, 1.1, 1.5, 2.0, 3.0, 5.0, 10.0, 50.0]:
    for c in [0.05, 0.1, 0.2, 0.3, 0.4, 0.45, 0.49]:
        a1=alpha1(c,q); a2=alpha2(c,q)
        dJ1 = (J(a1,c,q+h)-J(a1,c,q-h))/(2*h)
        dJ2 = (J(a2,c,q+h)-J(a2,c,q-h))/(2*h)
        def Hp(cc, qq):
            hh=1e-5
            return (H(cc+hh,qq)-H(cc-hh,qq))/(2*hh)
        dHp = (Hp(c,q+h)-Hp(c,q-h))/(2*h)
        worst['dJ1'] = min(worst['dJ1'], dJ1)
        worst['dJ2'] = max(worst['dJ2'], dJ2)
        worst['dHp'] = max(worst['dHp'], dHp)
        if dJ1 < 0 or dJ2 > 0 or dHp > 0:
            print(f'  VIOLATION q={q} c={c}: dJ1={dJ1:+.3f} dJ2={dJ2:+.3f} dHp={dHp:+.3f}')
print(f'worst: dJ1 min={worst["dJ1"]:+.3f}  dJ2 max={worst["dJ2"]:+.3f}  dHp max={worst["dHp"]:+.3f}')

print()
print('=== R2: G2 >= 0 for c <= 0.4, q in (1, 100]? ===')
mn = 1e9; arg=None
for q in [1.001, 1.01, 1.1, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0]:
    for c in np.linspace(0.001, 0.4, 81):
        a2 = alpha2(c,q)
        g2 = Gfun(a2,c,q)
        if g2 < mn: mn, arg = g2, (q, c)
print(f'  min G2 for c<=0.4 = {mn:+.6f} at {arg}')
