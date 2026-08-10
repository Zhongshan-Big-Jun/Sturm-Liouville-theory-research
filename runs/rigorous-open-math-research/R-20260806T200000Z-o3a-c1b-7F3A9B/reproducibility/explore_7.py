# -*- coding: utf-8 -*-
"""explore_7.py: fast branch continuation with local bisection (na=60, iters=16)."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fast_lib as F

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0

def R1r(a,b,R):
    return F.R1R2(a,b,R)[0]

def a_fp(R, lo=0.40, hi=0.5):
    r0 = R1r(lo,1.0-lo,R)
    for _ in range(60):
        m = 0.5*(lo+hi)
        if np.signbit(R1r(m,1.0-m,R)) == np.signbit(r0): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def bisect(a, R, lo, hi, iters=16):
    flo = R1r(a, lo, R)
    if flo*R1r(a, hi, R) > 0: return None
    for _ in range(iters):
        md = 0.5*(lo+hi)
        if np.signbit(R1r(a, md, R)) == np.signbit(flo): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def build_g1(R, na=60):
    fp = a_fp(R)
    a_stop = min(0.4998, fp + 0.004)
    agrid = np.linspace(A0, a_stop, na)
    g1 = [None]*na
    b_prev = None
    for i, a in enumerate(agrid):
        if b_prev is None:
            bs = np.linspace(a+1e-4, min(1.0-1e-4, a+0.6), 100)
            vals = np.array([R1r(a,b,R) for b in bs])
            ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
            roots = [bisect(a, R, bs[j], bs[j+1], iters=40) for j in np.nonzero(ch)[0]]
            sel = None
            for b in roots:
                if b is None: continue
                s1,s2 = F.roots2_fast(a,b,R)
                if (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1) > 0:
                    sel = b; break
            if sel is None: continue
            b_prev = sel
        else:
            step = 0.03
            b = bisect(a, R, max(a+1e-5, b_prev-step), min(1.0-1e-5, b_prev+step))
            if b is None:
                b = bisect(a, R, max(a+1e-5, b_prev-0.2), min(1.0-1e-5, b_prev+0.2))
            if b is None: continue
            b_prev = b
        g1[i] = b_prev
    return agrid, g1

if __name__ == "__main__":
    out = {}
    for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e5, 1e6]:
        t0 = time.time()
        fp = a_fp(R)
        agrid, g1 = build_g1(R, na=60)
        out[f"R={R}"] = {"fp": fp, "agrid": agrid.tolist(),
                          "g1": [None if x is None else round(x,9) for x in g1]}
        print(f"R={R:9g} fp={fp:.6f} done {time.time()-t0:.1f}s", flush=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_g1.json"), "w") as fh:
        json.dump(out, fh)
    print("saved")
