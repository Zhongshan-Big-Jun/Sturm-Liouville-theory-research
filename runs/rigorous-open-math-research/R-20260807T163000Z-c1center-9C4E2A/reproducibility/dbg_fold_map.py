import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import R1R2, a_fp
from fast_lib import roots2_fast, norm_n

R = 1000.0
# exhaustive: for a in fine grid, find ALL b-roots of R1 via fine b scan
def all_roots_col(a, R, nb=3000):
    b_arr = np.linspace(a+1e-5, 1-1e-4, nb)
    roots = []
    R1prev = None; bprev = None
    for j in range(nb):
        b = b_arr[j]
        s1, s2 = roots2_fast(a, float(b), R)
        n1 = norm_n(s1, a, float(b), R); n2 = norm_n(s2, a, float(b), R)
        R1 = np.sin(s1*a)**2/n1 - np.sin(s2*a)**2/n2
        if R1prev is not None and R1*R1prev < 0:
            lo, hi = bprev, b
            for _ in range(55):
                md = 0.5*(lo+hi)
                s1m, s2m = roots2_fast(a, md, R)
                n1m = norm_n(s1m, a, md, R); n2m = norm_n(s2m, a, md, R)
                R1m = np.sin(s1m*a)**2/n1m - np.sin(s2m*a)**2/n2m
                if R1m*R1prev < 0: hi = md
                else: lo = md
            roots.append(0.5*(lo+hi))
        R1prev = R1; bprev = b
    return roots

for a in np.linspace(0.4180, 0.4290, 111):
    rs = all_roots_col(a, R)
    if rs:
        print("a=%.4f: %s" % (a, ["%.5f" % r for r in rs]))
