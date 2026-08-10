# -*- coding: utf-8 -*-
"""Test candidate upper-bound chains for c>=1 (regime A) and c in [1/3,1] (regime B).
Chain1 (c>=3):  W <= (mu+c)^2 [4pi^2/(1+c)^2 - pi^2/(mu+c)^2]
Chain2 (c>=1):  W <= (mu+c)^2 [pi mu/(1+mu c)] * [2 pi mu/(1+mu c) + pi/(1+c)]
ChainB (c in [1/3,1]): W <= 3pi^2 (mu+c)^2/(1+c)^2
Compare each to 3 pi^2 mu^2.
"""
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

def W(mu, c):
    x1, x2 = xk(mu, c, 1, g1), xk(mu, c, 2, g2)
    return (mu+c)**2*(x2**2-x1**2)

PI2 = np.pi**2
print("== Chain2 (c>=1): ratio bound/(3 pi^2 mu^2); want < 1 ==")
worst2 = 0
for mu in [1.001, 1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0]:
    for c in np.linspace(1.0, 3.0, 60):
        b2 = (mu+c)**2*(np.pi*mu/(1+mu*c))*(2*np.pi*mu/(1+mu*c) + np.pi/(1+c))
        r = b2/(3*PI2*mu**2)
        if r > worst2: worst2 = r
        if r >= 1: print(f"  FAIL mu={mu} c={c}: ratio {r:.6f}")
print(f"worst Chain2 ratio = {worst2:.8f}")

print("== Chain1 (c>=3): ratio bound/(3 pi^2 mu^2) ==")
worst1 = 0
for mu in [1.001, 1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0]:
    for c in np.linspace(3.0, 100.0, 80):
        b1 = (mu+c)**2*(4*PI2/(1+c)**2 - PI2/(mu+c)**2)
        r = b1/(3*PI2*mu**2)
        if r > worst1: worst1 = r
        if r >= 1: print(f"  FAIL mu={mu} c={c}: ratio {r:.6f}")
print(f"worst Chain1 ratio = {worst1:.8f}")

print("== ChainB (c in [1/3,1]): ratio = ((mu+c)/(1+c))^2/mu^2; want < 1 ==")
worstB = 0
for mu in [1.001, 1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0]:
    for c in np.linspace(1/3, 1.0, 50):
        r = ((mu+c)/(1+c))**2/mu**2
        if r > worstB: worstB = r
print(f"worst ChainB ratio = {worstB:.8f}")

print("== sanity: actual W/(3 pi^2 mu^2) max over c for each mu ==")
for mu in [1.05, 2.0, 10.0]:
    worst = 0
    for c in np.concatenate([np.logspace(-6,-0.5,30), np.linspace(0.35,3,40), np.logspace(0.5,2,20)]):
        r = W(mu, c)/(3*PI2*mu**2)
        worst = max(worst, r)
    print(f"mu={mu}: actual max ratio = {worst:.10f}")
