# -*- coding: utf-8 -*-
"""dbg_R1b_decomp.py - decompose R1_b = eps*D1b + eps^2*D2b + ... at the sheet, b near 1."""
import mpmath as mp
import numpy as np
mp.mp.dps = 50
pi = mp.pi
a0n = float(mp.acos(mp.mpf(1)/4)/pi)

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

def D1b(a, b):  # d/db of first-order coefficient
    return float(mp.diff(lambda e: mp.diff(lambda bb: f_at(a, bb, e), b, 1), 0, 1))
def D2b(a, b):
    return float(mp.diff(lambda e: mp.diff(lambda bb: f_at(a, bb, e), b, 1), 0, 2))

for b in (0.9, 0.99, 0.999, 0.9999, 0.99999):
    a_s = a0n + 0.13*0.1  # approximate sheet a for eps=0.1; refine below
    # find sheet a at eps=0.1
    from fast_lib import R1R2
    lo, hi = a0n-0.01, a0n+0.02
    for _ in range(60):
        md = 0.5*(lo+hi)
        if np.signbit(R1R2(md, b, 1.1)[0]) == np.signbit(R1R2(lo, b, 1.1)[0]): lo = md
        else: hi = md
    a_s = 0.5*(lo+hi)
    d1 = D1b(a_s, b); d2 = D2b(a_s, b)
    # R1_b at eps=0.1 and eps=0.02
    rb1 = float(mp.diff(lambda bb: f_at(a_s, bb, 0.1), b, 1))
    rb2 = float(mp.diff(lambda bb: f_at(a_s, bb, 0.02), b, 1))
    print("b=%.5f a=%.6f  D1b=%.6e  D2b=%.4e  R1_b(0.1)=%.3e  R1_b(0.02)=%.3e"
          % (b, a_s, d1, d2, rb1, rb2))
    print("   check: 0.1*D1b+0.01*D2b = %.3e vs R1_b(0.1)=%.3e" % (0.1*d1+0.01*d2, rb1))
