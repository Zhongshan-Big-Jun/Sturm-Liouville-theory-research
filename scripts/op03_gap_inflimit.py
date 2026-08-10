# -*- coding: utf-8 -*-
"""R->infty limit of INF gap: solve the limiting system for (u, mu_2).
Even mode: mu_1 = pi^2/(4u^2). Odd mode: tan(sqrt(mu2) u) = sqrt(mu2)(u - 1/2).
Self-consistency: mu_1 * 2/u = mu_2 * sin^2(a u)/I2, a=sqrt(mu2), I2=int_0^u sin^2(a x) dx.
D*R -> mu_2 - mu_1.
"""
import numpy as np
from scipy.optimize import fsolve

def system(vars):
    u, mu2 = vars
    a = np.sqrt(mu2)
    I2 = 0.5*u - np.sin(2*a*u)/(4*a)
    F1 = np.tan(a*u) - a*(u - 0.5)
    mu1 = np.pi**2/(4*u**2)
    F2 = mu1*2/u - mu2*np.sin(a*u)**2/I2
    return [F1, F2]

for guess in ([0.33, 47.0], [0.30, 50.0], [0.35, 45.0]):
    try:
        u, mu2 = fsolve(system, guess, full_output=True)[0]
        mu1 = np.pi**2/(4*u**2)
        print(f"u={u:.8f} mu1={mu1:.6f} mu2={mu2:.6f} D*R={mu2-mu1:.6f}")
    except Exception as ex:
        print("fail", ex)
