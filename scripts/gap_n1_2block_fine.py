# -*- coding: utf-8 -*-
"""gap_n1_2block_fine.py: fine scan of D(t)-3pi^2 for 2-block configs (R=4)."""
import numpy as np
from gap_lib import lams_fast

def D_of(blocks):
    s = lams_fast(blocks, 2, npts=120000)
    return s[1]**2 - s[0]**2

R = 4.0
t3 = 3*np.pi**2
print("t        D([1,R]_t)      D([R,1]_t)      D-3pi^2 (max of two)")
worst = (0, None)
for t in np.linspace(0.001, 0.999, 400):
    d1 = D_of([(t,1.0),(1-t,R)])
    d2 = D_of([(t,R),(1-t,1.0)])
    dm = max(d1, d2)
    if dm - t3 > (worst[0] if worst[1] else -1):
        worst = (dm-t3, t)
    if abs(dm - t3) < 0.001 or t < 0.01 or t > 0.99:
        print(f"{t:7.3f}  {d1:12.6f}  {d2:12.6f}  {dm-t3:+.6f}")
print("worst excess over 3pi^2:", worst)
# also fine scan near t=0.95..1.0
ts = np.linspace(0.95, 0.9995, 100)
ex = max(D_of([(t,1.0),(1-t,R)]) - t3 for t in ts)
print("max D([1,R]_t)-3pi^2 for t in [0.95,0.9995]:", ex)
