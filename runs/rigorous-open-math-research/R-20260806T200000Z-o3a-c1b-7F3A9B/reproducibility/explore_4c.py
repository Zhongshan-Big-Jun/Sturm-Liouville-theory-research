# -*- coding: utf-8 -*-
"""explore_4c.py: coarse-but-fast branch + axis data."""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1_lib as L
from explore_1 import roots2_adaptive, cfg2, R1R2, partials2

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0
_memo = {}
def R1R2m(a,b,R):
    key = (round(a,9), round(b,9), R)
    if key not in _memo:
        _memo[key] = R1R2(a,b,R,cfg=cfg2(a,b,R))
    return _memo[key]

def a_fp(R, lo=0.40, hi=0.5):
    r0 = R1R2m(lo,1.0-lo,R)[0]
    for _ in range(60):
        m = 0.5*(lo+hi)
        if np.signbit(R1R2m(m,1.0-m,R)[0]) == np.signbit(r0): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def g1_main(a, R, ns=250):
    bs = np.linspace(a+1e-4, 1.0-1e-4, ns)
    vals = np.array([R1R2m(a,b,R)[0] for b in bs])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    roots = []
    for i in np.nonzero(ch)[0]:
        lo, hi = bs[i], bs[i+1]
        flo = R1R2m(a,lo,R)[0]
        for _ in range(60):
            md = 0.5*(lo+hi)
            if np.signbit(R1R2m(a,md,R)[0]) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    # main sheet: v(a)>0
    for b in roots:
        s1,s2 = roots2_adaptive(a,b,R)
        if (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1) > 0:
            return b
    return None

if __name__ == "__main__":
    for R in [1.05, 2.0, 4.0, 100.0, 1000.0, 1e4]:
        t0 = time.time()
        fp = a_fp(R)
        print(f"=== R={R:9g} fp={fp:.7f} ({(time.time()-t0):.1f}s) ===", flush=True)
        for a in np.linspace(A0, min(0.4999, fp+0.004), 7):
            g1 = g1_main(a, R)
            if g1 is None:
                print(f"  a={a:.4f}: no main-sheet g1", flush=True); continue
            r2 = R1R2m(a, g1, R)[1]
            try:
                p = partials2(a, g1, R)
                print(f"  a={a:.4f}: g1={g1:.6f} R2_on_g1={r2:+.2e} g1'={p['A']/p['B']:.5f}", flush=True)
            except Exception:
                print(f"  a={a:.4f}: g1={g1:.6f} R2_on_g1={r2:+.2e}", flush=True)
