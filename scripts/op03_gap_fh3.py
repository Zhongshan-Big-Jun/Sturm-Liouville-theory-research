# -*- coding: utf-8 -*-
"""FH test corrected: perturbation on (0.4,0.5)."""
import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

blocks0 = [(1.0, 1.0)]
s = lams_precise(blocks0, 2)
a, b = 0.4, 0.5
I = 2*( (b-a)/2 - (np.sin(2*np.pi*b)-np.sin(2*np.pi*a))/(4*np.pi) )
print("int_0.4^0.5 u1^2 =", I)
for c in (0.001, 0.01):
    blocks = [(a, 1.0), (b-a, 1.0+c), (1-b, 1.0)]
    s2 = lams_precise(blocks, 2)
    num = (s2[0]**2 - s[0]**2)/c
    fh = -s[0]**2 * I
    print(f"c={c}: num dL1/dc={num:.6f}  FH={fh:.6f}")

# Now moving junction test for [1,R,1]: dD/du with left junction only (asymmetric move)
# config for u+eps: blocks [(u+eps,1),(1-u-(u+eps),R),(u,1)] -- central band shrinks on left only
R = 4.0
def D_asym(u, eps=0.0):
    v = 1 - 2*u - eps
    blocks = [(u+eps, 1.0), (v, R), (u, 1.0)]
    s3 = lams_precise(blocks, 3)
    return s3[1]**2 - s3[0]**2
def f_junc(u):
    v = 1-2*u
    blocks = [(u,1.0),(v,R),(u,1.0)]
    s3 = lams_precise(blocks, 3)
    lam = s3**2
    vp = eigfuns_precise(blocks, s3[:2], np.array([u]))
    return lam[0]*vp[0,0]**2 - lam[1]*vp[1,0]**2
for u in (0.40, 0.45, 0.458):
    eps = 1e-6
    num = (D_asym(u, eps) - D_asym(u, 0))/eps
    f = f_junc(u)
    print(f"u={u}: dD/du_left-only={num:+.4e}  (1-R)*f(u)={ (1-R)*f:+.4e}")
