import time, numpy as np
from gap_lib import lams_fast, y_at, norm2
bl = [(0.45,1.0),(0.1,4.0),(0.45,1.0)]
t0=time.time()
for i in range(50):
    s = lams_fast(bl, 2, npts=8000)
    lam = s**2
    u1a = y_at(bl, s[0], np.array([0.3]))[0]/np.sqrt(norm2(bl, s[0]))
    u2a = y_at(bl, s[1], np.array([0.3]))[0]/np.sqrt(norm2(bl, s[1]))
t1=time.time()
print("per-call:", (t1-t0)/50*1000, "ms")
