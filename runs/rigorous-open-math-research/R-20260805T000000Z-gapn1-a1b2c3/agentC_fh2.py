# -*- coding: utf-8 -*-
"""Debug FH for 2-block HR at single t."""
import numpy as np
from scipy.optimize import brentq

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    return (np.sin(w1*t)/q1)*np.cos(w2*(1-t)) + np.cos(w1*t)*np.sin(w2*(1-t))/q2

def lams1(t, c1, c2, k=2):
    smax = np.pi*np.sqrt(max(c1,c2))*(k+2)+10
    s = np.linspace(1e-8, smax, 40000)
    M = M01_2block(t, c1, c2, s)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0][:k]
    return np.array([brentq(lambda x: M01_2block(t, c1, c2, x), s[idx[j]], s[idx[j]+1]) for j in range(k)])

def f_at(t, c1, c2, s1, s2):
    lam1, lam2 = s1**2, s2**2
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    # unnormalized y(0)=0,y'(0)=1 at x=t, both eigenvalues
    out = []
    for s in (s1, s2):
        w1 = s*q1
        yt = np.sin(w1*t)/q1
        ypt = np.cos(w1*t)
        # full norm on [0,1]
        nrm = 0.0
        nrm += c1*(0.5*(t - np.sin(2*w1*t)/(2*w1)))/q1**2  # B1=1/q1
        w2 = s*q2; L2 = 1-t
        A2, B2 = yt, ypt/w2
        Icc = 0.5*(L2 + np.sin(2*w2*L2)/(2*w2)); Iss = 0.5*(L2 - np.sin(2*w2*L2)/(2*w2)); Ics = np.sin(w2*L2)**2/(2*w2)
        nrm += c2*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
        out.append(yt/np.sqrt(nrm))
    u1, u2 = out
    return lam1*u1**2 - lam2*u2**2

R = 4.0
t = 0.4
h = 1e-6
s_p = lams1(t+h, 1.0, R); s_m = lams1(t-h, 1.0, R)
dD = ((s_p[1]**2-s_p[0]**2) - (s_m[1]**2-s_m[0]**2))/(2*h)
f = f_at(t, 1.0, R, *lams1(t, 1.0, R))
print(f"dD/dt = {dD:.8f}")
print(f"-(R-1)f = {-(R-1)*f:.8f}")
print(f"+(R-1)f = {+(R-1)*f:.8f}")
print(f"f = {f:.8f}")
