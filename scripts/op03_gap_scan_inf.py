import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
print("u, D, f at junction for [R,1,R]:")
for u in np.concatenate([np.linspace(0.01,0.10,10), np.linspace(0.12,0.30,10), np.linspace(0.32,0.49,9)]):
    v = 1-2*u
    blocks = [(u,R),(v,1.0),(u,R)]
    s = lams_precise(blocks, 3)
    lam = s**2
    vp = eigfuns_precise(blocks, s[:2], np.array([u]))
    f = lam[0]*vp[0,0]**2 - lam[1]*vp[1,0]**2
    print(f"u={u:.4f}  D={lam[1]-lam[0]:.6f}  f={f:+.4e}")
print(f"constant R: D = {3*np.pi**2/R:.6f}")
