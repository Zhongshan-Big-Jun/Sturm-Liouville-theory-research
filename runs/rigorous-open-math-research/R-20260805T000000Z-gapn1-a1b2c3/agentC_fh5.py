# -*- coding: utf-8 -*-
"""Fixed FH check: y = sin(sx)/s on [0,t] (y'(0)=1); correct C^1 matching.
D computed via the phase-coordinate solver (independent of M01)."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def F(x, mu, c):
    return theta(x, mu) + c*x

def xk(mu, c, k):
    return brentq(lambda x: F(x, mu, c) - k*np.pi, 0.0, k*np.pi)

def lams(t, c1, c2):
    # HR two-block: rho = c1 on [0,t], c2 on (t,1]; s = x/t (for c1=1)
    mu = np.sqrt(c2/c1)
    c = mu*(1.0-t)/t
    x1 = xk(mu, c, 1); x2 = xk(mu, c, 2)
    return x1*(mu+c)/mu, x2*(mu+c)/mu

def norm2_correct(t, c1, c2, s):
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
    lam1, lam2 = s1**2, s2**2
    out = []
    for s in (s1, s2):
        w1 = s*np.sqrt(c1)
        yt = np.sin(w1*t)/w1
        nrm = norm2_correct(t, c1, c2, s)
        out.append(yt/np.sqrt(nrm))
    return lam1*out[0]**2 - lam2*out[1]**2

print("== FH dD/dt = -(R-1) f, HR ==")
for R in [2.0, 4.0]:
    ts = np.linspace(0.05, 0.95, 200)
    h = 1e-6
    worst = 0.0
    for tt in ts:
        sp = lams(tt+h, 1.0, R); sm = lams(tt-h, 1.0, R)
        dD = ((sp[1]**2-sp[0]**2) - (sm[1]**2-sm[0]**2))/(2*h)
        s0, s1 = lams(tt, 1.0, R)
        f = f_correct(tt, 1.0, R, s0, s1)
        worst = max(worst, abs(dD + (R-1)*f))
    print(f"  R={R}: max |dD/dt + (R-1)f| = {worst:.3e}")
