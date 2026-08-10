# -*- coding: utf-8 -*-
"""Test d lambda_k/du = -lambda_k (1-R) u_k(u)^2 for left-junction move."""
import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.45
def lams_asym(u, eps):
    v = 1 - 2*u - eps
    blocks = [(u+eps, 1.0), (v, R), (u, 1.0)]
    s3 = lams_precise(blocks, 3)
    return s3**2

# base config
v0 = 1-2*u
blocks0 = [(u,1.0),(v0,R),(u,1.0)]
s0 = lams_precise(blocks0, 3)
lam0 = s0**2
vp = eigfuns_precise(blocks0, s0[:2], np.array([u]))
print("lam:", lam0[:2])
print("u_k(u)^2:", vp[0,0]**2, vp[1,0]**2)
for eps in (1e-4, 1e-5):
    lamE = lams_asym(u, eps)
    num = (lamE - lam0)/eps
    pred = -lam0*(1-R)*np.array([vp[0,0]**2, vp[1,0]**2])
    print(f"eps={eps}: num dlam/du={num[:2]}  pred={pred[:2]}")
