import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.45
v0 = 1-2*u
blocks0 = [(u,1.0),(v0,R),(u,1.0)]
lam0 = lams_precise(blocks0, 3)**2
a, b = 0.48, 0.49
def lams_c(c):
    blocks = [(u,1.0),(a-u,R),(b-a,R+c),(1-u-b,R),(u,1.0)]
    return lams_precise(blocks, 3)**2
vp = eigfuns_precise(blocks0, np.sqrt(lam0[:2]), np.array([0.485]))
I1 = vp[0,0]**2*(b-a); I2 = vp[1,0]**2*(b-a)
print("lam0:", lam0[:2])
for c in (0.01, 0.1):
    num = (lams_c(c)[:2]-lam0[:2])/c
    fh = -lam0[:2]*np.array([I1, I2])
    print(f"c={c}: num={num}  FH={fh}")

# junction perturbation again with correct widths
def lams_junc(eps):
    blocks = [(u,1.0),(eps,R + (1-R)),(v0-eps,R),(u,1.0)]
    return lams_precise(blocks, 3)**2
vp2 = eigfuns_precise(blocks0, np.sqrt(lam0[:2]), np.array([u]))
for eps in (0.001, 0.0001):
    num = (lams_junc(eps)[:2]-lam0[:2])
    fh = -lam0[:2]*(1-R)*np.array([vp2[0,0]**2, vp2[1,0]**2])*eps
    print(f"junc eps={eps}: num={num}  FH={fh}")
