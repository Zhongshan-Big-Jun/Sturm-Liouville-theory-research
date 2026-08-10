# -*- coding: utf-8 -*-
"""Max lambda2/lambda1 for 2-block via phase coordinates (accurate)."""
import numpy as np
from scipy.optimize import brentq, minimize_scalar

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def F(x, mu, c):
    return theta(x, mu) + c*x

g1 = np.linspace(1e-8, 2*np.pi, 30000)
g2 = np.linspace(1e-8, 3*np.pi, 30000)

def xk(mu, c, k, g):
    d = theta(g, mu) + c*g - k*np.pi
    sg = np.signbit(d)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    lo, hi = g[idx[0]], g[idx[0]+1]
    return brentq(lambda a: F(a, mu, c) - k*np.pi, lo, hi)

worst = 1.0; arg = None
for mu in [1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0, 1e4]:
    for c in np.concatenate([np.logspace(-3, 0.5, 40), np.linspace(3.5, 20, 40), np.logspace(1.4, 4, 30)]):
        x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
        r = (x2/x1)**2
        if r > worst: worst, arg = r, (mu, c)
print(f"max lambda2/lambda1 over grid = {worst:.8f} at mu={arg[0]}, c={arg[1]}  (4 would mean ratio<=4 fails)")
# refine at arg
res = minimize_scalar(lambda cc: -(xk(arg[0], cc, 2, g2)/xk(arg[0], cc, 1, g1))**2, bounds=(arg[1]*0.5, arg[1]*2), method='bounded')
print(f"refined: ratio = {(-res.fun):.8f} at c={res.x:.6f}, mu={arg[0]}")
