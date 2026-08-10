import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import R1R2, a_fp, A0, B0, partials
from e14_authoritative import b_roots

# fine column scan with small b-a threshold to see ALL components
for R in [886.0, 900.0, 1000.0, 2000.0]:
    fp = a_fp(R)
    print("=== R=%g fp=(%.5f,%.5f) ===" % (R, fp, 1-fp))
    for a in np.linspace(0.414, 0.436, 45):
        rs = [r for r in b_roots(a, R) if r > a + 1e-6]
        if rs:
            print("  a=%.4f roots=%s" % (a, ["%.5f" % r for r in rs]))
