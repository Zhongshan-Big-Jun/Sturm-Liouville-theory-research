# -*- coding: utf-8 -*-
"""scan phi' on [a0, 1) densely + asymptotics near b=1 (EVIDENCE)."""
import numpy as np
a0 = float(np.arccos(0.25)/np.pi)
pi = np.pi
sqrt15 = np.sqrt(15)
def dphi(b):
    u = np.cos(2*pi*b); v = np.sin(2*pi*b)
    N = (56*pi*a0 - 6*sqrt15)*u**2 + (2*pi*a0 + 3*sqrt15)*u + (3*sqrt15 - 58*pi*a0) + 2*sqrt15*pi*(1-b)*(1-4*u)*v
    return -N/(60*pi)
# dense scan
for bmax in (0.98, 0.999, 1.0-1e-6, 1.0-1e-9):
    grid = np.linspace(a0, bmax, 200001)
    vals = dphi(grid)
    print("scan to b=%.3g: min=%.6e at b=%.6f  pos=%s" % (bmax, vals.min(), grid[np.argmin(vals)], bool((vals>0).all())))
# near b=1 asymptotic
for eps in (1e-2, 1e-3, 1e-4, 1e-6):
    b = 1 - eps
    d = dphi(b)
    # predicted: phi' ~ C * eps^2 ; C = 2509.5/(60 pi)
    C_pred = ((9*sqrt15 - 114*pi*a0)*(-2*pi**2) - 12*sqrt15*pi**2)/(60*pi)
    print("eps=%.0e: phi'=%.6e  phi'/eps^2=%.4f  pred C=%.4f" % (eps, d, d/eps**2, C_pred))
