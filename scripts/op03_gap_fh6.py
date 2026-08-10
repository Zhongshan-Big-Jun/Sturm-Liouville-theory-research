import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.45
eps = 0.01
v0 = 1-2*u
# base: [1,R,1] with blocks (u,1),(v0,R),(u,1); perturb density on (u, u+eps): R -> R + t*(1-R)
def lams_t(t):
    blocks = [(u,1.0), (eps, R + t*(1-R)), (v0-eps, R), (u,1.0)]
    return lams_precise(blocks, 3)**2
lam0 = lams_t(0.0)
vp = eigfuns_precise([(u,1.0),(v0,R),(u,1.0)], np.sqrt(lam0[:2]), np.array([u]))
# FH: d lam/dt = -lam*(1-R)*u(u)^2*eps
pred = -lam0[:2]*(1-R)*np.array([vp[0,0]**2, vp[1,0]**2])*eps
print("pred (total over t in [0,1]):", pred)
for t in (0.5, 1.0):
    num = (lams_t(t) - lam0)/t
    print(f"t={t}: num avg = {num[:2]}")
