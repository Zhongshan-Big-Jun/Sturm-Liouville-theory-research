# -*- coding: utf-8 -*-
"""Sign of f(t) = lam1*u1^2 - lam2*u2^2 and dD/dt on fine grids; wiggle detection.
Fast: phase-coordinate eigenvalues + closed-form L2(rho) norms (y'(0)=1)."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def xk(mu, c, k):
    return brentq(lambda x: theta(x, mu) + c*x - k*np.pi, 0.0, k*np.pi)

def lams(t, c1, c2):
    # two-block densities (c1 on [0,t], c2 on (t,1]): x = s*sqrt(c1)*t
    mu = np.sqrt(c2/c1)
    c = mu*(1.0-t)/t
    x1, x2 = xk(mu, c, 1), xk(mu, c, 2)
    return x1/(np.sqrt(c1)*t), x2/(np.sqrt(c1)*t)

def norm2(t, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    w1 = s*q1
    yt = np.sin(w1*t)/w1
    ypt = np.cos(w1*t)
    nrm = c1*(0.5*(t - np.sin(2*w1*t)/(2*w1)))/w1**2
    w2 = s*q2; L2 = 1-t
    A2, B2 = yt, ypt/w2
    Icc = 0.5*(L2 + np.sin(2*w2*L2)/(2*w2)); Iss = 0.5*(L2 - np.sin(2*w2*L2)/(2*w2)); Ics = np.sin(w2*L2)**2/(2*w2)
    nrm += c2*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
    return nrm

def f_correct(t, c1, c2, s1, s2):
    out = []
    for s in (s1, s2):
        w1 = s*np.sqrt(c1)
        yt = np.sin(w1*t)/w1
        out.append(yt/np.sqrt(norm2(t, c1, c2, s)))
    return s1**2*out[0]**2 - s2**2*out[1]**2

for R in [1.5, 2.0, 4.0, 10.0, 100.0]:
    for hl in [False, True]:
        c1, c2 = (R, 1.0) if hl else (1.0, R)
        n = 2000
        ts = np.linspace(1e-4, 1-1e-4, n)
        fs = np.zeros(n); Ds = np.zeros(n)
        for i, t in enumerate(ts):
            s1, s2 = lams(t, c1, c2)
            Ds[i] = s2**2 - s1**2
            fs[i] = f_correct(t, c1, c2, s1, s2)
        sgf = np.signbit(fs)
        nsc = int((sgf[1:] != sgf[:-1]).sum())
        dD = np.diff(Ds)
        sgdd = np.signbit(dD)
        nscD = int((sgdd[1:] != sgdd[:-1]).sum())
        print(f"R={R:6.1f} {'HL' if hl else 'HR'}: f sign changes={nsc}, dD/dt sign changes={nscD}, "
              f"D[min]={Ds.min():.6f}, D[max]={Ds.max():.6f}, f(t=eps)={fs[0]:+.3e}, f(t=1-eps)={fs[-1]:+.3e}")
