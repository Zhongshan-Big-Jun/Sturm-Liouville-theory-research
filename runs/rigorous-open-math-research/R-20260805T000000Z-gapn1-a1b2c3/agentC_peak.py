# -*- coding: utf-8 -*-
"""Where does W peak? Measure margin to 3pi^2 mu^2."""
import numpy as np
from scipy.optimize import brentq, minimize_scalar

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

def W(mu, c):
    x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
    return (mu+c)**2*(x2**2-x1**2)

for mu in [1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0]:
    cs = np.linspace(1e-3, 4.0, 2000)
    ws = np.array([W(mu, c) for c in cs])
    i = np.argmax(ws)
    # refine
    res = minimize_scalar(lambda c: -W(mu, c), bounds=(cs[max(0,i-3)], cs[min(len(cs)-1,i+3)]), method='bounded')
    wmax = -res.fun
    print(f"mu={mu:6.3f}: sup_c W = {wmax:.10f}  3pi^2 mu^2 = {3*np.pi**2*mu**2:.10f}  margin = {3*np.pi**2*mu**2 - wmax:+.6e}  at c={res.x:.5f}  ratio={wmax/(3*np.pi**2*mu**2):.8f}")
