# -*- coding: utf-8 -*-
"""Final comprehensive check: verify each proof inequality of Subclaim 1 holds on a dense (mu,c) grid."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def thp(x, mu):
    t = np.tan(x)
    return mu*(1+t*t)/(1+mu*mu*t*t)

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

PI2 = np.pi**2
fails = []
n = 0
for mu in [1.001, 1.02, 1.05, 1.1, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0, 1e4]:
    for c in np.concatenate([np.logspace(-6, -0.6, 25), np.linspace(0.3, 1.0, 25), np.linspace(1.05, 5, 30), np.logspace(0.7, 4, 25)]):
        n += 1
        x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
        W = (mu+c)**2*(x2**2-x1**2)
        # conclusion must hold
        assert W > 3*PI2 and W < 3*PI2*mu**2, (mu, c, W)
        # proof inequalities:
        if c >= 1:
            # Chain2: W <= (mu+c)^2 [pi mu/(1+mu c)] [2 pi mu/(1+mu c) + pi/(1+c)] < 3 pi^2 mu^2
            b2 = (mu+c)**2*(np.pi*mu/(1+mu*c))*(2*np.pi*mu/(1+mu*c) + np.pi/(1+c))
            assert W <= b2 + 1e-9 and b2 < 3*PI2*mu**2, (mu, c, "chain2")
            # validity conditions
            assert x1 <= np.pi/(1+c) + 1e-9        # theta(x1) >= x1
            assert x2 <= 2*np.pi*mu/(1+mu*c) + 1e-9 # theta' >= 1/mu
            assert x2 - x1 <= np.pi*mu/(1+mu*c) + 1e-9
        elif c >= 1/3:
            # ChainB
            bB = 3*PI2*(mu+c)**2/(1+c)**2
            assert W <= bB + 1e-9 and bB < 3*PI2*mu**2, (mu, c, "chainB")
            assert x1 >= np.pi/(1+c) - 1e-9   # theta(x1) <= x1 (x1 in [pi/2,pi])
            assert x2 <= 2*np.pi/(1+c) + 1e-9 # theta(x2) >= x2 (x2 in [pi,3pi/2])
        else:
            # regime C: W' < 0
            p1, p2 = thp(x1, mu), thp(x2, mu)
            U = x2**2 - x1**2
            Up = -2*x2**2/(p2+c) + 2*x1**2/(p1+c)
            Wp = 2*(mu+c)*U + (mu+c)**2*Up
            assert Wp < 0, (mu, c, "Wp")
print(f"checked {n} (mu,c) points; ALL proof inequalities hold (0 failures)")
