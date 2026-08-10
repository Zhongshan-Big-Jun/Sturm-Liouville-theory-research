# -*- coding: utf-8 -*-
"""fast_lib.py: fast eigenvalue/residual library for this run."""
import numpy as np

def sec(s, a, b, R):
    m = np.sqrt(R); al = s*a; be = s*(1-b); th = s*m*(b-a)
    ca,sa = np.cos(al),np.sin(al); cb,sb = np.cos(be),np.sin(be); ct,st = np.cos(th),np.sin(th)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca

def roots2_fast(a, b, R, ns=2001, caps=(3.0*np.pi, 6.0*np.pi, 10.0*np.pi, 16.0*np.pi)):
    for cap in caps:
        s = np.linspace(1e-9, cap, ns)
        M = sec(s, a, b, R)
        ch = np.signbit(M[1:]) != np.signbit(M[:-1])
        idx = np.nonzero(ch)[0]
        if len(idx) >= 2:
            out = []
            for i in idx[:2]:
                lo, hi = s[i], s[i+1]; flo = M[i]
                for _ in range(45):
                    md = 0.5*(lo+hi)
                    if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
                    else: hi = md
                out.append(0.5*(lo+hi))
            return out[0], out[1]
    raise RuntimeError(f"roots2_fast fail (a,b,R)=({a},{b},{R})")

def y_at(s, a, b, R, x):
    m = np.sqrt(R)
    if x <= a:
        return np.sin(s*x)/s
    u = x - a
    if x <= b:
        return (np.sin(s*a)*np.cos(s*m*u) + (np.cos(s*a)/m)*np.sin(s*m*u))/s
    v = x - b
    th = s*m*(b-a)
    yb = (np.sin(s*a)*np.cos(th) + (np.cos(s*a)/m)*np.sin(th))/s
    ypb = -m*np.sin(th)*np.sin(s*a) + np.cos(th)*np.cos(s*a)
    return np.cos(s*v)*yb + np.sin(s*v)*ypb/s

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

def cfg(a, b, R):
    s1, s2 = roots2_fast(a, b, R)
    return s1, s2, norm_n(s1, a, b, R), norm_n(s2, a, b, R)

def R1R2(a, b, R, c=None):
    if c is None: c = cfg(a, b, R)
    s1, s2, n1, n2 = c
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    R1 = s1**2*y1a**2/n1 - s2**2*y2a**2/n2
    R2 = s1**2*y1b**2/n1 - s2**2*y2b**2/n2
    return R1, R2

def vratio(a, b, R):
    s1, s2 = roots2_fast(a, b, R)
    return (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1)
