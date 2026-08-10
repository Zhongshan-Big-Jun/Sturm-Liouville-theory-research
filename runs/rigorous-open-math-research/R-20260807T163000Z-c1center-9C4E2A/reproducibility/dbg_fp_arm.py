import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import a_fp, R1R2, partials
from fast_lib import roots2_fast

R = 1000.0
fp = a_fp(R)
print("fp=%.6f  R1(fp,1-fp)=%.3e" % (fp, R1R2(fp, 1-fp, R)[4]))
# find arm roots at a = fp +/- delta by scanning R1 with correct roots2_fast
for a in [fp-0.002, fp-0.001, fp, fp+0.001, fp+0.002]:
    bvals = np.linspace(0.45, 0.56, 1101)
    R1v = np.array([R1R2(a, float(b), R)[4] for b in bvals])
    roots = []
    for i in range(len(bvals)-1):
        if R1v[i]*R1v[i+1] < 0:
            lo, hi = bvals[i], bvals[i+1]; flo = R1v[i]
            for _ in range(50):
                md = 0.5*(lo+hi)
                if R1R2(a, md, R)[4]*flo < 0: hi = md
                else: lo = md
            roots.append(0.5*(lo+hi))
    print("a=%.6f: R1 roots in b: %s" % (a, ["%.6f" % r for r in roots]))
# slope at fp
R1a, R1b, R2a, R2b = partials(fp, 1-fp, R)
print("at fp: R1a=%.3e R1b=%.3e g1p=-R1a/R1b=%.6f" % (R1a, R1b, -R1a/R1b))
