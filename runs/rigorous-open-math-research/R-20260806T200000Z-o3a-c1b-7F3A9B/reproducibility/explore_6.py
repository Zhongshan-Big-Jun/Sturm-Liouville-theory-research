# -*- coding: utf-8 -*-
"""explore_6.py: branch continuation; g1 table per R; h, h', endpoints; JSON output."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fast_lib as F

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0
_memo = {}
def R1(a,b,R):
    key = (round(a,9), round(b,9), R)
    if key not in _memo:
        _memo[key] = F.R1R2(a,b,R)[0]
    return _memo[key]

def a_fp(R, lo=0.40, hi=0.5):
    r0 = R1(lo,1.0-lo,R)
    for _ in range(60):
        m = 0.5*(lo+hi)
        if np.signbit(R1(m,1.0-m,R)) == np.signbit(r0): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def bisect_root(a, R, b_lo, b_hi, iters=50):
    flo = R1(a, b_lo, R); fhi = R1(a, b_hi, R)
    if flo*fhi > 0:
        return None
    for _ in range(iters):
        md = 0.5*(b_lo+b_hi)
        if np.signbit(R1(a, md, R)) == np.signbit(flo): b_lo = md
        else: b_hi = md
    return 0.5*(b_lo+b_hi)

def build_g1(R, na=100):
    """Continuation: g1(a) for a in linspace(A0, a_stop). a_stop = min(0.5, fp+0.006)."""
    fp = a_fp(R)
    a_stop = min(0.4999, fp + 0.006)
    agrid = np.linspace(A0, a_stop, na)
    g1 = []
    b_prev = None
    for a in agrid:
        if b_prev is None:
            # find initial bracket by coarse scan
            bs = np.linspace(a+1e-4, min(1.0-1e-4, a+0.6), 120)
            vals = np.array([R1(a,b,R) for b in bs])
            ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
            roots = []
            for i in np.nonzero(ch)[0]:
                roots.append(bisect_root(a, R, bs[i], bs[i+1]))
            # main sheet: v(a)>0
            sel = None
            for b in roots:
                if b is None: continue
                s1,s2 = F.roots2_fast(a,b,R)
                if (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1) > 0:
                    sel = b; break
            if sel is None:
                g1.append(None); continue
            b_prev = sel
        else:
            # local bracket around previous root
            step = 0.03
            b = bisect_root(a, R, max(a+1e-5, b_prev-step), min(1.0-1e-5, b_prev+step))
            if b is None:
                # widen
                b = bisect_root(a, R, max(a+1e-5, b_prev-0.15), min(1.0-1e-5, b_prev+0.15))
            if b is None:
                g1.append(None); continue
            b_prev = b
        g1.append(b_prev)
    return agrid, g1

def invert_g1(g1_table, target, agrid):
    """g1^{-1}(target) by scanning the table (g1 increasing)."""
    for i in range(len(agrid)-1):
        g_lo, g_hi = g1_table[i], g1_table[i+1]
        if g_lo is None or g_hi is None: continue
        if g_lo <= target <= g_hi:
            a_lo, a_hi = agrid[i], agrid[i+1]
            for _ in range(50):
                am = 0.5*(a_lo+a_hi)
                # linear interp for g at am via bisection on table? use bisect_root on g1(am)=target
                pass
            # refine by direct root on g1(am) - target via bisection in a
            lo, hi = agrid[i], agrid[i+1]
            for _ in range(50):
                am = 0.5*(lo+hi)
                gm = g1_interp(g1_table, agrid, am)
                if gm is None: break
                if gm < target: lo = am
                else: hi = am
            return 0.5*(lo+hi)
    return None

def g1_interp(g1_table, agrid, a):
    i = int(np.clip(np.searchsorted(agrid, a, side='right')-1, 0, len(agrid)-2))
    g0, g1 = g1_table[i], g1_table[i+1]
    if g0 is None or g1 is None: return None
    t = (a - agrid[i])/(agrid[i+1]-agrid[i])
    return g0 + t*(g1-g0)

if __name__ == "__main__":
    out = {}
    for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e5, 1e6]:
        t0 = time.time()
        fp = a_fp(R)
        agrid, g1 = build_g1(R, na=120)
        rec = {"fp": fp, "agrid": agrid.tolist(), "g1": [None if x is None else round(x,9) for x in g1]}
        out[f"R={R}"] = rec
        print(f"R={R:9g} fp={fp:.6f} g1 table len={len(g1)} in {time.time()-t0:.1f}s", flush=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_g1.json"), "w") as fh:
        json.dump(out, fh)
    print("saved data_g1.json")
