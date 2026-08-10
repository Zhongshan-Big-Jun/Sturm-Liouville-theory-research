# -*- coding: utf-8 -*-
"""Off-axis E=0 branch existence threshold over R (E3 evidence)."""
import numpy as np
from scipy.optimize import brentq
from _well_landscape2 import eigs_well

def rtau_val(a, b, R):
    m = np.sqrt(R)
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
    A = m*s1*a; B = m*s1*(1-b)
    J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    return np.log(J(tau*A)/J(A)) - np.log(J(tau*B)/J(B))

for R in [1.2, 1.5, 1.8, 2.0, 2.25, 2.5, 3.0, 4.0]:
    found = False
    for a in np.linspace(0.02, 0.30, 40):
        bs = np.linspace(a+0.3, 0.999, 200)
        E = np.array([rtau_val(a, b, R) for b in bs])
        for i in range(len(bs)-1):
            if E[i]*E[i+1] < 0 and abs(a+0.5*(bs[i]+bs[i+1])-1) > 0.01:
                found = True
                break
        if found: break
    print(f"R={R:5.2f}: off-axis E=0 branch exists: {found}")
