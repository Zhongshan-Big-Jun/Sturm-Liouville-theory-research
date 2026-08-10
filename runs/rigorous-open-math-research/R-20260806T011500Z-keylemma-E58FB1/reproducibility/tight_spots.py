# -*- coding: utf-8 -*-
"""tight_spots.py -- where are dJ1/dq, dJ2/dq, dHp/dq tight on (1,2]x[0.4,0.5]?"""
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
def Hp(c,q):
    hh=1e-5
    return (H(c+hh,q)-H(c-hh,q))/(2*hh)

h = 1e-4
mnJ1=(1e9,None); mxJ2=(-1e9,None); mxHp=(-1e9,None)
for qi in range(1, 41):
    q = 1.0 + qi/40
    for k in range(1, 21):
        c = 0.4 + 0.1*k/20
        a1=alpha1(c,q); a2=alpha2(c,q)
        dJ1 = (J(a1,c,q+h)-J(a1,c,q-h))/(2*h)
        dJ2 = (J(a2,c,q+h)-J(a2,c,q-h))/(2*h)
        dHp = (Hp(c,q+h)-Hp(c,q-h))/(2*h)
        if dJ1 < mnJ1[0]: mnJ1 = (dJ1, (round(q,3), round(c,3)))
        if dJ2 > mxJ2[0]: mxJ2 = (dJ2, (round(q,3), round(c,3)))
        if dHp > mxHp[0]: mxHp = (dHp, (round(q,3), round(c,3)))
print('min dJ1/dq =', mnJ1)
print('max dJ2/dq =', mxJ2)
print('max dHp/dq =', mxHp)
