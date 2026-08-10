# -*- coding: utf-8 -*-
"""dbg_e1left.py - EVIDENCE: E1-left margin: R1(b0,b0,eps) sign and size."""
import mpmath as mp
import numpy as np
mp.mp.dps = 45
pi = mp.pi
a0 = mp.acos(mp.mpf(1)/4)/pi
b0 = 1 - a0

def sec_mp(s, a, b, eps):
    q = mp.sqrt(1+eps)
    al = s*a; be = s*(1-b); th = q*s*(b-a)
    return (mp.cos(be)*mp.cos(th)*mp.sin(al) - q*mp.sin(be)*mp.sin(th)*mp.sin(al)
            + (mp.cos(be)*mp.sin(th)/q)*mp.cos(al) + mp.sin(be)*mp.cos(th)*mp.cos(al))
def norm_mp(s, a, b, eps):
    q = mp.sqrt(1+eps); Lw = b-a; be = 1-b
    al = s*a; th = q*s*Lw
    I1 = a/2 - mp.sin(2*al)/(4*s)
    Icc = Lw/2 + mp.sin(2*th)/(4*q*s); Iss = Lw/2 - mp.sin(2*th)/(4*q*s)
    Ics = mp.sin(th)**2/(2*q*s)
    sa, ca = mp.sin(al), mp.cos(al)
    I2 = sa**2*Icc + (ca/q)**2*Iss + 2*sa*(ca/q)*Ics
    yb = sa*mp.cos(th) + (ca/q)*mp.sin(th)
    ypb = -q*mp.sin(th)*sa + mp.cos(th)*ca
    Icc3 = be/2 + mp.sin(2*s*be)/(4*s); Iss3 = be/2 - mp.sin(2*s*be)/(4*s)
    Ics3 = mp.sin(s*be)**2/(2*s)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/s**2
    return (I1 + q**2*I2)/s**2 + I3
def root_mp(k, a, b, eps):
    return mp.findroot(lambda s: sec_mp(s, a, b, eps), k*pi, tol=1e-45, maxsteps=80)
def f_at(a, b, eps):
    s1 = root_mp(1, a, b, eps); s2 = root_mp(2, a, b, eps)
    n1 = norm_mp(s1, a, b, eps); n2 = norm_mp(s2, a, b, eps)
    y1a = mp.sin(s1*a)/s1; y2a = mp.sin(s2*a)/s2
    return s1**2*y1a**2/n1 - s2**2*y2a**2/n2

def fconst(x):
    return 2*pi**2*(mp.sin(pi*x)**2 - 4*mp.sin(2*pi*x)**2)

print("f_const(b0) = %.6e" % fconst(b0))
for eps in (0.0, 1e-3, 1e-2, 0.02, 0.05, 0.1):
    v = f_at(b0, b0, eps)
    print("eps=%.3f: R1(b0,b0,eps) = %.6f" % (eps, v))
# first-order coefficient
r11 = float(mp.diff(lambda e: f_at(b0, b0, e), 0, 1))
print("R1_1(b0,b0) = %.6f" % r11)
print("prediction eps*R1_1: 0.05*R1_1 = %.4f" % (0.05*r11))
# h(a0) direct: A_eps(b0) - b0
from fast_lib import R1R2
a0n = float(a0)
for eps in (1e-3, 1e-2, 0.05):
    lo, hi = a0n-0.02, a0n+0.02
    for _ in range(70):
        md = 0.5*(lo+hi)
        if np.signbit(R1R2(md, b0, 1+eps)[0]) == np.signbit(R1R2(lo, b0, 1+eps)[0]): lo = md
        else: hi = md
    A = 0.5*(lo+hi)
    print("eps=%.3f: A_eps(b0)=%.8f  h(a0)=A-b0=%.6f" % (eps, A, A-b0))
