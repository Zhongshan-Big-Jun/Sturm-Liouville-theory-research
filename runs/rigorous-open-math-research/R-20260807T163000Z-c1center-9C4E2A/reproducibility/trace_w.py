# -*- coding: utf-8 -*-
"""trace_w.py: robust S3 tracer using width w = b-a > 0 with sign-consistency.
Newton corrects in w (not b), enforcing w>0, and checks v(a) > 0 (a = x_- type).
"""
import numpy as np, sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n, y_at
from c1trace_lib import R1R2, a_fp, A0, B0, partials

def R1_of_w(a, w, R):
    b = a + w
    if b >= 1.0 or w <= 0: return None
    s1, s2, n1, n2, R1v, R2v = R1R2(a, b, R)
    return R1v, b, s1, s2, n1, n2

def newton_w(a, w0, R, cache=None, maxit=40, tol=1e-13):
    w = w0
    for _ in range(maxit):
        b = a + w
        if w <= 0 or b >= 1.0: return None
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        R1v = R1R2(a, b, R, cache)[4]
        # dR1/dw = R1_b
        if abs(R1b) < 1e-12: return None
        dw = -R1v/R1b
        w2 = w + dw
        if w2 <= 1e-10: return None
        w = w2
        if abs(dw) < tol: break
    b = a + w
    R1v = R1R2(a, b, R, cache)[4]
    return w if abs(R1v) < 1e-9 else None

def trace_w(R, a_lo, a_hi, nstep=2000, cache=None):
    fp = a_fp(R, cache=cache)
    pts = [(fp, 1-fp)]
    a, b = fp, 1-fp
    w = b - a
    step = (a_hi - fp)/nstep
    guard = 0
    while a < a_hi - 1e-12 and guard < 300000:
        guard += 1
        a_new = min(a + step, a_hi)
        w_new = newton_w(a_new, w, R, cache)
        if w_new is None:
            step *= 0.5
            if step < 1e-10: break
            continue
        b_new = a_new + w_new
        if b_new >= 1.0 or w_new < 1e-9:
            step *= 0.5
            if step < 1e-10: break
            continue
        pts.append((a_new, b_new))
        a, b, w = a_new, b_new, w_new
        step = min((a_hi-fp)/nstep, step*1.4)
    a, b = fp, 1-fp
    w = b - a
    step = (fp - a_lo)/nstep
    guard = 0
    while a > a_lo + 1e-12 and guard < 300000:
        guard += 1
        a_new = max(a - step, a_lo)
        w_new = newton_w(a_new, w, R, cache)
        if w_new is None:
            step *= 0.5
            if step < 1e-10: break
            continue
        b_new = a_new + w_new
        if b_new >= 1.0 or w_new < 1e-9:
            step *= 0.5
            if step < 1e-10: break
            continue
        pts.append((a_new, b_new))
        a, b, w = a_new, b_new, w_new
        step = min((fp-a_lo)/nstep, step*1.4)
    pts.sort()
    return pts

def analyze(R, nstep=2000):
    cache = {}
    fp = a_fp(R, cache=cache)
    pts = trace_w(R, A0, B0, nstep=nstep, cache=cache)
    if not pts: return None
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
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
        if y < bb.min() or y > bb.max():
            rows.append([float(a), float(b), float(G), np.nan, np.nan, np.nan, np.nan, np.nan]); continue
        j = int(np.clip(np.searchsorted(bb, y), 1, len(bb)-1))
        lo, hi = aa[j-1], aa[j]
        for _ in range(60):
            md = 0.5*(lo+hi)
            if np.interp(md, aa, bb) < y: lo = md
            else: hi = md
        u = 0.5*(lo+hi)
        bu = np.interp(u, aa, bb)
        for _ in range(8):
            j2 = int(np.clip(np.searchsorted(aa, u), 1, len(aa)-1))
            sl = (bb[j2]-bb[j2-1])/(aa[j2]-aa[j2-1])
            if abs(sl) < 1e-14: break
            du = (y - bu)/sl
            if not (aa[0]-1e-6 < u+du < aa[-1]+1e-6): break
            u = u + du; bu = np.interp(u, aa, bb)
            if abs(du) < 1e-12: break
        u = float(np.clip(u, aa[0], aa[-1]))
        wu = newton_w(u, bu - u, R, cache)
        if wu is not None: bu = u + wu
        Ru1a, Ru1b, Ru2a, Ru2b = partials(u, bu, R, cache=cache)
        Gu = -Ru1a/Ru1b
        Phi = G*Gu; h = b - 1.0 + u; hp = G - 1.0/Gu
        rows.append([float(a), float(b), float(G), float(u), float(Gu), float(Phi), float(h), float(hp)])
    return dict(R=R, fp=float(fp), rows=rows)

if __name__ == "__main__":
    for Rs in [1000.0, 5000.0, 10000.0, 100000.0, 1000000.0]:
        o = analyze(Rs, nstep=2000)
        rows = [r for r in o["rows"] if np.isfinite(r[7])]
        print("R=%g npts=%d fp=%.8f" % (Rs, len(rows), o["fp"]))
        if not rows: continue
        a = np.array([r[0] for r in rows]); G = np.array([r[2] for r in rows])
        Phi = np.array([r[5] for r in rows]); h = np.array([r[6] for r in rows])
        s = np.sign(Phi-1); chg = np.nonzero(np.diff(s)!=0)[0]
        print("  Phi-1 zeros: %d at a=%s" % (len(chg), np.array2string(a[chg], precision=5)))
        print("  G min=%.6f@a=%.5f max=%.6f@a=%.5f G(fp)=%.6f" % (G.min(), a[np.argmin(G)], G.max(), a[np.argmax(G)], G[np.argmin(np.abs(a-o['fp']))]))
        print("  hL=%.6f hR=%.6f hz=%d w(fp)=%.6f w(a0)=%.6f" % (h[0], h[-1], int(np.sum(np.diff(np.sign(h))!=0)), (rows[np.argmin(np.abs(a-o['fp']))][1]-rows[np.argmin(np.abs(a-o['fp']))][0]), rows[0][1]-rows[0][0]))
        json.dump(o, open(os.path.join(HERE, "tracew_%g.json" % Rs), "w"))
