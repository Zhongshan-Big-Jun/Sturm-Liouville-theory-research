# -*- coding: utf-8 -*-
"""Check sign of W'(c) = 2(mu+c)U + (mu+c)^2 U' on a grid."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def thp(x, mu):
    t = np.tan(x)
    return mu*(1+t*t)/(1+mu*mu*t*t)

def F(x, mu, c):
    return theta(x, mu) + c*x

g1 = np.linspace(1e-7, 2*np.pi, 20000)
g2 = np.linspace(1e-7, 3*np.pi, 20000)

def xk(mu, c, k, g):
    d = theta(g, mu) + c*g - k*np.pi
    sg = np.signbit(d)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    lo, hi = g[idx[0]], g[idx[0]+1]
    return brentq(lambda a: F(a, mu, c) - k*np.pi, lo, hi)

print("W'(c) sign scan; want < 0 everywhere for monotone decrease")
for mu in [1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0]:
    worst = 1.0; worst_arg = None
    cs = np.concatenate([np.logspace(-4, 0, 30), np.linspace(1.1, 10, 20), np.logspace(1.05, 4, 25)])
    for c in cs:
        x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
        U = x2**2 - x1**2
        p1, p2 = thp(x1, mu), thp(x2, mu)
        Up = -2*x2**2/(p2+c) + 2*x1**2/(p1+c)
        Wp = 2*(mu+c)*U + (mu+c)**2*Up
        if Wp < worst: worst, worst_arg = Wp, c
        if Wp > 0:
            print(f"  mu={mu} c={c}: W' = {Wp:+.6e}  (positive!)")
    print(f"mu={mu:7.3f}: min W' = {worst:+.6e} at c={worst_arg}")
