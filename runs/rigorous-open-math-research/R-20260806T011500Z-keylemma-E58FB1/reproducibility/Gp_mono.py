# -*- coding: utf-8 -*-
"""Gp_mono.py -- dG'/dalpha on (alpha0, pi-alpha0) for all c in (0,1/2), various q."""
import numpy as np

def Phi(a, q): return np.cos(a)**2 + q*q*np.sin(a)**2
def Wfun(a): return 3 + 2*a/np.tan(a)
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

h = 1e-5
print('=== max dG\'/da on (alpha0+eps, pi-alpha0-eps) over c in (0.05,0.5), q grid ===')
for q in [1.01, 1.1, 1.5, 2.0, 3.0, 10.0, 100.0]:
    a0 = 2*np.arcsin(1/np.sqrt(2*(q+1)))
    worst = -1e9; arg=None
    for c in np.linspace(0.05, 0.499, 12):
        for k in range(1, 60):
            a = a0 + (np.pi-2*a0)*k/60
            if abs(a - np.pi/2) < 0.05:  # skip tiny neighborhood of pi/2 (FD endpoint effects)
                continue
            d = (Gprime(a+h,c,q)-Gprime(a-h,c,q))/(2*h)
            if d > worst: worst, arg = d, (c, a)
    print(f'  q={q:<6}: max dG\'/da = {worst:+.4f} at {arg}')
