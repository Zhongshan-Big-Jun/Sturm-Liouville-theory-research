# -*- coding: utf-8 -*-
"""Fresh verification (fast): phase-coordinate reduction for 2-block problem."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def F(x, mu, c):
    return theta(x, mu) + c*x

def xk(mu, c, k, g):
    d = theta(g, mu) + c*g - k*np.pi
    sg = np.signbit(d)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    if len(idx) == 0:
        raise RuntimeError(f"no root mu={mu} c={c} k={k}")
    lo, hi = g[idx[0]], g[idx[0]+1]
    return brentq(lambda a: F(a, mu, c) - k*np.pi, lo, hi)

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    return (np.sin(w1*t)/q1)*np.cos(w2*(1-t)) + np.cos(w1*t)*np.sin(w2*(1-t))/q2

def lams_direct(t, c1, c2, k=2):
    smax = np.pi*np.sqrt(max(c1,c2))*(k+2)+10
    s = np.linspace(1e-9, smax, 40000)
    M = M01_2block(t, c1, c2, s)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0][:k]
    roots = [brentq(lambda x: M01_2block(t, c1, c2, x), s[idx[j]], s[idx[j]+1]) for j in range(k)]
    return np.array(roots)

PI2 = np.pi**2
g1 = np.linspace(1e-7, 2*np.pi, 20000)
g2 = np.linspace(1e-7, 3*np.pi, 20000)
print("== check: D_HR == D_HL == Q(mu,c) ==")
for R, ts in [(1.5, [0.05,0.3,0.6,0.95]), (4.0, [0.05,0.3,0.6,0.95]), (10.0, [0.1,0.5,0.9])]:
    mu = np.sqrt(R)
    for t in ts:
        c = mu*(1-t)/t
        x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
        Q = (mu+c)**2*(x2**2-x1**2)/mu**2
        rHR = lams_direct(t, 1.0, R); rHL = lams_direct(t, R, 1.0)
        dHR = rHR[1]**2 - rHR[0]**2; dHL = rHL[1]**2 - rHL[0]**2
        print(f"  R={R} t={t}: Q={Q:.10f} D_HR={dHR:.10f} D_HL={dHL:.10f} diffs={max(abs(Q-dHR),abs(Q-dHL)):.2e}")

print()
print("== W = (mu+c)^2 (x2^2-x1^2) vs 3pi^2 and 3pi^2 mu^2 ==")
worst_lo = 1.0; worst_hi = 1.0
worst_lo_arg = worst_hi_arg = None
for mu in [1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0]:
    cs = np.concatenate([np.logspace(-4, -0.3, 25), np.linspace(0.6, 3, 15), np.logspace(0.5, 4, 25)])
    for c in cs:
        x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
        W = (mu+c)**2*(x2**2-x1**2)
        lo = W/(3*PI2) - 1.0
        hi = (3*PI2*mu**2)/W - 1.0
        if lo < worst_lo: worst_lo, worst_lo_arg = lo, (mu, c)
        if hi < worst_hi: worst_hi, worst_hi_arg = hi, (mu, c)
        assert lo > 0 and hi > 0, (mu, c, lo, hi)
print(f"min(W/3pi^2 - 1) = {worst_lo:.6e} at mu={worst_lo_arg[0]}, c={worst_lo_arg[1]}")
print(f"min(3mu^2pi^2/W - 1) = {worst_hi:.6e} at mu={worst_hi_arg[0]}, c={worst_hi_arg[1]}")
