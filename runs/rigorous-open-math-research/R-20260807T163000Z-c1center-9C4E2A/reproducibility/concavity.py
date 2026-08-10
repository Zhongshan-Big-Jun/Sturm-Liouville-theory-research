# -*- coding: utf-8 -*-
"""concavity.py: test D_aa, D_bb, det(Hess) signs over the full triangle for several R."""
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n, y_at
from c1trace_lib import R1R2, partials

def D_hess(a, b, R):
    R1a, R1b, R2a, R2b = partials(a, b, R)
    Daa = -(R-1)*R1a; Dab = (R-1)*R2a; Dbb = (R-1)*R2b
    return Daa, Dab, Dbb

for R in [1.2, 4.0, 100.0, 1000.0]:
    ng = 40
    aa = np.linspace(0.01, 0.98, ng)
    worst = {}
    counts = dict(Daa_neg=0, Dbb_neg=0, det_pos=0, total=0)
    for a in aa:
        for b in np.linspace(a+0.005, 0.99, ng):
            Daa, Dab, Dbb = D_hess(a, b, R)
            det = Daa*Dbb - Dab**2
            counts["total"] += 1
            if Daa < 0: counts["Daa_neg"] += 1
            if Dbb < 0: counts["Dbb_neg"] += 1
            if det > 0: counts["det_pos"] += 1
            key = "Daa>0" if Daa > 0 else None
            if key: worst.setdefault(key, (a, b, Daa))
            key2 = "det<0" if det < 0 else None
            if key2: worst.setdefault(key2, (a, b, det))
    print("R=%g: Daa<0 in %d/%d, Dbb<0 in %d/%d, det>0 in %d/%d" % (
        R, counts["Daa_neg"], counts["total"], counts["Dbb_neg"], counts["total"], counts["det_pos"], counts["total"]))
    for k, v in worst.items():
        print("   worst %s at (a,b)=(%.4f,%.4f) val=%.4e" % (k, v[0], v[1], v[2]))
