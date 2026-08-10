import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from fast_lib import sec, roots2_fast, y_at, norm_n
from c1trace_lib import R1R2, a_fp, A0, B0, partials
from e14_authoritative import b_roots, arm_b

R = 4.0
fp = a_fp(R)
print("fp =", fp, "1-fp =", 1-fp)
# scan the arm: for a grid, list all roots with b-a > 0.0005
for a in np.linspace(0.30, 0.60, 61):
    rs = [r for r in b_roots(a, R) if r - a > 0.0005]
    print("a=%.4f roots=%s" % (a, ["%.4f" % r for r in rs]))
