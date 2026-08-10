# -*- coding: utf-8 -*-
"""Agent C: critical points of D (zeros of f) + (a,c) coordinates. Vectorized."""
import numpy as np
from scipy.optimize import brentq

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    return (np.sin(w1*t)/q1)*np.cos(w2*(1-t)) + (np.cos(w1*t)/q1**0)*np.sin(w2*(1-t))/q2

def lams_vec(ts, c1, c2, k=2, n_s=40000, chunk=300):
    smax = np.pi*np.sqrt(max(c1, c2))*(k+2)+10
    s = np.linspace(1e-9, smax, n_s)
    roots = np.zeros((len(ts), k))
    for a0 in range(0, len(ts), chunk):
        tch = ts[a0:a0+chunk]
        T = tch[:, None]; S = s[None, :]
        w1 = S*np.sqrt(c1); w2 = S*np.sqrt(c2)
        M = (np.sin(w1*T)/np.sqrt(c1))*np.cos(w2*(1-T)) + np.cos(w1*T)*np.sin(w2*(1-T))/np.sqrt(c2)
        sg = np.signbit(M); ch = sg[:,1:] != sg[:,:-1]
        for i in range(len(tch)):
            idx = np.nonzero(ch[i])[0][:k]
            for j in range(k):
                lo, hi = s[idx[j]], s[idx[j]+1]
                roots[a0+i, j] = brentq(lambda x, tt=tch[i]: M01_2block(tt, c1, c2, x), lo, hi)
    return roots

def fvals(ts, c1, c2, roots):
    n = len(ts)
    f = np.zeros(n)
    for i in range(n):
        t = ts[i]; lam = roots[i]**2
        vals = []
        for sk in roots[i]:
            w1 = sk*np.sqrt(c1); q1 = np.sqrt(c1)
            A1, B1 = 0.0, 1.0/q1
            Icc = 0.5*(t + np.sin(2*w1*t)/(2*w1)); Iss = 0.5*(t - np.sin(2*w1*t)/(2*w1)); Ics = np.sin(w1*t)**2/(2*w1)
            nrm = c1*(A1*A1*Icc + B1*B1*Iss + 2*A1*B1*Ics)
            w2 = sk*np.sqrt(c2); L2 = 1-t
            yt = np.sin(w1*t)/q1; ypt = np.cos(w1*t)
            A2 = yt; B2 = ypt/w2
            Icc = 0.5*(L2 + np.sin(2*w2*L2)/(2*w2)); Iss = 0.5*(L2 - np.sin(2*w2*L2)/(2*w2)); Ics = np.sin(w2*L2)**2/(2*w2)
            nrm += c2*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
            vals.append(yt/np.sqrt(nrm))
        f[i] = lam[0]*vals[0]**2 - lam[1]*vals[1]**2
    return f

print("=== critical points and margins (HR) ===")
for R in [1.5, 2.0, 4.0, 10.0, 100.0]:
    ts = np.linspace(1e-6, 1-1e-6, 3000)
    roots = lams_vec(ts, 1.0, R)
    f = fvals(ts, 1.0, R, roots)
    sg = np.signbit(f)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    tcrits = []
    for i in idx:
        tcrits.append(brentq(lambda x: fvals(np.array([x]), 1.0, R, lams_vec(np.array([x]), 1.0, R, k=2))[0], ts[i], ts[i+1]))
    print(f"R={R}: f-zeros at {[f'{t:.8f}' for t in tcrits]}")
    for t in tcrits:
        r = lams_vec(np.array([t]), 1.0, R)[0]
        D = r[1]**2 - r[0]**2
        print(f"   t={t:.8f}: D={D:.12f}  3pi^2-D={3*np.pi**2-D:+.3e}  D-3pi^2/R={D-3*np.pi**2/R:+.3e}")
