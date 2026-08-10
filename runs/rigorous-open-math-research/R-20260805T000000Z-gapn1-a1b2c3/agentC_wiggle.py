# -*- coding: utf-8 -*-
"""Wiggle structure: interior local extrema of D(t) for HR two-block.
D has exactly one interior local max and one local min (the two zeros of
f(t) = lam1*u1^2 - lam2*u2^2; dD/dt = -(R-1)*f).  Both lie strictly inside
(3*pi^2/R, 3*pi^2).  Fast phase-coordinate solver for the eigenvalues."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def xk(mu, c, k):
    # F = theta + c*x strictly increasing, F(0)=0, F(k*pi) > k*pi
    return brentq(lambda x: theta(x, mu) + c*x - k*np.pi, 0.0, k*np.pi)

def lams(t, R):
    mu = np.sqrt(R)
    c = mu*(1.0-t)/t
    x1, x2 = xk(mu, c, 1), xk(mu, c, 2)
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

def f_correct(t, R):
    s1, s2 = lams(t, R)
    out = []
    for s in (s1, s2):
        w1 = s
        yt = np.sin(w1*t)/w1
        nrm = norm2_correct(t, 1.0, R, s)
        out.append(yt/np.sqrt(nrm))
    return s1**2*out[0]**2 - s2**2*out[1]**2

PI2 = np.pi**2
for R in [1.5, 2.0, 4.0, 10.0, 100.0]:
    ts = np.linspace(0.01, 0.99, 6000)
    fs = np.array([f_correct(t, R) for t in ts])
    sg = np.signbit(fs); ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0]
    zs = [brentq(lambda t: f_correct(t, R), ts[i], ts[i+1]) for i in idx]
    s1, s2 = lams(zs[0], R); Dmax = s2**2 - s1**2
    s1, s2 = lams(zs[1], R); Dmin = s2**2 - s1**2
    print(f"R={R}: f zeros at t = {[round(z,4) for z in zs]}, "
          f"D max={Dmax:.4f} at t={zs[0]:.4f}, D min={Dmin:.4f} at t={zs[1]:.4f}, "
          f"bounds ({3*PI2/R:.4f}, {3*PI2:.4f})")
