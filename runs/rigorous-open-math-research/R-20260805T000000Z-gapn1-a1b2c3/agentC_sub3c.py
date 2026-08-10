# -*- coding: utf-8 -*-
"""Subclaim 3: hunt for asymmetric critical points with random seeds."""
import numpy as np
from scipy.optimize import brentq, root

def M01_barrier(a, b, R, s):
    ca, sa = np.cos(s*a), np.sin(s*a)
    mu = np.sqrt(R)
    w = s*mu; L = b-a
    cw, sw = np.cos(w*L), np.sin(w*L)
    c1b, s1b = np.cos(s*(1-b)), np.sin(s*(1-b))
    return c1b*(cw*sa + sw*ca/mu) + s1b*(cw*ca - mu*sw*sa)

def lams(a, b, R, k=2):
    smax = np.pi*np.sqrt(R)*(k+2)+10
    s = np.linspace(1e-8, smax, 60000)
    M = M01_barrier(a, b, R, s)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0][:k]
    return np.array([brentq(lambda x: M01_barrier(a, b, R, x), s[idx[j]], s[idx[j]+1]) for j in range(k)])

def eig_at(a, b, R, s, x):
    if x <= a:
        return np.sin(s*x)/s
    yt = np.sin(s*a)/s; ypt = np.cos(s*a)
    w = s*np.sqrt(R)
    if x <= b:
        return yt*np.cos(w*(x-a)) + (ypt/w)*np.sin(w*(x-a))
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

def crit(a, b, R):
    return [f_at(a, b, R, a), f_at(a, b, R, b)]

rng = np.random.default_rng(42)
for R in [1.5, 2.0, 4.0, 10.0]:
    found = []
    for trial in range(25):
        a0 = rng.uniform(0.02, 0.48)
        b0 = rng.uniform(a0+0.03, 0.98)
        try:
            sol = root(lambda v: crit(v[0], v[1], R), [a0, b0], method='hybr')
        except Exception:
            continue
        if sol.success:
            a, b = sol.x
            resid = abs(sol.fun[0]) + abs(sol.fun[1])
            if resid < 1e-7 and 0 < a < b < 1:
                xs = np.linspace(0.001, 0.999, 300)
                fv = np.array([f_at(a, b, R, x) for x in xs])
                pos = fv > 0
                pat = ''.join('+' if p else '-' for p in pos)
                collapsed = pat[0]
                for cc in pat[1:]:
                    if cc != collapsed[-1]: collapsed += cc
                found.append((a, b, resid, collapsed))
    print(f"R={R}: {len(found)} distinct-ish critical points from 25 random seeds")
    seen = set()
    for a, b, r, pat in found:
        key = (round(a,6), round(b,6))
        if key in seen: continue
        seen.add(key)
        print(f"   a={a:.9f} b={b:.9f} a+b={a+b:.12f} resid={r:.1e} sign-pattern={pat}")
