# -*- coding: utf-8 -*-
"""Test: is w(mu) = W(mu,c)/mu^2 decreasing in mu for fixed c?"""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

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

for c in [1e-4, 0.01, 0.1, 1/3, 0.5, 1.0, 2.0, 10.0]:
    mus = np.linspace(1.0001, 10.0, 120)
    ws = []
    for mu in mus:
        x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
        ws.append((mu+c)**2*(x2**2-x1**2)/mu**2)
    dec = all(ws[i+1] < ws[i] for i in range(len(ws)-1))
    print(f"c={c:8.4f}: w decreasing? {dec}   w(1+)= {ws[0]:.10f}  w(10)= {ws[-1]:.10f}  (3pi^2={3*np.pi**2:.6f})")
