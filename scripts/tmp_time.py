import time, numpy as np
from gap_lib import lams_fast, y_at, norm2
bl = [(0.45,1.0),(0.1,4.0),(0.45,1.0)]
for npts in (6000, 12000, 30000):
    t0=time.time(); s=lams_fast(bl,2,npts=npts); t1=time.time()
    print(npts, s, f"{t1-t0:.3f}s")
