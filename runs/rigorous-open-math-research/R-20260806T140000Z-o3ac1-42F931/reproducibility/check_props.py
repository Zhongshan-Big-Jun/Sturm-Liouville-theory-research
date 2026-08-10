# -*- coding: utf-8 -*-
"""check_props.py: verify properties (2)-(5) of the reduction numerically.
(2) h(a0) < 0 ; (3) g1' strictly decreasing on I_1; (4) g1'(a) > 1 on [fp, beta];
(5) g2' > 0 on [fp, b0].
"""
import sys, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
import c1_lib as L

a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi

def solve_branch(an, b, R, at, vpos):
    for w in [0.005, 0.02, 0.06]:
        lo, hi = max(b - w, an + 1e-9), min(b + w, 1 - 1e-9)
        f = lambda y: L.residual(an, y, R, at=at)
        xs = np.linspace(lo, hi, 7)
        ys = np.array([f(x) for x in xs])
        ch = np.signbit(ys[1:]) != np.signbit(ys[:-1])
        for j in np.nonzero(ch)[0]:
            cand = brentq(f, xs[j], xs[j+1], xtol=1e-13)
            if not (cand > an + 1e-4 and abs(cand - b) <= 2.5*w):
                continue
            try:
                L.roots2(an, cand, R)
                vv = L.v_at(an, cand, R, (an+1e-9) if at=='a' else (cand-1e-9))
            except Exception:
                continue
            if (vv > 0) == vpos:
                return cand
    return None

def trace_br(R, astart, bstart, adir, target, at, vpos, n=2000, step=1e-4):
    a, b = astart, bstart
    pts = [(a, b)]
    for i in range(n):
        an = a + adir*step
        if adir > 0 and an > target: break
        if adir < 0 and an < target: break
        b2 = solve_branch(an, b, R, at, vpos)
        if b2 is None: break
        pts.append((an, b2)); a, b = an, b2
    return pts

for R in [1.05, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e5, 1e6]:
    fpf = L.a_fp(R)
    g1d = trace_br(R, fpf, 1-fpf, -1, a0+1e-4, 'a', True)
    g1u = trace_br(R, fpf, 1-fpf, +1, 0.999, 'a', True)
    g2d = trace_br(R, fpf, 1-fpf, -1, 0.001, 'b', False)
    g2u = trace_br(R, fpf, 1-fpf, +1, b0-1e-4, 'b', False)
    pts1 = g1d + g1u[1:]; pts2 = g2d + g2u[1:]
    a1 = np.array([p[0] for p in pts1]); b1 = np.array([p[1] for p in pts1])
    a2 = np.array([p[0] for p in pts2]); b2 = np.array([p[1] for p in pts2])
    o1 = np.argsort(a1); o2 = np.argsort(a2)
    a1, b1 = a1[o1], b1[o1]; a2, b2 = a2[o2], b2[o2]
    beta = min(a1[-1], b0)
    # g1' on a grid via FD of the trace (dense, step 1e-4 -> smooth)
    # use local slopes with window 5e-3
    def g1p(aa):
        i = np.searchsorted(a1, aa)
        if i <= 0 or i >= len(a1)-1: return None
        return (b1[i+1]-b1[i-1])/(a1[i+1]-a1[i-1])
    # property (3): check g1' decreasing on I_1 sample
    grid1 = np.linspace(a1[1], a1[-2], 40)
    g1ps = np.array([g1p(x) for x in grid1])
    dec = np.all(np.diff(g1ps) < 0) if len(g1ps) > 1 else None
    # property (4): g1' > 1 on [fp, beta]
    grid4 = np.linspace(fpf, beta, 25) if beta > fpf else np.array([fpf])
    g1ps4 = np.array([g1p(x) for x in grid4])
    min4 = np.min(g1ps4) if len(g1ps4) else None
    # property (5): g2' > 0
    def g2p(aa):
        i = np.searchsorted(a2, aa)
        if i <= 0 or i >= len(a2)-1: return None
        return (b2[i+1]-b2[i-1])/(a2[i+1]-a2[i-1])
    grid5 = np.linspace(fpf, min(b0, a2[-1]), 25) if a2[-1] > fpf else np.array([fpf])
    g2ps = np.array([g2p(x) for x in grid5])
    min5 = np.min(g2ps) if len(g2ps) else None
    # property (2): h(a0)
    g2a0 = np.interp(a0, a2, b2)
    h_a0 = a0 - g2a0
    print(f"R={R:>7g}: fp={fpf:.5f} beta={beta:.5f} (2) h(a0)={h_a0:+.6f} | (3) g1' dec={dec} | "
          f"(4) min g1' on [fp,beta]={min4:.6f} @ a={grid4[np.argmin(g1ps4)] if len(g1ps4) else None:.4f} | (5) min g2'={min5:.6f} | g1'(fp)={g1p(fpf):.4f}")
