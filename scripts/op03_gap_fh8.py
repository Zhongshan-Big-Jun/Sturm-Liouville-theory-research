import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.45
v0 = 1-2*u
blocks0 = [(u,1.0),(v0,R),(u,1.0)]
lam0 = lams_precise(blocks0, 3)**2
# test perturbation inside central block (0.48,0.49): rho R -> R + c
a, b = 0.48, 0.49
def lams_c(c):
    blocks = [(u,1.0),(a-u,R),(b-a,R+c),(1-b,R),(u,1.0)]
    return lams_precise(blocks, 3)**2
# FH: d lam/dc = -lam * int_(a,b) u^2 dx  (eta=1 on (a,b))
vp = eigfuns_precise(blocks0, np.sqrt(lam0[:2]), np.array([0.485]))
# int_a^b u^2 dx ~ u(0.485)^2 * (b-a) (fine for small interval)
I1 = vp[0,0]**2*(b-a); I2 = vp[1,0]**2*(b-a)
print("lam0:", lam0[:2])
for c in (0.01, 0.1):
    num = (lams_c(c)[:2]-lam0[:2])/c
    fh = -lam0[:2]*np.array([I1, I2])
    print(f"c={c}: num={num}  FH={fh}")
