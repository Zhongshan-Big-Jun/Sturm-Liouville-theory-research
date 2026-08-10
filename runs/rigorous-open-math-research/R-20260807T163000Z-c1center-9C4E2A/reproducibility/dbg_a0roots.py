import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import R1R2, A0, B0

# direct scan of R1(A0, b) over b
for R in [880.0, 888.0, 900.0, 920.0, 950.0, 1000.0, 2000.0]:
    vals = []
    for b in np.linspace(A0+1e-4, 1-1e-4, 4001):
        vals.append((b, R1R2(A0, float(b), R)[4]))
    # find sign changes
    z = []
    for i in range(len(vals)-1):
        if vals[i][1]*vals[i+1][1] < 0:
            lo, hi = vals[i][0], vals[i+1][0]
            for _ in range(50):
                md = 0.5*(lo+hi)
                if R1R2(A0, md, R)[4]*R1R2(A0, lo, R)[4] < 0: hi = md
                else: lo = md
            z.append(0.5*(lo+hi))
    print("R=%g: R1(A0,b)=0 roots at b = %s" % (R, ["%.5f" % x for x in z]))
