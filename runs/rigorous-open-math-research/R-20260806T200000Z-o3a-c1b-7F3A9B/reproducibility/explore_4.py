# -*- coding: utf-8 -*-
"""explore_4.py: comprehensive data on branches, h, h', axis problem, curves S/T."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1_lib as L
from explore_1 import roots2_adaptive, cfg2, R1R2, partials2, hessian2, Dval

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0

def a_fp(R, lo=0.40, hi=0.5):
    r0 = R1R2(lo,1.0-lo,R)[0]
    for _ in range(90):
        m = 0.5*(lo+hi)
        if np.signbit(R1R2(m,1.0-m,R)[0]) == np.signbit(r0): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def branch1_root(a, R, b_lo=None, b_hi=None, want='R1'):
    if b_lo is None: b_lo = a + 1e-5
    if b_hi is None: b_hi = 1.0 - 1e-5
    def f(b):
        r1, r2 = R1R2(a, b, R)
        return r1 if want=='R1' else r2
    bs = np.linspace(b_lo, b_hi, 4000)
    vals = np.array([f(bb) for bb in bs])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx:
        lo, hi = bs[i], bs[i+1]
        flo = f(lo)
        for _ in range(80):
            md = 0.5*(lo+hi)
            if np.signbit(f(md)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    return roots

def main():
    Rvals = [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e6]
    for R in Rvals:
        fp = a_fp(R)
        # g1 at a grid: main sheet (largest branch-1 root? or the one with v(a)>0)
        # Use the reflection formula structure: g1 root selection via v(a)>0
        print(f"=== R={R:9g} fp={fp:.7f} ===")
        # scan g1 roots on [A0, fp+0.02]
        for a in np.linspace(A0, min(0.5, fp+0.005), 7):
            roots = branch1_root(a, R, want='R1')
            if len(roots) == 0:
                print(f"  a={a:.4f}: no R1 roots")
                continue
            # select main sheet: v(a)>0
            sel = None
            for b in roots:
                s1,s2 = roots2_adaptive(a,b,R)
                v_a = (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1)
                if v_a > 0:
                    sel = b
            if sel is None:
                print(f"  a={a:.4f}: roots {roots} none with v(a)>0")
                continue
            g1p = None
            try:
                p = partials2(a, sel, R)
                g1p = p['A']/p['B']
            except Exception as e:
                pass
            r2 = R1R2(a, sel, R)[1]
            print(f"  a={a:.4f}: g1={sel:.6f} R2_on_g1={r2:+.3e} g1'={g1p if g1p is None else round(g1p,4)}")
    print()
    # axis problem data
    print("axis problem R1_sym(a) (a from 0.36 to 0.499):")
    for R in [1.05, 4.0, 100.0, 1000.0, 1e4]:
        fp = a_fp(R)
        print(f"  R={R:9g} fp={fp:.6f}:")
        for a in [0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48, 0.49, 0.495, 0.498]:
            if a >= 0.5: continue
            r1, r2 = R1R2(a, 1.0-a, R)
            print(f"    a={a:.3f}: R1={r1:+.4e} R2={r2:+.4e}")

if __name__ == "__main__":
    main()
