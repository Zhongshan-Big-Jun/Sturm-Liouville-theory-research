# -*- coding: utf-8 -*-
"""Agent C: verify FH derivative dD/dt = (R-1)*f(t) and f-sign near t=1."""
import numpy as np
from scipy.optimize import brentq

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    B = np.sin(w1*t)/q1; Dm = np.cos(w1*t)
    E = np.cos(w2*(1-t)); F = np.sin(w2*(1-t))/q2
    return E*B + F*Dm

def lams_2block(t, c1, c2, k=2):
    smax = np.pi*np.sqrt(max(c1, c2))*(k+2)+10
    s = np.linspace(1e-9, smax, 120000)
    d = np.array([M01_2block(t, c1, c2, x) for x in s])
    sg = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(sg)[0]
    roots = []
    for i in idx[:k]:
        roots.append(brentq(lambda x: M01_2block(t, c1, c2, x), s[i], s[i+1]))
    return np.array(roots)

def eig_at(t, c1, c2, s_vals, x):
    out = []
    for s in s_vals:
        w1 = s*np.sqrt(c1); q1 = np.sqrt(c1)
        M1 = np.array([[np.cos(w1*t), np.sin(w1*t)/q1], [-q1*np.sin(w1*t), np.cos(w1*t)]])
        if x <= t:
            y, yp = M1[0,1], M1[1,1]
        else:
            w2 = s*np.sqrt(c2); q2 = np.sqrt(c2); d = x - t
            M2 = np.array([[np.cos(w2*d), np.sin(w2*d)/q2], [-q2*np.sin(w2*d), np.cos(w2*d)]])
            Mt = M2 @ M1
            y, yp = Mt[0,1], Mt[1,1]
        nrm = 0.0
        A1, B1 = 0.0, 1.0/q1
        Icc = 0.5*(t + np.sin(2*w1*t)/(2*w1)); Iss = 0.5*(t - np.sin(2*w1*t)/(2*w1)); Ics = np.sin(w1*t)**2/(2*w1)
        nrm += c1*(A1*A1*Icc + B1*B1*Iss + 2*A1*B1*Ics)
        yt = M1[0,1]; ypt = M1[1,1]
        w2 = s*np.sqrt(c2); L2 = 1-t
        A2 = yt; B2 = ypt/w2
        Icc = 0.5*(L2 + np.sin(2*w2*L2)/(2*w2)); Iss = 0.5*(L2 - np.sin(2*w2*L2)/(2*w2)); Ics = np.sin(w2*L2)**2/(2*w2)
        nrm += c2*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
        out.append(y/np.sqrt(nrm))
    return np.array(out)

R = 4.0
print("t, D, f(t), (R-1)f(t), dD/dt(FD)")
for t in [0.5, 0.9, 0.99, 0.999, 0.9999, 1-1e-6]:
    s = lams_2block(t, 1.0, R)
    lam = s**2
    u = eig_at(t, 1.0, R, s, t)
    f = lam[0]*u[0]**2 - lam[1]*u[1]**2
    h = 1e-7
    t2 = min(t+h, 1-1e-9)
    s2 = lams_2block(t2, 1.0, R)
    dD_dt = ((s2[1]**2 - s2[0]**2) - (s[1]**2 - s[0]**2))/ (t2 - t)
    print(f"t={t:.7f} D={lam[1]-lam[0]:.12f} f={f:.8e} (R-1)f={(R-1)*f:.8e} dD/dt={dD_dt:.8e}")
