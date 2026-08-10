# -*- coding: utf-8 -*-
"""Checks: (a) FH dD/dt = -(R-1)*f for 2-block HR; (b) f sign pattern; (c) D_SUP(1/4), D_INF(1/4)."""
import numpy as np
from scipy.optimize import brentq

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    return (np.sin(w1*t)/q1)*np.cos(w2*(1-t)) + np.cos(w1*t)*np.sin(w2*(1-t))/q2

def lams(t, c1, c2, k=2):
    smax = np.pi*np.sqrt(max(c1,c2))*(k+2)+10
    s = np.linspace(1e-8, smax, 60000)
    M = M01_2block(t, c1, c2, s)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0][:k]
    return np.array([brentq(lambda x: M01_2block(t, c1, c2, x), s[idx[j]], s[idx[j]+1]) for j in range(k)])

def u_at_jump(t, c1, c2, s1, s2):
    u1 = np.zeros(len(t)); u2 = np.zeros(len(t))
    for i in range(len(t)):
        tt = t[i]
        for j, s in enumerate([s1[i], s2[i]]):
            w1 = s*np.sqrt(c1); q1 = np.sqrt(c1)
            A1, B1 = 0.0, 1.0/q1
            Icc = 0.5*(tt + np.sin(2*w1*tt)/(2*w1)); Iss = 0.5*(tt - np.sin(2*w1*tt)/(2*w1)); Ics = np.sin(w1*tt)**2/(2*w1)
            nrm = c1*(A1*A1*Icc + B1*B1*Iss + 2*A1*B1*Ics)
            w2 = s*np.sqrt(c2); L2 = 1-tt
            yt = np.sin(w1*tt)/q1; ypt = np.cos(w1*tt)
            A2 = yt; B2 = ypt/w2
            Icc = 0.5*(L2 + np.sin(2*w2*L2)/(2*w2)); Iss = 0.5*(L2 - np.sin(2*w2*L2)/(2*w2)); Ics = np.sin(w2*L2)**2/(2*w2)
            nrm += c2*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
            val = yt/np.sqrt(nrm)
            if j == 0: u1[i] = val
            else: u2[i] = val
    return u1, u2

print("== (a) FH: dD/dt vs -(R-1)*f, HR, R=4 ==")
for R in [2.0, 4.0]:
    ts = np.linspace(0.05, 0.95, 300)
    L = np.array([lams(t, 1.0, R) for t in ts])
    lam = L**2
    Ds = lam[:,1]-lam[:,0]
    u1, u2 = u_at_jump(ts, 1.0, R, L[:,0], L[:,1])
    f = lam[:,0]*u1**2 - lam[:,1]*u2**2
    dD = np.gradient(Ds, ts)
    ratio = dD/(-(R-1)*f)
    print(f"  R={R}: max |dD/dt + (R-1)f| = {np.max(np.abs(dD+(R-1)*f)):.3e}")

print("== (b) f sign changes for 2-block (should be 2: -,+,-) ==")
for R in [1.5, 4.0, 10.0]:
    ts = np.linspace(0.02, 0.98, 800)
    L = np.array([lams(t, 1.0, R) for t in ts])
    lam = L**2
    u1, u2 = u_at_jump(ts, 1.0, R, L[:,0], L[:,1])
    f = lam[:,0]*u1**2 - lam[:,1]*u2**2
    sg = np.signbit(f)
    nsc = (sg[1:] != sg[:-1]).sum()
    print(f"  R={R}: f sign changes = {nsc}")

print("== (c) D_SUP(1/4) vs 3pi^2, D_INF(1/4) vs 3pi^2/R ==")
PI2 = np.pi**2
def D_sym(u, R, sup):
    # full symmetric 3-block: compute via half-problem DN/DD
    c1, c2 = (1.0, R) if sup else (R, 1.0)
    # DN first root
    g = np.linspace(1e-8, np.pi*np.sqrt(max(c1,c2))+4, 80000)
    v0 = np.array([(np.cos(s*np.sqrt(c1)*u)*np.cos(s*np.sqrt(c2)*(0.5-u))/np.sqrt(c2) - np.sin(s*np.sqrt(c1)*u)*np.sin(s*np.sqrt(c2)*(0.5-u))/np.sqrt(c1)) for s in g])
    sg0 = np.signbit(v0); idx0 = np.nonzero(sg0[1:]!=sg0[:-1])[0]
    s0 = brentq(lambda s: (np.cos(s*np.sqrt(c1)*u)*np.cos(s*np.sqrt(c2)*(0.5-u))/np.sqrt(c2) - np.sin(s*np.sqrt(c1)*u)*np.sin(s*np.sqrt(c2)*(0.5-u))/np.sqrt(c1)), g[idx0[0]], g[idx0[0]+1])
    v1 = np.array([(np.sin(s*np.sqrt(c1)*u)*np.cos(s*np.sqrt(c2)*(0.5-u))/np.sqrt(c1) + np.cos(s*np.sqrt(c1)*u)*np.sin(s*np.sqrt(c2)*(0.5-u))/np.sqrt(c2)) for s in g])
    sg1 = np.signbit(v1); idx1 = np.nonzero(sg1[1:]!=sg1[:-1])[0]
    s1 = brentq(lambda s: (np.sin(s*np.sqrt(c1)*u)*np.cos(s*np.sqrt(c2)*(0.5-u))/np.sqrt(c1) + np.cos(s*np.sqrt(c1)*u)*np.sin(s*np.sqrt(c2)*(0.5-u))/np.sqrt(c2)), g[idx1[0]], g[idx1[0]+1])
    return s1**2 - s0**2

for R in [1.5, 2.0, 4.0, 10.0, 100.0]:
    ds = D_sym(0.25, R, True); di = D_sym(0.25, R, False)
    print(f"  R={R:7.2f}: D_SUP(1/4)-3pi^2 = {ds-3*PI2:+.4e}   D_INF(1/4)-3pi^2/R = {di-3*PI2/R:+.4e}")
