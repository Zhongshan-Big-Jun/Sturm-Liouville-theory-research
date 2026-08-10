# -*- coding: utf-8 -*-
"""s33_profile.py - clean S3 branch profile at several q (W, G, Phi, s1, s2).
Outputs s33_profile.json.  Continuation from the fp with Newton, cross-checked
against the (P-)/(P+) formulas.  Numerics only."""
import numpy as np, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1trace_lib import R1R2, partials, a_fp
pi = np.pi
HERE = os.path.dirname(os.path.abspath(__file__))
a0 = float(np.arccos(0.25)/pi)

def trace_clean(R, a_lo, a_hi, nstep=1200):
    cache = {}
    fp = a_fp(R, 0.40, 0.5, cache)
    pts = [(fp, 1-fp)]
    for direction in [-1, 1]:
        a, b = fp, 1-fp
        step = (a_hi - fp)/nstep if direction > 0 else (fp - a_lo)/nstep
        guard = 0
        while guard < 200000:
            guard += 1
            a_new = a + direction*step
            if direction > 0 and a_new >= a_hi: break
            if direction < 0 and a_new <= a_lo: break
            b_new = b
            ok = False
            for _ in range(10):
                R1v = R1R2(a_new, b_new, R, cache)[4]
                R1b = partials(a_new, b_new, R, cache=cache)[1]
                if abs(R1b) < 1e-12: break
                db = -R1v/R1b
                b_new += db
                if abs(db) < 1e-12:
                    ok = True; break
            if not ok or abs(b_new - b) > 0.02 or not (a_new < b_new < 1):
                step *= 0.5
                if step < 1e-8: break
                continue
            pts.append((a_new, b_new))
            a, b = a_new, b_new
            step = min(step, (a_hi - a_lo)/nstep)
            step *= 1.3
    pts.sort()
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
    # dedupe
    keep = [0]
    for i in range(1, len(aa)):
        if aa[i] > aa[keep[-1]] + 1e-12: keep.append(i)
    return aa[keep], bb[keep], cache, fp

def profile_at(a, R, aa, bb, cache):
    if a < aa[0] or a > aa[-1]: return None
    b = float(np.interp(a, aa, bb))
    for _ in range(8):
        R1v = R1R2(a, b, R, cache)[4]
        R1b = partials(a, b, R, cache=cache)[1]
        if abs(R1b) < 1e-12: break
        db = -R1v/R1b
        b += db
        if abs(db) < 1e-12: break
    s1, s2, n1, n2, R1v, R2v = R1R2(a, b, R, cache)
    G = -partials(a, b, R, cache=cache)[0]/partials(a, b, R, cache=cache)[1]
    y = 1 - a
    u = float(np.interp(y, bb, aa))
    for _ in range(10):
        bu = float(np.interp(u, aa, bb))
        j = int(np.clip(np.searchsorted(aa, u), 1, len(aa)-1))
        sl = (bb[j]-bb[j-1])/(aa[j]-aa[j-1])
        if abs(sl) < 1e-14: break
        F = bu - y
        u -= F/sl
        if abs(F) < 1e-12: break
    bu = float(np.interp(u, aa, bb))
    Gu = -partials(u, bu, R, cache=cache)[0]/partials(u, bu, R, cache=cache)[1]
    return dict(a=a, b=b, W=(b-a)*np.sqrt(R), G=G, u=u, Phi=G*Gu, s1=s1, s2=s2,
                s1q=s1*np.sqrt(np.sqrt(R)), s2a=s2*a, R1=R1v, R2=R2v)

out = {}
for R in [1e4, 1e6]:
    t0 = time.time()
    aa, bb, cache, fp = trace_clean(R, a0 + 1e-4, 1 - a0 - 1e-4)
    q = np.sqrt(R)
    rows = []
    for a in [a0+2e-4, 0.43, 0.45, 0.47, 0.51, 0.53, 0.55, 1-a0-2e-4]:
        if a >= 1 - a0: continue
        r = profile_at(a, R, aa, bb, cache)
        if r: rows.append(r)
    out["R%g" % R] = dict(fp=fp, q=q, rows=rows)
    print("R=%g q=%.1f done in %.1fs" % (R, q, time.time()-t0))
    for r in rows:
        print("  a=%.4f W=%.5f G=%.5f Phi=%.6f s1q=%.4f s2a=%.5f" % (r["a"], r["W"], r["G"], r["Phi"], r["s1q"], r["s2a"]))
with open(os.path.join(HERE, "s33_profile.json"), "w") as f:
    json.dump(out, f, indent=1)
