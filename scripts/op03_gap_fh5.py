import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.45
def lams_asym(u, eps):
    v = 1 - 2*u - eps
    blocks = [(u+eps, 1.0), (v, R), (u, 1.0)]
    return lams_precise(blocks, 3)**2

v0 = 1-2*u
blocks0 = [(u,1.0),(v0,R),(u,1.0)]
lam0 = lams_precise(blocks0, 3)**2
vp = eigfuns_precise(blocks0, np.sqrt(lam0[:2]), np.array([u]))
pred = -lam0[:2]*(1-R)*np.array([vp[0,0]**2, vp[1,0]**2])
print("pred:", pred)
for eps in (1e-4, 1e-5, 1e-6):
    lamE = lams_asym(u, eps)
    print(f"eps={eps}: num={ (lamE[:2]-lam0[:2])/eps }")
