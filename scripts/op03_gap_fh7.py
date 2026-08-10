import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.45
v0 = 1-2*u
blocks0 = [(u,1.0),(v0,R),(u,1.0)]
lam0 = lams_precise(blocks0, 3)**2
vp = eigfuns_precise(blocks0, np.sqrt(lam0[:2]), np.array([u]))
u1s = vp[0,0]**2; u2s = vp[1,0]**2

def lams_t(t, eps):
    blocks = [(u,1.0), (eps, R + t*(1-R)), (v0-eps, R), (u,1.0)]
    return lams_precise(blocks, 3)**2

for eps in (0.01, 0.001, 0.0001):
    num1 = (lams_t(1.0, eps)[0] - lam0[0])
    num2 = (lams_t(1.0, eps)[1] - lam0[1])
    fh1 = -lam0[0]*(1-R)*u1s*eps
    fh2 = -lam0[1]*(1-R)*u2s*eps
    print(f"eps={eps}: num dL1={num1:+.6f} FH={fh1:+.6f} | num dL2={num2:+.6f} FH={fh2:+.6f}")
