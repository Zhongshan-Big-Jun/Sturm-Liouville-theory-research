# -*- coding: utf-8 -*-
"""check_Fpp.py -- verify Fpp == M1t*J1 - M2t*J2 by finite differences; check J signs."""
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
def M1t(c,q): return Mtil(alpha1(c,q),c,q)
def M2t(c,q): return Mtil(alpha2(c,q),c,q)

q = 1.3
for c in [0.475, 0.49, 0.499]:
    h = 1e-5
    fpp_fd = (Fp(c+h,q)-2*Fp(c,q)+Fp(c-h,q))/h**2
    a1=alpha1(c,q); a2=alpha2(c,q)
    m1=M1t(c,q); m2=M2t(c,q)
    j1=J(a1,c,q); j2=J(a2,c,q)
    ident = m1*j1 - m2*j2
    print(f'c={c}: Fpp_fd={fpp_fd:+.6f}  M1J1-M2J2={ident:+.6f}  diff={abs(fpp_fd-ident):.2e}')
    print(f'     J1={j1:+.6f}  J2={j2:+.6f}  M1={m1:.4f} M2={m2:.4f}')
    # verify Gprime == finite diff of G along curve
    a1p=alpha1(c+h,q); a1m=alpha1(c-h,q)
    g_fd = (Gfun(a1p,c+h,q)-Gfun(a1m,c-h,q))/(2*h)
    print(f'     G1prime_fd={g_fd:+.6f}  G1prime_formula={Gprime(a1,c,q):+.6f}')
