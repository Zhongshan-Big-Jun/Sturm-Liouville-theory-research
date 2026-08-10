import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.30
# [1,R,1] base: blocks (u,1),(1-2u,R),(u,1)
v0 = 1-2*u
base = [(u,1.0),(v0,R),(u,1.0)]
lam0 = lams_precise(base, 3)**2
print("base lam:", lam0[:2])

# perturb: move LEFT junction right by eps: (0,u+eps)=1,(u+eps,1-u)=R,(1-u,1)=1
eps = 1e-5
pert = [(u+eps,1.0),(v0-eps,R),(u,1.0)]
lamP = lams_precise(pert, 3)**2
print("pert lam:", lamP[:2], " dlam:", (lamP[:2]-lam0[:2])/eps)

# FH: dlam_k = -lam_k * (1-R) * u_k(u)^2
vp = eigfuns_precise(base, np.sqrt(lam0[:2]), np.array([u]))
pred = -lam0[:2]*(1-R)*np.array([vp[0,0]**2, vp[1,0]**2])
print("FH pred dlam:", pred)
print("u_k(u)^2:", vp[0,0]**2, vp[1,0]**2)
print("norm check: int rho u^2 = 1 expected; lam ratio check: lambda1*int u1^2 = ", end="")
