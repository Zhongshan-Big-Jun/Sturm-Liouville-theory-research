# -*- coding: utf-8 -*-
"""Subclaim 3: independent check that sign-consistent critical points of the barrier family satisfy b=1-a.
Barrier: rho=1 on [0,a] u [b,1], R on (a,b). Critical: f(a)=f(b)=0, f = lam1 u1^2 - lam2 u2^2, {f>0}=(a,b)."""
import numpy as np
from scipy.optimize import brentq, root

def M01_barrier(a, b, R, s):
    # 3 blocks (a,1),(b-a,R),(1-b,1); M01* s = secular
    ca, sa = np.cos(s*a), np.sin(s*a)
    mu = np.sqrt(R)
    w = s*mu; L = b-a
    cw, sw = np.cos(w*L), np.sin(w*L)
    c1b, s1b = np.cos(s*(1-b)), np.sin(s*(1-b))
    # M01*s:
    return c1b*(cw*sa + sw*ca/mu) + s1b*(cw*ca - mu*sw*sa)

def lams(a, b, R, k=2):
    smax = np.pi*np.sqrt(R)*(k+2)+10
    s = np.linspace(1e-8, smax, 120000)
    M = M01_barrier(a, b, R, s)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0][:k]
    return np.array([brentq(lambda x: M01_barrier(a, b, R, x), s[idx[j]], s[idx[j]+1]) for j in range(k)])

def eig_at(a, b, R, s, x):
    """unnormalized eigenfunction y (y(0)=0,y'(0)=1) at x; block1 y=sin(sx)/s"""
    if x <= a:
        return np.sin(s*x)/s
    yt = np.sin(s*a)/s; ypt = np.cos(s*a)
    w = s*np.sqrt(R)
    if x <= b:
        return yt*np.cos(w*(x-a)) + (ypt/w)*np.sin(w*(x-a))
    # second light block: match at b
    yb = yt*np.cos(w*(b-a)) + (ypt/w)*np.sin(w*(b-a))
    ypb = -yt*w*np.sin(w*(b-a)) + ypt*np.cos(w*(b-a))
    return yb*np.cos(s*(x-b)) + (ypb/s)*np.sin(s*(x-b))

def norm2(a, b, R, s):
    nrm = 0.0
    w = s*np.sqrt(R)
    nrm += 0.5*(a - np.sin(2*s*a)/(2*s))/s**2
    yt = np.sin(s*a)/s; ypt = np.cos(s*a)
    L = b-a
    A2, B2 = yt, ypt/w
    Icc = 0.5*(L + np.sin(2*w*L)/(2*w)); Iss = 0.5*(L - np.sin(2*w*L)/(2*w)); Ics = np.sin(w*L)**2/(2*w)
    nrm += R*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
    yb = yt*np.cos(w*L) + (ypt/w)*np.sin(w*L)
    ypb = -yt*w*np.sin(w*L) + ypt*np.cos(w*L)
    L2 = 1-b
    A3, B3 = yb, ypb/s
    Icc = 0.5*(L2 + np.sin(2*s*L2)/(2*s)); Iss = 0.5*(L2 - np.sin(2*s*L2)/(2*s)); Ics = np.sin(s*L2)**2/(2*s)
    nrm += 1.0*(A3*A3*Icc + B3*B3*Iss + 2*A3*B3*Ics)
    return nrm

def f_at(a, b, R, x):
    s1, s2 = lams(a, b, R)
    lam = s1**2, s2**2
    vals = []
    for s in (s1, s2):
        y = eig_at(a, b, R, s, x)
        n = norm2(a, b, R, s)
        vals.append(y/np.sqrt(n))
    return lam[0]*vals[0]**2 - lam[1]*vals[1]**2

def crit_solve(R, a0):
    # solve f(a)=0, f(b)=0 near (a0, 1-a0)
    def F(v):
        a, b = v
        return [f_at(a, b, R, a), f_at(a, b, R, b)]
    # fine: use scipy root with numeric jacobian; seed on the symmetric line
    sol = root(F, [a0, 1-a0], method='hybr')
    return sol

print("Solve f(a)=f(b)=0 for barrier; check b vs 1-a (seed = symmetric point)")
for R in [1.5, 2.0, 4.0, 10.0]:
    # first find symmetric critical point by scanning u
    us = np.linspace(0.05, 0.49, 300)
    fs = np.array([f_at(u, 1-u, R, u) for u in us])
    sg = np.signbit(fs)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    u0 = None
    for i in idx:
        u0 = brentq(lambda u: f_at(u, 1-u, R, u), us[i], us[i+1])
    print(f"R={R}: symmetric critical u*={u0:.9f}, b=1-a={1-u0:.9f}")
    sol = crit_solve(R, u0)
    a, b = sol.x
    print(f"   solved (a,b) = ({a:.9f}, {b:.9f}), a+b = {a+b:.12f}, success={sol.success}, |f(a)|+|f(b)|={abs(sol.fun[0])+abs(sol.fun[1]):.2e}")
