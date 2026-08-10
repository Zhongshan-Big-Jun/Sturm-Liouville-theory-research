# -*- coding: utf-8 -*-
"""2-block family D(t) monotonicity check + lambda_1(t), lambda_2(t), ratio."""
import numpy as np
from gap_lib import lams_fast

def lams2(blocks, npts=120000):
    return lams_fast(blocks, 2, npts=npts)**2

R = 4.0
t3 = 3*np.pi**2
for R in (2.0, 4.0, 100.0):
    print(f"==== R={R} ====")
    for name, blfun in (("[1,R]_t", lambda t: [(t,1.0),(1-t,R)]), ("[R,1]_t", lambda t: [(t,R),(1-t,1.0)])):
        ts = np.linspace(0.001, 0.999, 500)
        L = np.array([lams2(blfun(t)) for t in ts])
        D = L[:,1]-L[:,0]
        dD = np.diff(D)
        mono_up = np.all(dD >= -1e-9)
        mono_dn = np.all(dD <= 1e-9)
        print(f"  {name}: D range [{D.min():.5f},{D.max():.5f}]  monotone increasing: {mono_up}, decreasing: {mono_dn}")
        print(f"        min D at t*={ts[int(np.argmin(D))]:.4f}, max at t*={ts[int(np.argmax(D))]:.4f}")
        print(f"        lam1 range [{L[:,0].min():.5f},{L[:,0].max():.5f}], lam2 range [{L[:,1].min():.5f},{L[:,1].max():.5f}]")
