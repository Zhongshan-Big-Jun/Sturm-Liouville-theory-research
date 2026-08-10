# -*- coding: utf-8 -*-
"""trace_cont2.py: robust numpy continuation of the fp-branch S3.
- Start at fp; step in a; Newton in b from previous b (nearest-root continuity).
- Adaptive step near difficult zones; verify |R1| small at each point.
- For each R outputs grid of (a, b, G, u, Gu, Phi, h, hp).
"""
import numpy as np, sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n
from c1trace_lib import R1R2, a_fp, A0, B0, partials, _newton_b, _bisect_b

def trace_arm(R, a_lo, a_hi, nstep=800, cache=None):
    fp = a_fp(R, cache=cache)
    pts = [(fp, 1-fp)]
    # right
    a, b = fp, 1-fp
    step = (a_hi - fp)/nstep
    guard = 0
    while a < a_hi - 1e-12 and guard < 200000:
        guard += 1
        a_new = min(a + step, a_hi)
        b_new = _newton_b(a_new, b, R, cache)
        if b_new is None:
            b_new = _bisect_b(a_new, b, R, cache, win=0.03)
        if b_new is None or abs(b_new - b) > 0.25:
            step *= 0.5
            if step < 1e-8: break
            continue
        pts.append((a_new, b_new))
        a, b = a_new, b_new
        step = min((a_hi-fp)/nstep, step*1.4)
    # left
    a, b = fp, 1-fp
    step = (fp - a_lo)/nstep
    guard = 0
    while a > a_lo + 1e-12 and guard < 200000:
        guard += 1
        a_new = max(a - step, a_lo)
        b_new = _newton_b(a_new, b, R, cache)
        if b_new is None:
            b_new = _bisect_b(a_new, b, R, cache, win=0.03)
        if b_new is None or abs(b_new - b) > 0.25:
            step *= 0.5
            if step < 1e-8: break
            continue
        pts.append((a_new, b_new))
        a, b = a_new, b_new
        step = min((fp-a_lo)/nstep, step*1.4)
    pts.sort()
    return pts

def build_profile(R, nstep=800):
    cache = {}
    fp = a_fp(R, cache=cache)
    pts = trace_arm(R, A0, B0, nstep=nstep, cache=cache)
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
    # dedupe
    keep = [0]
    for i in range(1, len(aa)):
        if aa[i] > aa[keep[-1]] + 1e-12: keep.append(i)
    aa = aa[keep]; bb = bb[keep]
    rows = []
    for i, a in enumerate(aa):
        b = bb[i]
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        G = -R1a/R1b
        y = 1.0 - a
        # solve g1(u) = y by monotone interpolation + Newton
        if y < bb.min() or y > bb.max():
            rows.append([float(a), float(b), float(G), np.nan, np.nan, np.nan, np.nan, np.nan])
            continue
        # find bracket via searchsorted on bb
        j = int(np.searchsorted(bb, y))
        j = min(max(j, 1), len(bb)-1)
        # refine: solve b(u) = y with u in [aa[j-1], aa[j]]
        lo, hi = aa[j-1], aa[j]
        for _ in range(50):
            md = 0.5*(lo+hi)
            bmd = np.interp(md, aa, bb)
            if bmd < y: lo = md
            else: hi = md
        u = 0.5*(lo+hi)
        bu = np.interp(u, aa, bb)
        # Newton refine on b(u)=y using local slope
        for _ in range(8):
            j2 = int(np.clip(np.searchsorted(aa, u), 1, len(aa)-1))
            sl = (bb[j2]-bb[j2-1])/(aa[j2]-aa[j2-1])
            if abs(sl) < 1e-14: break
            du = (y - bu)/sl
            if not (aa[0]-1e-6 < u+du < aa[-1]+1e-6): break
            u = u + du
            bu = np.interp(u, aa, bb)
            if abs(du) < 1e-12: break
        u = float(np.clip(u, aa[0], aa[-1]))
        # recompute G at u precisely via Newton on the branch at u
        bu_new = _newton_b(u, bu, R, cache)
        if bu_new is not None: bu = bu_new
        Ru1a, Ru1b, Ru2a, Ru2b = partials(u, bu, R, cache=cache)
        Gu = -Ru1a/Ru1b
        Phi = G*Gu
        h = b - 1.0 + u
        hp = G - 1.0/Gu
        rows.append([float(a), float(b), float(G), float(u), float(Gu), float(Phi), float(h), float(hp)])
    return dict(R=R, fp=float(fp), rows=rows)

if __name__ == "__main__":
    for Rs in [1500.0, 10000.0, 100000.0, 1000000.0]:
        o = build_profile(Rs, nstep=1200)
        rows = [r for r in o["rows"] if np.isfinite(r[7])]
        print("R=%g npts=%d fp=%.8f" % (Rs, len(rows), o["fp"]))
        if not rows: continue
        a = np.array([r[0] for r in rows]); G = np.array([r[2] for r in rows])
        Phi = np.array([r[5] for r in rows]); h = np.array([r[6] for r in rows]); hp = np.array([r[7] for r in rows])
        s = np.sign(Phi-1); chg = np.nonzero(np.diff(s)!=0)[0]
        print("  Phi-1 zeros: %d at a=%s" % (len(chg), np.array2string(a[chg], precision=5)))
        print("  G: min=%.6f at a=%.5f ; max=%.6f at a=%.5f ; G(fp)=%.6f" % (
            G.min(), a[np.argmin(G)], G.max(), a[np.argmax(G)], G[np.argmin(np.abs(a-o['fp']))]))
        print("  h: hL=%.6f hR=%.6f ; h zeros: %d" % (h[0], h[-1], int(np.sum(np.diff(np.sign(h))!=0))))
        json.dump(o, open(os.path.join(HERE, "trace2_%g.json" % Rs), "w"), indent=0)
