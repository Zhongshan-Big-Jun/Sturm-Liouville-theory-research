import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import R1R2, A0
from e14_authoritative import b_roots
from fast_lib import sec, roots2_fast

R = 1000.0; a = A0
print("b_roots(a0,1000):", b_roots(a, R))
# manual: scan b in [0.4205, 0.4225]
for b in np.linspace(0.4206, 0.4224, 19):
    s1, s2 = roots2_fast(a, float(b), R)
    print("b=%.5f s1=%.6f s2=%.6f R1=%.4e R2=%.4e" % (b, s1, s2, *R1R2(a, float(b), R)[4:]))
