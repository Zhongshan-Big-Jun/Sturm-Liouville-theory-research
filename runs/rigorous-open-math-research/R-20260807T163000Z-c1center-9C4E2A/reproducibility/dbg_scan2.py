import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from e14_authoritative import b_roots

for R in [888.0, 900.0, 920.0, 950.0, 1000.0]:
    print("=== R=%g ===" % R)
    for a in np.linspace(0.4180, 0.4290, 56):
        rs = [r for r in b_roots(a, R) if r > a + 1e-6]
        if rs:
            print("  a=%.4f roots=%s" % (a, ["%.5f" % r for r in rs]))
