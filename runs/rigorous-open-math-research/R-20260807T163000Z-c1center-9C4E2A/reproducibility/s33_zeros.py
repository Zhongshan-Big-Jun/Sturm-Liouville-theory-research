# -*- coding: utf-8 -*-
"""s33_zeros.py - Phi-1 zero locations vs q, using the tracew LEFT side filtered
by recomputed R1 residual, with a direct cross-check.  Outputs s33_zeros.json."""
import numpy as np, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1trace_lib import R1R2
pi = np.pi
HERE = os.path.dirname(os.path.abspath(__file__))
a0 = float(np.arccos(0.25)/pi)

def left_zero(Rs):
    p = os.path.join(HERE, "tracew_%g.json" % Rs)
    d = json.load(open(p))
    fp = d["fp"]; rows = d["rows"]
    sel = []
    for r in rows:
        a = r[0]
        if not (a0 - 1e-9 <= a <= fp): continue
        Phi = r[5]
        if not np.isfinite(Phi): continue
        R1v = R1R2(a, r[1], Rs)[4]
        if abs(R1v) > 1e-5: continue
        sel.append((a, Phi))
    if len(sel) < 4: return None, sel
    sel.sort()
    xs = np.array([s[0] for s in sel]); Phis = np.array([s[1] for s in sel])
    ch = np.nonzero(np.signbit(Phis[1:]-1) != np.signbit(Phis[:-1]-1))[0]
    z = None
    for i in ch:
        lo, hi = xs[i], xs[i+1]
        for _ in range(45):
            md = 0.5*(lo+hi)
            pm = np.interp(md, xs, Phis)
            if np.signbit(pm-1) == np.signbit(Phis[i]-1): lo = md
            else: hi = md
        z = 0.5*(lo+hi); break
    return z, sel

out = {}
for Rs in [5000.0, 10000.0, 100000.0, 1000000.0]:
    z, sel = left_zero(Rs)
    q = np.sqrt(Rs)
    out["R%g" % Rs] = dict(z0=z, xi=(0.5-z)*q if z else None, n_pts=len(sel))
    print("R=%g q=%.1f z0=%s xi=%s" % (Rs, q, ("%.4f" % z) if z else None, ("%.2f" % ((0.5-z)*q)) if z else None))

# direct cross-check at R=1e4 near the zero (clean Newton computation)
from fast_lib import sec, roots2_fast, y_at, norm_n
from c1trace_lib import partials
R = 1e4; q = 100.0; cache = {}
def branch_b(a, b0):
    b = b0
    for _ in range(15):
        R1v = R1R2(a, b, R, cache)[4]
        R1b = partials(a, b, R, cache=cache)[1]
        if abs(R1b) < 1e-12: return None
        db = -R1v/R1b
        b += db
        if abs(db) < 1e-13: break
    return b
def Phi1(a):
    b = branch_b(a, a + 1e-4)
    if b is None: return None
    G = -partials(a, b, R, cache=cache)[0]/partials(a, b, R, cache=cache)[1]
    y = 1 - a
    u = 1 - a
    for _ in range(10):
        bu = branch_b(u, u + 1e-4)
        if bu is None: break
        F = bu - y
        Gu = -partials(u, bu, R, cache=cache)[0]/partials(u, bu, R, cache=cache)[1]
        u -= F/Gu
        if abs(F) < 1e-12: break
    bu = branch_b(u, u + 1e-4)
    Gu = -partials(u, bu, R, cache=cache)[0]/partials(u, bu, R, cache=cache)[1]
    return G*Gu - 1
for a in [0.4460, 0.4468, 0.4476]:
    print("direct R=1e4 Phi-1 at a=%.4f: %+.6f" % (a, Phi1(a)))
out["direct_R1e4"] = {str(a): Phi1(a) for a in [0.4460, 0.4468, 0.4476]}
with open(os.path.join(HERE, "s33_zeros.json"), "w") as f:
    json.dump(out, f, indent=1)
