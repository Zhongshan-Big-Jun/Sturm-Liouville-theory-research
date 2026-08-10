# -*- coding: utf-8 -*-
"""fast_local.py - cheap local machinery for margin scans (EVIDENCE only).
Reduced grid sizes; ~50x faster than fast_lib for margin scans."""
import numpy as np

def sec(s, a, b, R):
    m = np.sqrt(R); al = s*a; be = s*(1-b); th = s*m*(b-a)
    ca,sa = np.cos(al),np.sin(al); cb,sb = np.cos(be),np.sin(be); ct,st = np.cos(th),np.sin(th)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca

def roots2_fast(a, b, R, ns=401):
    s = np.linspace(1e-9, 3.0*np.pi, ns)
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    if len(idx) >= 2:
        out = []
        for i in idx[:2]:
            lo, hi = s[i], s[i+1]; flo = M[i]
            for _ in range(40):
                md = 0.5*(lo+hi)
                if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
                else: hi = md
            out.append(0.5*(lo+hi))
        return out[0], out[1]
    raise RuntimeError("roots2_fast fail")

def norm_n(s, a, b, R):
    m = np.sqrt(R); Lw = b-a; be = 1-b
    al = s*a; th = s*m*Lw
    I1 = a/2 - np.sin(2*al)/(4*s)
    Icc = Lw/2 + np.sin(2*th)/(4*s*m); Iss = Lw/2 - np.sin(2*th)/(4*s*m)
    Ics = np.sin(th)**2/(2*s*m)
    sa = np.sin(al); ca = np.cos(al)
    I2 = sa*sa*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
    yb = sa*np.cos(th) + (ca/m)*np.sin(th)
    ypb = -m*np.sin(th)*np.sin(al) + np.cos(th)*np.cos(al)
    Icc3 = be/2 + np.sin(2*s*be)/(4*s); Iss3 = be/2 - np.sin(2*s*be)/(4*s)
    Ics3 = np.sin(s*be)**2/(2*s)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/s**2
    return (I1 + R*I2)/s**2 + I3

def R1R2(a, b, R):
    s1, s2 = roots2_fast(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    R1 = s1**2*y1a**2/n1 - s2**2*y2a**2/n2
    return R1
