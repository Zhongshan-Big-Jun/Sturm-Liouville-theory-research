import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import R1R2, a_fp
from fast_lib import roots2_fast, norm_n

R = 1000.0
def all_roots_col(a, R, nb=2000):
    b_arr = np.linspace(a+1e-5, 1-1e-4, nb)
    roots = []
    R1prev = None; bprev = None
    for j in range(nb):
        b = b_arr[j]
        s1, s2 = roots2_fast(a, float(b), R)
        n1 = norm_n(s1, a, float(b), R); n2 = norm_n(s2, a, float(b), R)
        R1 = np.sin(s1*a)**2/n1 - np.sin(s2*a)**2/n2
        if R1prev is not None and R1*R1prev < 0:
            roots.append(0.5*(bprev+b))
        R1prev = R1; bprev = b
    return roots

for a in [0.10, 0.20, 0.30, 0.35, 0.38, 0.40, 0.41, 0.412, 0.413, 0.414, 0.415, 0.416, 0.417, 0.418]:
    rs = all_roots_col(a, R)
    print("a=%.3f: %s" % (a, ["%.5f" % r for r in rs]))
