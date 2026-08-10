import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import R1R2, a_fp, A0, B0, partials
from e14_authoritative import b_roots, arm_b, find_fold

for R in [4.0, 10000.0, 100000.0]:
    fp = a_fp(R)
    print("=== R=%g fp=%.6f ===" % (R, fp))
    # walk down from fp
    a, b = fp, 1 - fp
    steps = []
    for a_dec in np.linspace(fp, 0.002, 300)[1:]:
        bnew = arm_b(float(a_dec), R, coarse=True)
        if bnew is None or abs(bnew - b) > 0.04:
            steps.append((float(a_dec), None, bnew))
            break
        steps.append((float(a_dec), float(bnew), None))
        a, b = float(a_dec), bnew
    print("down-walk last 3:", steps[-3:])
    ff = find_fold(R, (a, b))
    print("fold from walk seed:", ff)
    # roots at a0
    rs = [r for r in b_roots(A0, R) if r - A0 > 0.0003]
    print("roots at a0:", ["%.5f" % r for r in rs])
    # roots at a = 0.42, 0.43
    for aq in [0.42, 0.43, 0.45, 0.50]:
        rsq = [r for r in b_roots(aq, R) if r - aq > 0.0003]
        print("a=%.2f roots=%s" % (aq, ["%.5f" % r for r in rsq]))
