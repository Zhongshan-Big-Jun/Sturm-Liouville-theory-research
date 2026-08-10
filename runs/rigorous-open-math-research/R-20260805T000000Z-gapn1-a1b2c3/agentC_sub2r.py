# -*- coding: utf-8 -*-
"""Subclaim 2 R->inf: fixed root scanning."""
import numpy as np
from scipy.optimize import brentq

def sec_DN(u, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    a = s*q1*u; b = s*q2*(0.5-u)
    return np.cos(a)*np.cos(b)/q2 - np.sin(a)*np.sin(b)/q1

def sec_DD(u, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    a = s*q1*u; b = s*q2*(0.5-u)
    return np.sin(a)*np.cos(b)/q1 + np.cos(a)*np.sin(b)/q2

def first_root(u, c1, c2, which):
    f = (lambda s: sec_DN(u,c1,c2,s)) if which=='DN' else (lambda s: sec_DD(u,c1,c2,s))
    smax = np.pi*np.sqrt(max(c1,c2))*2 + 5
    g = np.linspace(1e-8, smax, 200000)
    v = np.array([f(ss) for ss in g])
    sg = np.signbit(v)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    if len(idx) == 0:
        raise RuntimeError("no root")
    j = idx[0]
    return brentq(f, g[j], g[j+1])

def roots_half(u, c1, c2):
    return first_root(u, c1, c2, 'DN'), first_root(u, c1, c2, 'DD')

def half_norm(u, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    w1 = q1*s; L1 = u
    nrm = c1*(0.5*(L1 - np.sin(2*w1*L1)/(2*w1)))/w1**2
    a = q1*s*u
    yt = np.sin(a)/(q1*s); ypt = np.cos(a)
    w2 = q2*s; L2 = 0.5-u
    A2, B2 = yt, ypt/w2
    Icc = 0.5*(L2 + np.sin(2*w2*L2)/(2*w2)); Iss = 0.5*(L2 - np.sin(2*w2*L2)/(2*w2)); Ics = np.sin(w2*L2)**2/(2*w2)
    nrm += c2*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
    return nrm

def f_u(u, c1, c2):
    s0, s1 = roots_half(u, c1, c2)
    N0 = half_norm(u, c1, c2, s0); N1 = half_norm(u, c1, c2, s1)
    q1 = np.sqrt(c1)
    y0 = np.sin(q1*s0*u)/(q1*s0); y1 = np.sin(q1*s1*u)/(q1*s1)
    return s0**2*y0**2/(2*N0) - s1**2*y1**2/(2*N1)

def ustar(R, sup, npts=400):
    c1, c2 = (1.0, R) if sup else (R, 1.0)
    uu = np.linspace(1e-6, 0.5-1e-6, npts)
    ff = np.array([f_u(u, c1, c2) for u in uu])
    sg = np.signbit(ff)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    return [brentq(lambda u: f_u(u, c1, c2), uu[i], uu[i+1]) for i in idx]

print("R -> inf: D_SUP -> 4 pi^2 =", 4*np.pi**2, "; D_INF*R -> 24.943866...")
for R in [1e2, 1e4, 1e6]:
    us = ustar(R, True)[0]
    s0, s1 = roots_half(us, 1.0, R)
    Dsup = s1**2 - s0**2
    ui = ustar(R, False)[0]
    t0, t1 = roots_half(ui, R, 1.0)
    Dinf = t1**2 - t0**2
    print(f"  R={R:8.0f}: SUP u*={us:.7f} D_SUP={Dsup:.7f} (4pi^2-D={4*np.pi**2-Dsup:+.3e}) | INF u*={ui:.7f} D_INF*R={Dinf*R:.7f} u={ui:.7f}")
