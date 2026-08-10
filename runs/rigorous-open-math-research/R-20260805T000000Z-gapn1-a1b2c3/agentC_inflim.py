# -*- coding: utf-8 -*-
"""INF R->inf structure: lam1, lam2 at u=u_inf."""
import numpy as np
from scipy.optimize import brentq

def sec_DN(u, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    a = s*q1*u; b = s*q2*(0.5-u)
    return np.cos(a)*np.cos(b)/q2 - np.sin(a)*np.sin(b)/q1

def sec_DD(u, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    a = s*q1*u; b = s*q2*(0.5-u)
    return np.sin(a)*np.cos(b)/q1 + np.cos(a)*np.sin(b)/q2

R = 1e6
u = 0.32992251
# scan for first DN and DD roots
g = np.linspace(1e-8, 40, 300000)
for which, f in [('DN', lambda s: sec_DN(u, R, 1.0, s)), ('DD', lambda s: sec_DD(u, R, 1.0, s))]:
    v = np.array([f(ss) for ss in g])
    sg = np.signbit(v)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    print(which, "first root bracket:", g[idx[0]], g[idx[0]+1])
    s = brentq(f, g[idx[0]], g[idx[0]+1])
    print("  s =", s, " lam =", s**2)
print("D = lam2-lam1, D*R =", )
# even mode: check lambda1 ~ pi^2/(4u^2)
print("pi^2/(4u^2) =", np.pi**2/(4*u**2))
# odd: tan(s2*u) = s2*(u-1/2)
for a in np.linspace(1.5, 3.0, 1000):
    lhs = np.tan(a)
    rhs = a/u*(u-0.5)
    if abs(lhs-rhs) < 1e-3:
        print("approx a =", a, "lam2 =", (a/u)**2)
