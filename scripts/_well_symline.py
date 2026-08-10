# -*- coding: utf-8 -*-
"""Multi-R symmetric-line landscape + off-axis branch (E3 evidence only)."""
import numpy as np
from _well_landscape2 import eigs_well, fval

def sym_line(R, N=600):
    vs = np.linspace(1e-4, 0.4999, N)
    Ds = np.array([eigs_well(v, 1-v, R)[1]-eigs_well(v, 1-v, R)[0] for v in vs])
    i = int(np.argmin(Ds))
    return vs, Ds, i

for R in [1.05, 1.1, 1.5, 2.0, 3.0, 4.0, 10.0, 25.0, 100.0, 400.0]:
    vs, Ds, i = sym_line(R)
    vstar = vs[i]
    Dstar = Ds[i]
    # check monotonicity structure: Ds should decrease then increase
    # count local minima
    lm = np.sum((Ds[1:-1] < Ds[:-2]) & (Ds[1:-1] < Ds[2:]))
    const_R = 3*np.pi**2/R
    print(f"R={R:6.1f}: v*={vstar:.5f} D*={Dstar:.6f} 3pi^2/R={const_R:.6f} D*<3pi^2/R: {Dstar<const_R} local_mins={lm}")
