# -*- coding: utf-8 -*-
"""verify_Fp12.py -- verify closed form Fp(q,1/2) = -pi s co P(x)/(...) formula."""
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
def Fp(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mtil(a1,c,q)*Gfun(a1,c,q)-Mtil(a2,c,q)*Gfun(a2,c,q)

print('=== verify closed form Fp(q,1/2) ===')
for q in [1.001, 1.1, 1.3, 1.5, 1.8, 2.0, 10.0]:
    x = 2*np.arcsin(1/np.sqrt(2*(q+1)))
    s, co = np.sin(x), np.cos(x)
    qc = co/(1-co)
    Ph = -2*co*co/(co-1)
    D = s*s*co/(co-1)**2
    P = 3*x*x + 6*x*s - 3*np.pi*x - 3*np.pi*s + np.pi*np.pi
    N = -np.pi*P*s*co/(co-1)**2
    Fp12_formula = N*s*s*Ph/D**3
    Fp12_num = Fp(0.5, q)
    print(f'  q={q:<6}: formula={Fp12_formula:+.9f}  numeric={Fp12_num:+.9f}  diff={abs(Fp12_formula-Fp12_num):.1e}  P={P:+.6f}')
print()
print('=== dG\'/dalpha on (0, pi): check G\' decreasing in alpha ===')
for q in [1.1, 1.5, 2.0, 10.0]:
    for c in [0.2, 0.4, 0.49]:
        h = 1e-5
        mn = 1e9; mx=-1e9
        for k in range(1, 100):
            a = np.pi*k/100
            d = (Gprime(a+h,c,q)-Gprime(a-h,c,q))/(2*h)
            mn=min(mn,d); mx=max(mx,d)
        print(f'  q={q:<5} c={c:.2f}: dG\'/da in [{mn:+.4f}, {mx:+.4f}]')
