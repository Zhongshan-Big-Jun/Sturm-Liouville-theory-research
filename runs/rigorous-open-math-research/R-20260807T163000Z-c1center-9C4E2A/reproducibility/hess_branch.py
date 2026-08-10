# -*- coding: utf-8 -*-
"""hess_branch.py: signs of D_aa, D_ab, D_bb and rotated Hessian along the fp-branch."""
import numpy as np, sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n, y_at
from c1trace_lib import R1R2, a_fp, A0, B0, partials
from trace_w import trace_w, newton_w

def D_partials(a, b, R, cache=None):
    R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
    # dD/da = -(R-1) R1 ; dD/db = (R-1) R2  (P1)
    # D_aa = -(R-1) R1_a ; D_ab = (R-1) R2_a ; D_bb = (R-1) R2_b
    return -(R-1)*R1a, (R-1)*R2a, (R-1)*R2b

for R in [1.2, 4.0, 100.0, 1000.0, 10000.0, 100000.0]:
    cache = {}
    fp = a_fp(R, cache=cache)
    pts = trace_w(R, A0, B0, nstep=600, cache=cache)
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
    keep = [0]
    for i in range(1, len(aa)):
        if aa[i] > aa[keep[-1]] + 1e-12: keep.append(i)
    aa = aa[keep]; bb = bb[keep]
    nz = len(aa)
    Daa = np.zeros(nz); Dab = np.zeros(nz); Dbb = np.zeros(nz)
    for i in range(nz):
        Daa[i], Dab[i], Dbb[i] = D_partials(aa[i], bb[i], R, cache=cache)
    Dww = (Daa - 2*Dab + Dbb)/4
    Dtt = (Daa + 2*Dab + Dbb)/4
    # G = -Daa/Dab should match branch slope
    G = -Daa/Dab
    print("R=%g n=%d" % (R, nz))
    print("  Daa: min=%.4e max=%.4e  sign=%s" % (Daa.min(), Daa.max(), "all<0" if (Daa<0).all() else "mixed"))
    print("  Dab: min=%.4e max=%.4e  sign=%s" % (Dab.min(), Dab.max(), "all>0" if (Dab>0).all() else "mixed"))
    print("  Dbb: min=%.4e max=%.4e  sign=%s" % (Dbb.min(), Dbb.max(), "all<0" if (Dbb<0).all() else "mixed"))
    print("  Dww: min=%.4e max=%.4e ; Dtt: min=%.4e max=%.4e" % (Dww.min(), Dww.max(), Dtt.min(), Dtt.max()))
    print("  G from Hessian: min=%.5f max=%.5f" % (G.min(), G.max()))
