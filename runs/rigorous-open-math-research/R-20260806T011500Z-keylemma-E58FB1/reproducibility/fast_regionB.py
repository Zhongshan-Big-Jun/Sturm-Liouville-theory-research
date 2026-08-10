# -*- coding: utf-8 -*-
"""fast_regionB.py -- float64 (numpy/scipy) verification of Region B structure."""
import numpy as np
from scipy.optimize import brentq

def Phi(a, q): return np.cos(a)**2 + q*q*np.sin(a)**2
def Wfun(a): return 3 + 2*a/np.tan(a)
def E_curve(a, q): return np.arctan(1.0/(q*np.tan(a)))
def O_curve(a, q):
    a = np.asarray(a, dtype=float); out = np.empty_like(a)
    hi = a > np.pi/2
    eq = a == np.pi/2
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
def cG2(q):
    if Gfun(alpha2(0.5,q),0.5,q) >= 0: return None
    return brentq(lambda c: Gfun(alpha2(c,q),c,q), 0.40, 0.5)

print('=== boundary c=1/2 ===')
for q in [1.001, 1.1, 1.3, 1.5, 1.7, 1.85, 2.0, 3.0, 10.0]:
    fp = Fp(0.5, q); h = H(0.5, q)
    cfH = 2*np.pi*q*(q+1)/(2*q+1)**1.5
    print(f'  q={q:<6}: -Fp(1/2)={-fp:+.6f}  H(1/2)={h:+.6f}  formula={cfH:+.6f}  diff={abs(h-cfH):.2e}')

print()
print('=== Region B grids: J1, J2, Fpp, dH/dc ===')
for q in [1.0, 1.1, 1.3, 1.5, 1.7, 1.8]:
    cb = cG2(q)
    if cb is None:
        print(f'  q={q}: Region B empty'); continue
    cs = np.linspace(cb, 0.5, 15)
    j1m=1e9; j2x=-1e9; fppm=1e9; dHx=-1e9; fpm=1e9; hm=1e9
    for c in cs:
        a1=alpha1(c,q); a2=alpha2(c,q)
        j1=J(a1,c,q); j2=J(a2,c,q)
        h=1e-5
        fpp=(Fp(c+h,q)-2*Fp(c,q)+Fp(c-h,q))/h**2
        dH=(H(c+h,q)-H(c-h,q))/(2*h)
        j1m=min(j1m,j1); j2x=max(j2x,j2); fppm=min(fppm,fpp); dHx=max(dHx,dH)
        fpm=min(fpm,-Fp(c,q)); hm=min(hm,H(c,q))
    print(f'  q={q:<4}: cB={cb:.4f} minJ1={j1m:+.3f} maxJ2={j2x:+.3f} minFpp={fppm:+.3f} maxdH/dc={dHx:+.3f} min(-Fp)={fpm:+.3f} minH={hm:+.3f}')
