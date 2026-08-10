# -*- coding: utf-8 -*-
"""trace4.py: b-continuation of main sheets; output g1(a), g2(a), h on common range."""
import sys, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
from c1_lib import residual, v_at

a0 = np.arccos(0.25) / np.pi
b0 = np.arccos(-0.25) / np.pi

def trace_g1(R, bmax=1.0 - 1e-6, n=400, d0=1e-4):
    """Gamma_1 main sheet: a = a1(b); continuation from (a0, a0)."""
    pts = []
    b = a0 + d0
    aprev = a0
    while b < bmax:
        # solve R1(a, b) = 0 for a near aprev
        w = 0.03
        lo, hi = max(aprev - w, 1e-9), min(aprev + w, b - 1e-9)
        f = lambda a: residual(a, b, R, at='a')
        fl, fh = f(lo), f(hi)
        if fl * fh > 0:
            # widen window
            w = 0.12
            lo, hi = max(aprev - w, 1e-9), min(aprev + w, b - 1e-9)
            fl, fh = f(lo), f(hi)
            if fl * fh > 0:
                break
        a = brentq(f, lo, hi, xtol=1e-14)
        try:
            vv = v_at(a, b, R, a + 1e-9)
        except Exception:
            break
        if vv <= 0:
            break
        pts.append((a, b))
        if len(pts) >= n:
            break
        aprev = a
        b = b + (bmax - (a0 + d0)) / n
    return pts

def trace_g2(R, amin=0.02, n=400, d0=1e-4):
    """Gamma_2 main sheet: a = a2(b); continuation from (b0, b0) downward in b."""
    pts = []
    b = b0 - d0
    aprev = b0
    while b > amin:
        w = 0.03
        lo, hi = max(aprev - w, 1e-9), min(aprev + w, b - 1e-9)
        f = lambda a: residual(a, b, R, at='b')
        fl, fh = f(lo), f(hi)
        if fl * fh > 0:
            w = 0.12
            lo, hi = max(aprev - w, 1e-9), min(aprev + w, b - 1e-9)
            fl, fh = f(lo), f(hi)
            if fl * fh > 0:
                break
        a = brentq(f, lo, hi, xtol=1e-14)
        try:
            vv = v_at(a, b, R, b - 1e-9)
        except Exception:
            break
        if vv >= 0:
            break
        pts.append((a, b))
        if len(pts) >= n:
            break
        aprev = a
        b = b - (b0 - d0 - amin) / n
    return pts

def interp_ab(pts, aa):
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    order = np.argsort(xs)
    return np.interp(aa, xs[order], ys[order])

if __name__ == "__main__":
    for R in [1.02, 1.05, 1.2, 4.0, 100.0, 1000.0, 1e4]:
        print(f"===== R = {R} =====")
        g1 = trace_g1(R)
        g2 = trace_g2(R)
        print(f"  G1: {len(g1)} pts, a in [{min(p[0] for p in g1):.6f},{max(p[0] for p in g1):.6f}], b in [{min(p[1] for p in g1):.6f},{max(p[1] for p in g1):.6f}]")
        print(f"  G2: {len(g2)} pts, a in [{min(p[0] for p in g2):.6f},{max(p[0] for p in g2):.6f}], b in [{min(p[1] for p in g2):.6f},{max(p[1] for p in g2):.6f}]")
        aL = max(min(p[0] for p in g1), min(p[0] for p in g2))
        aR = min(max(p[0] for p in g1), max(p[0] for p in g2))
        if aL < aR:
            b1L, b2L = interp_ab(g1, aL), interp_ab(g2, aL)
            b1R, b2R = interp_ab(g1, aR), interp_ab(g2, aR)
            print(f"  common [{aL:.6f},{aR:.6f}]: h(L)={b1L-b2L:+.6f} h(R)={b1R-b2R:+.6f}")
        print()
