# -*- coding: utf-8 -*-
"""map_structure.py -- sign map of J1, J2, Fpp, Hp over (q,c) grid."""
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
def H(c,q):
    return Gfun(alpha2(c,q),c,q)-Gfun(alpha1(c,q),c,q)

qs = [1.01, 1.1, 1.3, 1.5, 1.8, 2.0, 3.0, 10.0]
cs = np.linspace(0.05, 0.495, 20)
print('q     c      J1      J2      Fpp(=M1J1-M2J2)   Hp      H      -Fp')
for q in qs:
    for c in cs:
        a1=alpha1(c,q); a2=alpha2(c,q)
        j1=J(a1,c,q); j2=J(a2,c,q)
        fpp = Mtil(a1,c,q)*j1 - Mtil(a2,c,q)*j2
        h=1e-5
        hp = (H(c+h,q)-H(c-h,q))/(2*h)
        Hv = H(c,q); mfp = -Fp(c,q)
        flag = ''
        if j1 < 0: flag += ' J1<0!'
        if j2 > 0: flag += ' J2>0!'
        if fpp < 0: flag += ' Fpp<0!'
        if hp > 0: flag += ' Hp>0!'
        if Hv < 0: flag += ' H<0!'
        if mfp < 0: flag += ' Fp>0!'
        if flag:
            print(f'{q:<5} {c:.3f} {j1:+8.3f} {j2:+8.3f} {fpp:+9.3f} {hp:+8.3f} {Hv:+7.3f} {mfp:+7.3f}{flag}')
print('(only lines with violations shown)')
