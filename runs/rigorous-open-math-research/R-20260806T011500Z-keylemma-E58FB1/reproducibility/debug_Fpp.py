# -*- coding: utf-8 -*-
"""debug_Fpp.py -- trace the Fpp identity failure."""
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

q = 1.3; c = 0.49
h = 1e-6
a1=alpha1(c,q); a2=alpha2(c,q)
M1 = Mtil(a1,c,q); M2 = Mtil(a2,c,q)
G1 = Gfun(a1,c,q); G2 = Gfun(a2,c,q)
print('M1 =', M1, ' M2 =', M2)
print('G1 =', G1, ' G2 =', G2)
print('M1*G1 - M2*G2 =', M1*G1 - M2*G2)

# FD of M1(c) itself
a1p = alpha1(c+h,q); a1m = alpha1(c-h,q)
M1p = Mtil(a1p,c+h,q); M1m = Mtil(a1m,c-h,q)
dM1_fd = (M1p-M1m)/(2*h)
print('dM1/dc FD =', dM1_fd, '  M1*G1 =', M1*G1)

# FD of G1
dG1_fd = (Gfun(a1p,c+h,q)-Gfun(a1m,c-h,q))/(2*h)
print('dG1/dc FD =', dG1_fd, '  Gprime formula =', Gprime(a1,c,q))

# d/dc(M1 G1) FD
dM1G1_fd = (M1p*Gfun(a1p,c+h,q) - M1m*Gfun(a1m,c-h,q))/(2*h)
print('d(M1G1)/dc FD =', dM1G1_fd, '  M1*J1 =', M1*J(a1,c,q))

# Fp and its FD
def Fp(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mtil(a1,c,q)*Gfun(a1,c,q)-Mtil(a2,c,q)*Gfun(a2,c,q)
fp = Fp(c,q)
fpp_fd = (Fp(c+h,q)-2*fp+Fp(c-h,q))/h**2
print('Fp =', fp)
print('Fpp FD =', fpp_fd)
print('M1J1-M2J2 =', M1*J(a1,c,q) - M2*J(a2,c,q))
# direct: d(Fp)/dc FD
dFp_fd = (Fp(c+h,q)-Fp(c-h,q))/(2*h)
print('dFp/dc FD =', dFp_fd)
