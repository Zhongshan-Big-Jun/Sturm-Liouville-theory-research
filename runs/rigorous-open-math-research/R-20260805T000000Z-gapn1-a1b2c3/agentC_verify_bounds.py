# -*- coding: utf-8 -*-
"""Agent C: verify analytic bounds (optimized)."""
import numpy as np
from scipy.optimize import brentq

def theta(x, mu):
    return np.arctan(mu*np.tan(x)) + np.pi*np.floor((x+np.pi/2)/np.pi)

def xk(mu, c, k, g=None):
    if g is None:
        g = np.linspace(1e-7, (k+1)*np.pi, 4000)
    d = np.array([theta(a, mu) + c*a - k*np.pi for a in g])
    sg = np.signbit(d)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    lo, hi = g[idx[0]], g[idx[0]+1]
    return brentq(lambda a: theta(a, mu) + c*a - k*np.pi, lo, hi)

print("=== c>=1: (mu+c)^2 * [pi mu/(mu c+1)] * (x1b+x2b) / (3pi^2 mu^2) ===")
for mu in [1.05, 1.225, 1.5, 2.0, 3.0, 5.0, 10.0]:
    worst = 0
    for c in np.linspace(1.0, 20.0, 60):
        x1b = np.pi/(1+c)
        x2b = np.pi*(mu+1)/(mu+c) if c <= 3 else 2*np.pi/(1+c)
        prod = (np.pi*mu/(mu*c+1))*(x1b + x2b)
        worst = max(worst, (mu+c)**2*prod/(3*np.pi**2*mu**2))
    print(f"  mu={mu:6.3f}: worst ratio = {worst:.6f}  (<1 needed)")

print("=== c in [1/3,1): LB vs RHS ===")
for mu in [1.05, 1.2, 1.225, 1.5, 2.0, 3.0, 10.0]:
    ok = True; worst = 0
    for c in np.linspace(1/3, 1.0, 40):
        LB = (c/(1+c))*(4*mu+3*c+2)/(mu+c)
        RHS = 3*c*(2*mu+c)/(mu+c)**2
        if LB <= RHS: ok = False
        worst = max(worst, RHS/LB)
    print(f"  mu={mu:6.3f}: LB>RHS? {ok}  (max RHS/LB={worst:.6f})")

print("=== c in (0,1/3]: LB2 vs RHS ===")
for mu in [1.05, 1.2, 1.225, 1.5, 2.0, 3.0, 10.0]:
    ok = True; worst = 0
    for c in np.linspace(1e-4, 1/3, 80):
        u2l = 2*c/(mu+c); u2h = 2*c/(1+c); u1l = c/(mu+c); u1h = c/(1+c)
        LB = u2l*(4 - u2h) - u1h*(2 - u1l)
        RHS = 3*c*(2*mu+c)/(mu+c)**2
        if LB <= RHS: ok = False
        worst = max(worst, RHS/LB)
    print(f"  mu={mu:6.3f}: LB2>RHS? {ok}  (max RHS/LB={worst:.6f})")
