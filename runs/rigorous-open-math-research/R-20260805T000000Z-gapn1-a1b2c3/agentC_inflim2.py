# -*- coding: utf-8 -*-
"""Verify INF R->inf closed form: u_lim solves self-consistency, D*R = (a^2 - pi^2/4)/u^2 with tan a = a(1-1/(2u))."""
import numpy as np
from scipy.optimize import brentq

def Dr(u):
    # a in (pi/2, pi) solving tan a = a*(1 - 1/(2u)); note for u<1/2, 1-1/(2u)<0
    a = brentq(lambda x: np.tan(x) - x*(1-1/(2*u)), 1.7, np.pi-1e-6)
    return (a**2 - np.pi**2/4)/u**2

# find u in (1/3, 1/2) approx where Dr matches 24.943866; scan
uu = np.linspace(0.32, 0.36, 400)
vals = np.array([Dr(u) for u in uu])
print("Dr(0.32992251) =", Dr(0.32992251))
print("target 24.943866...")
i = np.argmin(np.abs(vals-24.943866))
print("closest u in scan:", uu[i], Dr(uu[i]))
# Dr has an interior minimum (the target value is the minimum itself), so
# brentq on [0.32, 0.34] fails (both endpoints sit above the minimum).
# Locate the minimum by a fine scan instead.
uu2 = np.linspace(0.32, 0.36, 40000)
vals2 = np.array([Dr(u) for u in uu2])
imin = int(np.argmin(vals2))
print('min Dr over scan:', uu2[imin], vals2[imin])
print('target           : 24.943866138432938')
