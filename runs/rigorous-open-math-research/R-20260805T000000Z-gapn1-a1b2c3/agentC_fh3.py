# -*- coding: utf-8 -*-
"""Debug FH per eigenvalue."""
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

def norm2_rho(t, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    w1 = s*q1
    nrm = c1*(0.5*(t - np.sin(2*w1*t)/(2*w1)))/q1**2
    yt = np.sin(w1*t)/q1; ypt = np.cos(w1*t)
    w2 = s*q2; L2 = 1-t
    A2, B2 = yt, ypt/w2
    Icc = 0.5*(L2 + np.sin(2*w2*L2)/(2*w2)); Iss = 0.5*(L2 - np.sin(2*w2*L2)/(2*w2)); Ics = np.sin(w2*L2)**2/(2*w2)
    nrm += c2*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
    return nrm

R = 4.0; t = 0.4; h = 1e-7
for k, which in [(0,'lam1'), (1,'lam2')]:
    s_p = lams1(t+h, 1.0, R); s_m = lams1(t-h, 1.0, R)
    dlam = ((s_p[k]**2) - (s_m[k]**2))/(2*h)
    s = lams1(t, 1.0, R)[k]
    lam = s**2
    q1 = np.sqrt(1.0)
    w1 = s*q1
    yt = np.sin(w1*t)/q1
    nrm = norm2_rho(t, 1.0, R, s)
    u = yt/np.sqrt(nrm)
    fh = (R-1)*lam*u**2
    print(f"{which}: dlam/dt = {dlam:.8f}   (R-1)lam u(t)^2 = {fh:.8f}   diff = {dlam-fh:.4e}")
