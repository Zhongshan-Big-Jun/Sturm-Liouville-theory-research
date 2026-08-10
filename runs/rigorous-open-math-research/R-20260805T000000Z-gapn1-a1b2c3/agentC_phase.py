# -*- coding: utf-8 -*-
"""Agent C: phase-coordinate analysis. F(x)=theta(x)+cx, theta(x)=arctan(mu tan x) (continuous branch).
Roots by monotone bisection (F strictly increasing; no grid needed)."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    # continuous branch: theta(x) = arctan(mu tan x) + pi*floor((x+pi/2)/pi)
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def F(x, mu, c):
    return theta(x, mu) + c*x

def roots_ac(mu, c, kmax=2):
    # F strictly increasing on (0, k*pi) with F(0)=0 and F(k*pi) > k*pi
    return [brentq(lambda a, kk=kk: F(a, mu, c) - kk*np.pi, 0.0, kk*np.pi) for kk in range(1, kmax+1)]

print("c, x1, x2, Q=(mu+c)^2(x2^2-x1^2), Q-3pi^2, 3pi^2mu^2-Q, x1*?, theta'(x1), theta'(x2)")
for mu in [np.sqrt(1.5), 2.0, np.sqrt(100.0)]:
    print(f"==== mu={mu:.6f} (R={mu**2}) ====")
    for c in [1e-3, 0.02, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 100.0, 1e3]:
        x1, x2 = roots_ac(mu, c)
        Q = (mu+c)**2*(x2**2 - x1**2)
        def thp(x):
            t = np.tan(x)
            return mu*(1+t*t)/(1+mu*mu*t*t)
        print(f"c={c:9.2f}: x1={x1:.8f} x2={x2:.8f} Q={Q:.8f} Q-3pi^2={Q-3*np.pi**2:+.4e} 3mu^2pi^2-Q={3*np.pi**2*mu**2-Q:+.4e} thp(x1)={thp(x1):.6f} thp(x2)={thp(x2):.6f}")
