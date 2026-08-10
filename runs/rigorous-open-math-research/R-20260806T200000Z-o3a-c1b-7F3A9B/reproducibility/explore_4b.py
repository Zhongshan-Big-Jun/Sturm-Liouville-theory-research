# -*- coding: utf-8 -*-
"""explore_4b.py: faster comprehensive data (vectorized scans, memoized cfg)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1_lib as L
from explore_1 import roots2_adaptive, cfg2, R1R2, partials2, hessian2, Dval

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0
_cfg_memo = {}
def cfg_m(a,b,R):
    key = (round(a,10), round(b,10), R)
    if key not in _cfg_memo:
        _cfg_memo[key] = cfg2(a,b,R)
    return _cfg_memo[key]

def R1R2m(a,b,R):
    s1,s2,n1,n2 = cfg_m(a,b,R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = L.y_at(s1,a,b,R,b); y2b = L.y_at(s2,a,b,R,b)
    return s1**2*y1a**2/n1 - s2**2*y2a**2/n2, s1**2*y1b**2/n1 - s2**2*y2b**2/n2

def a_fp(R, lo=0.40, hi=0.5):
    r0 = R1R2m(lo,1.0-lo,R)[0]
    for _ in range(80):
        m = 0.5*(lo+hi)
        if np.signbit(R1R2m(m,1.0-m,R)[0]) == np.signbit(r0): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def roots1_scan(a, R, ns=1200):
    bs = np.linspace(a+1e-4, 1.0-1e-4, ns)
    vals = np.empty(ns)
    for i,b in enumerate(bs):
        vals[i] = R1R2m(a, b, R)[0]
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    roots = []
    for i in np.nonzero(ch)[0]:
        lo, hi = bs[i], bs[i+1]
        flo = R1R2m(a,lo,R)[0]
        for _ in range(70):
            md = 0.5*(lo+hi)
            if np.signbit(R1R2m(a,md,R)[0]) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    return roots

def main():
    for R in [2.0, 4.0, 100.0, 1000.0, 1e4]:
        fp = a_fp(R)
        print(f"=== R={R:9g} fp={fp:.7f} a0={A0:.5f} b0={B0:.5f} ===")
        for a in np.linspace(A0, min(0.5, fp+0.005), 9):
            roots = roots1_scan(a, R, ns=1500)
            if not roots:
                print(f"  a={a:.4f}: no R1 roots"); continue
            sel = None
            for b in roots:
                s1,s2 = roots2_adaptive(a,b,R)
                if (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1) > 0:
                    sel = b
            if sel is None:
                print(f"  a={a:.4f}: roots {[round(r,5) for r in roots]} no v(a)>0"); continue
            r2 = R1R2m(a, sel, R)[1]
            try:
                p = partials2(a, sel, R)
                g1p = p['A']/p['B']
                print(f"  a={a:.4f}: g1={sel:.6f} R2={r2:+.2e} g1'={g1p:.5f}")
            except Exception as e:
                print(f"  a={a:.4f}: g1={sel:.6f} R2={r2:+.2e} partials failed")
    print()
    print("axis R1_sym(a):")
    for R in [1.05, 4.0, 100.0, 1000.0, 1e4]:
        fp = a_fp(R)
        row = []
        for a in [0.30, 0.36, 0.40, 0.42, 0.44, 0.46, 0.48, 0.49, 0.494, 0.497, 0.499]:
            if a >= 0.5: continue
            r1, r2 = R1R2m(a, 1.0-a, R)
            row.append(f"a={a:.3f}:{r1:+.2e}")
        print(f"  R={R:9g} fp={fp:.6f}: " + " ".join(row))

if __name__ == "__main__":
    main()
