# -*- coding: utf-8 -*-
"""Agent C: Q'(c) sign on (0,1/3]; check G>=B/(phi2+c) condition phi1>=phi2 (x2-x1<=pi)."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def thp(x, mu):
    t = np.tan(x)
    return mu*(1+t*t)/(1+mu*mu*t*t)

def roots(mu, c):
    out = []
    for k in (1, 2):
        g = np.linspace(1e-7, (k+1)*np.pi, 6000)
        d = np.array([theta(a, mu) + c*a - k*np.pi for a in g])
        sg = np.signbit(d)
        idx = np.nonzero(sg[1:] != sg[:-1])[0]
        lo, hi = g[idx[0]], g[idx[0]+1]
        out.append(brentq(lambda a: theta(a, mu) + c*a - k*np.pi, lo, hi))
    return out

for mu in [1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0]:
    worst_Qp = 1.0
    worst_x2x1 = 0.0
    for c in np.linspace(1e-3, 1/3, 60):
        x1, x2 = roots(mu, c)
        B = x2**2 - x1**2
        p1, p2 = thp(x1, mu), thp(x2, mu)
        G = x2**2/(p2+c) - x1**2/(p1+c)
        Qp = 2*(mu+c)*(B - (mu+c)*G)
        worst_Qp = min(worst_Qp, Qp)      # if min > 0, Q' > 0 somewhere
        worst_x2x1 = max(worst_x2x1, x2-x1)
    print(f"mu={mu:6.3f}: min Q' on (0,1/3] = {worst_Qp:+.6e}  max (x2-x1) = {worst_x2x1:.6f} vs pi={np.pi:.6f}")
