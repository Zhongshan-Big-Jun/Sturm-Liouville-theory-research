# -*- coding: utf-8 -*-
"""qmono.py -- check d/dq of J1, J2, Fpp, -Hp on Region B and full domain."""
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
def Fp(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mtil(a1,c,q)*Gfun(a1,c,q)-Mtil(a2,c,q)*Gfun(a2,c,q)
def Fpp(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mtil(a1,c,q)*J(a1,c,q) - Mtil(a2,c,q)*J(a2,c,q)
def Hp(c,q):
    h=1e-5
    def H(cc): return Gfun(alpha2(cc,q),cc,q)-Gfun(alpha1(cc,q),cc,q)
    return (H(c+h)-H(c-h))/(2*h)

def cG2(q):
    if Gfun(alpha2(0.5,q),0.5,q) >= 0: return None
    return brentq(lambda c: Gfun(alpha2(c,q),c,q), 0.40, 0.5)

h = 1e-4
print('=== d/dq on Region B: J1, J2, Fpp, -Hp ===')
for q in [1.05, 1.3, 1.5, 1.7, 1.8]:
    cb = cG2(q)
    if cb is None: continue
    worst = [1e9]*4; worstc=[None]*4
    for k in range(9):
        c = cb + (0.5-cb)*k/8
        a1=alpha1(c,q); a2=alpha2(c,q)
        dJ1 = (J(a1,c,q+h)-J(a1,c,q-h))/(2*h)
        dJ2 = (J(a2,c,q+h)-J(a2,c,q-h))/(2*h)
        dFpp = (Fpp(c,q+h)-Fpp(c,q-h))/(2*h)
        dHp = (Hp(c,q+h)-Hp(c,q-h))/(2*h)
        for i, v in enumerate([dJ1, dJ2, dFpp, dHp]):
            if v < worst[i]: worst[i], worstc[i] = v, c
    print(f'  q={q:<5}: min dJ1/dq={worst[0]:+9.3f}@c={worstc[0]:.3f} | max dJ2/dq={worst[1]:+9.3f}@c={worstc[1]:.3f} | min dFpp/dq={worst[2]:+9.3f}@c={worstc[2]:.3f} | max dHp/dq={worst[3]:+9.3f}@c={worstc[3]:.3f}')
