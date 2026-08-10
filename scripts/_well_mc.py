# -*- coding: utf-8 -*-
"""Compute m_c: largest m with Psi~'(x;m) < 0 on (0,pi) (E3 evidence)."""
import numpy as np
from scipy.optimize import brentq

def Psi(m, x):
    W = np.sin(x)**2 + m*m*np.cos(x)**2
    return x*np.cos(x)/np.sin(x)/W

def dPsi(m, x, h=1e-6):
    return (Psi(m, x+h) - Psi(m, x-h))/(2*h)

# find where min of dPsi over (0,pi) crosses 0
xs = np.linspace(1e-5, np.pi-1e-5, 20001)
for m in [1.30, 1.35, 1.40, 1.41, 1.414, 1.42, 1.43, 1.44, 1.45, 1.46, 1.48, 1.50, 1.55, 1.60]:
    d = dPsi(m, xs)
    print(f"m={m:.3f}: min dPsi={d.min():+.6f} at x={xs[np.argmin(d)]:.4f}")
# bisect for m_c
def min_dPsi(m):
    return dPsi(m, xs).min()
lo, hi = 1.40, 1.50
for _ in range(30):
    mid = 0.5*(lo+hi)
    if min_dPsi(mid) < 0: lo = mid
    else: hi = mid
m_c = 0.5*(lo+hi)
print(f"m_c = {m_c:.6f}, R_c = m_c^2 = {m_c**2:.6f}")
# verify r_tau monotonicity at R just below R_c
m = m_c - 1e-4
for tau in [1.2, 1.5, 1.7, 1.9]:
    xs2 = np.linspace(1e-6, np.pi/tau-1e-6, 20001)
    r = np.log(Psi.__call__ if False else (lambda t: np.sin(tau*t)**2/(np.sin(tau*t)**2+m*m*np.cos(tau*t)**2) / (np.sin(t)**2/(np.sin(t)**2+m*m*np.cos(t)**2)))(xs2))
    # d/dx log r = tau * dlogJ(tau x) - dlogJ(x); check sign
    J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    dlogJ = lambda t: 2/np.sin(t)/np.cos(t)*0  # placeholder
    # direct: log r derivative
    h = 1e-6
    lr = lambda t: np.log(J(tau*t)/J(t))
    d = (lr(xs2[100:-100]+h) - lr(xs2[100:-100]-h))/(2*h)
    print(f"  m={m:.5f} tau={tau}: max d/dx log r_tau = {d.max():+.4e} (<=0 => decreasing)")
