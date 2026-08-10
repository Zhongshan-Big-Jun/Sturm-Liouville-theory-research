# -*- coding: utf-8 -*-
"""explore_3.py: D_ww/D_tt near the fixed point and along branches; locate positivity."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1_lib as L
from explore_1 import roots2_adaptive, cfg2, R1R2, partials2, hessian2, Dval

def a_fp(R, lo=0.40, hi=0.5):
    for _ in range(90):
        m = 0.5*(lo+hi)
        r1,_ = R1R2(m, 1.0-m, R)
        if np.signbit(r1) == np.signbit(R1R2(lo,1.0-lo,R)[0]):
            lo = m
        else:
            hi = m
    return 0.5*(lo+hi)

def g1_at(a, R, b_lo=None, b_hi=None):
    """branch1 root: R1(a,b)=0, v(a)>0. Bisection on b."""
    # find bracket: R1(a,b) as function of b
    if b_lo is None: b_lo = a + 1e-6
    if b_hi is None: b_hi = 1.0 - 1e-6
    def f(b): return R1R2(a, b, R)[0]
    flo = f(b_lo); fhi = f(b_hi)
    # bracket search
    if flo*fhi > 0:
        # scan
        bs = np.linspace(b_lo, b_hi, 2000)
        vals = np.array([R1R2(a,bb,R)[0] for bb in bs])
        ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
        idx = np.nonzero(ch)[0]
        if len(idx)==0: return None
        b_lo, b_hi = bs[idx[0]], bs[idx[0]+1]
        flo = f(b_lo)
    for _ in range(90):
        m = 0.5*(b_lo+b_hi)
        if np.signbit(f(m)) == np.signbit(flo): b_lo = m
        else: b_hi = m
    return 0.5*(b_lo+b_hi)

if __name__ == "__main__":
    print("fp and curvature at fp:")
    for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e6]:
        fp = a_fp(R)
        Daa,Dab,Dbb,p = hessian2(fp, 1.0-fp, R)
        Dww = (Daa-2*Dab+Dbb)/4.0; Dtt = (Daa+2*Dab+Dbb)/4.0
        print(f"  R={R:9g}: fp={fp:.7f} D_ww={Dww:+.6e} D_tt={Dtt:+.6e} "
              f"(A={p['A']:+.4e} B={p['B']:+.4e} C={p['C']:+.4e})")
    print()
    print("axis profile near fp (a in [0.40, 0.50)):")
    for R in [4.0, 1000.0, 1e4]:
        fp = a_fp(R)
        print(f"  R={R:9g}: fp={fp:.7f}")
        for a in [0.40, 0.42, 0.44, 0.46, 0.48, 0.49, 0.495, fp-5e-4, fp-1e-4, fp, fp+1e-4]:
            if a <= 0 or a >= 0.5: continue
            Daa,Dab,Dbb,p = hessian2(a, 1.0-a, R)
            Dww = (Daa-2*Dab+Dbb)/4.0; Dtt = (Daa+2*Dab+Dbb)/4.0
            print(f"    a={a:.7f}: D_ww={Dww:+.4e} D_tt={Dtt:+.4e}")
