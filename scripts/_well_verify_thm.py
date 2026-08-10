# -*- coding: utf-8 -*-
"""Verify: (1) H'>=0 lemma numerically; (2) r~_tau decreasing for R<=1.5, non-mono for R>1.5;
(3) off-axis E=0 branch threshold ~R=1.5."""
import numpy as np
from scipy.optimize import brentq

# (1) H' >= 0
xs = np.linspace(1e-6, np.pi-1e-6, 20001)
Hp = 18 - 16*np.cos(2*xs) - 2*np.cos(4*xs) - 8*xs*np.sin(2*xs) - 8*xs*np.sin(4*xs)
print(f"H' min on (0,pi): {Hp.min():+.3e}  (>=0 => lemma OK)")

# (2) r~_tau monotonicity across threshold
for R in [1.4, 1.5, 1.6, 1.7]:
    m = np.sqrt(R)
    J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    worst = 0.0
    for tau in [1.2, 1.5, 1.9]:
        xx = np.linspace(1e-6, np.pi/tau-1e-6, 20001)
        lr = np.log(J(tau*xx)/J(xx))
        d = np.diff(lr)
        worst = max(worst, d.max())
    print(f"R={R}: worst max-step of log r~_tau = {worst:+.3e}  {'DECREASING' if worst<=1e-12 else 'NOT monotone'}")

# (3) off-axis E=0 branch threshold, fine scan
def rtau_val(a, b, R):
    from _well_landscape2 import eigs_well
    m = np.sqrt(R)
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
    A = m*s1*a; B = m*s1*(1-b)
    J2 = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    return np.log(J2(tau*A)/J2(A)) - np.log(J2(tau*B)/J2(B))
for R in [1.50, 1.52, 1.55, 1.60]:
    found = False
    for a in np.linspace(0.02, 0.20, 25):
        bs = np.linspace(a+0.3, 0.999, 150)
        E = np.array([rtau_val(a, b, R) for b in bs])
        for i in range(len(bs)-1):
            if E[i]*E[i+1] < 0 and abs(a+0.5*(bs[i]+bs[i+1])-1) > 0.01:
                found = True; break
        if found: break
    print(f"R={R:.2f}: off-axis E=0 branch: {found}")
