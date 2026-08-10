# -*- coding: utf-8 -*-
import sys, math
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import numpy as np
from gap_lib import lams_fast

R = 4.0
for u in [0.05, 0.1, 0.2, 0.3, 0.4, 0.45, 0.5-1e-3]:
    blocks = [(u,1.0),(1-2*u,R),(u,1.0)]
    s = lams_fast(blocks, 2, npts=40000)
    print("u=%.3f: lam1=%.6f lam2=%.6f D=%.6f" % (u, s[0]**2, s[1]**2, s[1]**2-s[0]**2))