# -*- coding: utf-8 -*-
"""Count zeros of f(v) on symmetric line (0,1/2) for several R (E3)."""
import numpy as np
from scipy.optimize import brentq
from _well_landscape2 import eigs_well, fval

def fzeros(R):
    vs = np.linspace(1e-4, 0.4999, 3001)
    fv = np.array([fval(v, 1-v, R, v) for v in vs])
    zs = []
    for i in range(len(vs)-1):
        if fv[i]*fv[i+1] < 0:
            zs.append(brentq(lambda v: fval(v, 1-v, R, v), vs[i], vs[i+1]))
    return zs

for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0]:
    zs = fzeros(R)
    print(f"R={R:6.1f}: f zeros on (0,1/2): {len(zs)} {[round(z,5) for z in zs]}")
# also verify D endpoints
for R in [2.0, 4.0]:
    lam0 = eigs_well(1e-4, 1-1e-4, R)   # near rho==1
    lam1 = eigs_well(0.4999, 0.5001, R) # near rho==R
    print(f"R={R}: D(v->0)={lam0[1]-lam0[0]:.4f} vs 3pi^2={3*np.pi**2:.4f}; D(v->1/2)={lam1[1]-lam1[0]:.4f} vs 3pi^2/R={3*np.pi**2/R:.4f}")
