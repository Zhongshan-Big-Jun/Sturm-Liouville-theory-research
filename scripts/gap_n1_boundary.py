# -*- coding: utf-8 -*-
"""gap_n1_boundary.py: dense scan of 2-block D(t); verify D* bounds."""
import numpy as np
from gap_lib import lams_fast

def D_of(blocks):
    s = lams_fast(blocks, 2)
    return s[1]**2 - s[0]**2

def sym_D(R, mode, u):
    bl = [(u,1.0),(1-2*u,R),(u,1.0)] if mode=="SUP" else [(u,R),(1-2*u,1.0),(u,R)]
    return D_of(bl)

# known symmetric self-consistent points from session 5 / this session
ustar = {1.5: (0.429832, 0.408814), 2.0: (0.436696, 0.401037), 3.0: (0.445665, 0.390127),
         4.0: (0.451485, 0.382598), 10.0: (0.466931, 0.361313), 100.0: (0.4769, 0.334804)}
print("R    max2block_D  D*SUP     3pi^2     |  min2block_D  D*INF     3pi^2/R")
for R in (1.5, 2.0, 3.0, 4.0, 10.0):
    # dense scan of 2-block configs
    tvals = np.linspace(0.0005, 0.9995, 900)
    Ds = np.array([max(D_of([(t,1.0),(1-t,R)]), D_of([(t,R),(1-t,1.0)])) for t in tvals])
    Dsmin = np.array([min(D_of([(t,1.0),(1-t,R)]), D_of([(t,R),(1-t,1.0)])) for t in tvals])
    mx2 = Ds.max(); mn2 = Dsmin.min()
    uS, uI = ustar[R]
    DsS = sym_D(R, "SUP", uS); DsI = sym_D(R, "INF", uI)
    print(f"{R:5.1f}  {mx2:10.4f}  {DsS:9.4f}  {3*np.pi**2:8.4f}  |  {mn2:10.4f}  {DsI:9.4f}  {3*np.pi**2/R:8.4f}")
    print(f"       margins: D*SUP-3pi^2={DsS-3*np.pi**2:+.4f} ; 3pi^2/R-D*INF={3*np.pi**2/R-DsI:+.4f}")
