# -*- coding: utf-8 -*-
"""explore_5.py: comprehensive branch/axis data using fast_lib; writes JSON output."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fast_lib as F

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0
_memo = {}
def R1R2m(a,b,R):
    key = (round(a,9), round(b,9), R)
    if key not in _memo:
        _memo[key] = F.R1R2(a,b,R)
    return _memo[key]

def a_fp(R, lo=0.40, hi=0.5):
    r0 = R1R2m(lo,1.0-lo,R)[0]
    for _ in range(60):
        m = 0.5*(lo+hi)
        if np.signbit(R1R2m(m,1.0-m,R)[0]) == np.signbit(r0): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def g1_main(a, R, ns=300):
    bs = np.linspace(a+1e-4, 1.0-1e-4, ns)
    vals = np.array([R1R2m(a,b,R)[0] for b in bs])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    roots = []
    for i in np.nonzero(ch)[0]:
        lo, hi = bs[i], bs[i+1]
        flo = R1R2m(a,lo,R)[0]
        for _ in range(50):
            md = 0.5*(lo+hi)
            if np.signbit(R1R2m(a,md,R)[0]) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    for b in roots:
        s1,s2 = F.roots2_fast(a,b,R)
        if (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1) > 0:
            return b
    return None

def g2_from_reflection(a, R, g1):
    """g2(a) = 1 - g1^{-1}(1-a) via solving g1(u) = 1-a."""
    target = 1.0 - a
    # g1 is increasing; solve g1(u) = target on u in [A0, ...]
    u_lo, u_hi = A0, 0.5
    g_lo = g1_main(u_lo, R); g_hi = g1_main(u_hi, R)
    if g_lo is None or g_hi is None: return None
    if g_lo > target or g_hi < target: return None
    for _ in range(50):
        mu = 0.5*(u_lo+u_hi)
        gm = g1_main(mu, R)
        if gm is None: return None
        if gm < target: u_lo = mu
        else: u_hi = mu
    u = 0.5*(u_lo+u_hi)
    return 1.0 - u

out = {}
for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4]:
    t0 = time.time()
    fp = a_fp(R)
    rec = {"fp": fp, "a0": A0, "b0": B0, "rows": []}
    for a in np.linspace(A0, min(0.4999, fp+0.004), 8):
        g1 = g1_main(a, R)
        if g1 is None:
            rec["rows"].append({"a": a, "g1": None}); continue
        r2 = R1R2m(a, g1, R)[1]
        g2 = g2_from_reflection(a, R, g1)
        rec["rows"].append({"a": round(a,6), "g1": round(g1,8), "R2": r2, "g2": g2})
    out[f"R={R}"] = rec
    print(f"R={R:9g} fp={fp:.6f} done in {time.time()-t0:.1f}s", flush=True)

# axis data
axis = {}
for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e5, 1e6]:
    fp = a_fp(R)
    vals = []
    for a in np.linspace(0.30, 0.4999, 30):
        r1, r2 = R1R2m(a, 1.0-a, R)
        vals.append((round(a,6), r1, r2))
    axis[f"R={R}"] = {"fp": fp, "vals": vals}
out["axis"] = axis

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_branches.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("saved data_branches.json")
