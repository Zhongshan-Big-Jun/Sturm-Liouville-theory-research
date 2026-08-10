import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
import e15_authoritative as e15
from c1trace_lib import a_fp, R1R2, partials

R = 1000.0
fp = a_fp(R)
s1, s2 = e15.s12_full(fp, 1-fp, R)
print("fp=%.6f s1=%.8f s2=%.8f" % (fp, s1, s2))
# test scan at first up column
a_new = fp + 0.002
b_lo, b_hi = (1-fp) - 0.08, (1-fp) + 0.08
rs, (ns1, ns2) = e15.scan_roots(a_new, b_lo, b_hi, R, 500, s1, s2)
print("scan roots:", ["%.6f" % r for r in rs], "ns1=%.6f ns2=%.6f" % (ns1, ns2))
# what is R1(a_new, b) near the arm?  scan directly
for b in np.linspace(0.500, 0.506, 13):
    print("b=%.4f R1=%.3e" % (b, R1R2(a_new, float(b), R)[4]))
