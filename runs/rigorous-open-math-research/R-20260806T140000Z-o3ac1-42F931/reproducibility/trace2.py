# -*- coding: utf-8 -*-
"""trace2.py: robust continuation for main sheets; report h and endpoints."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
from c1_lib import residual, roots2, y_at, v_at, sec

a0 = np.arccos(0.25) / np.pi
b0 = np.arccos(-0.25) / np.pi

def newton_resid(a, R, at, b0, tol=1e-13):
    b = b0
    for it in range(80):
        r = residual(a, b, R, at=at)
        hh = 1e-7
        rp = residual(a, b + hh, R, at=at)
        dr = (rp - r) / hh
        if abs(dr) < 1e-16:
            break
        step = r / dr
        nb = b - step
        if not (a + 1e-10 < nb < 1 - 1e-10):
            break
        b = nb
        if abs(step) < tol:
            break
    return b, abs(residual(a, b, R, at=at))

def trace_g1(R, astart, n=300):
    """Trace Gamma_1 from (a0+eps, b) with Newton seeded by previous point."""
    a = astart
    b, res = newton_resid(a, R, 'a', a0 + 0.01)
    pts = [(a, b, res)]
    for i in range(n):
        an = a + (0.9 - a) / n
        # try small step
        for step in [ (0.9-a)/n * 2, (0.9-a)/n, (0.9-a)/n * 0.5 ]:
            atry = min(a + step, 0.9)
            btry, res = newton_resid(atry, R, 'a', b + (b - pts[-1][1]) * 0.0 if False else b)
            if btry > atry + 1e-9 and res < 1e-8:
                a = atry; b = btry
                break
        else:
            break
        try:
            vv = v_at(a, b, R, a + 1e-10)
        except Exception:
            break
        if not (vv > 0):
            break
        pts.append((a, b, res))
    return pts

def trace_g2(R, astart, n=300):
    a = astart
    b, res = newton_resid(a, R, 'b', b0 - 0.01)
    pts = [(a, b, res)]
    for i in range(n):
        step = (0.42 - a) / n
        for st in [step * 2, step, step * 0.5]:
            atry = a + st if st > 0 else a - st
            if atry <= 0.42:
                atry = 0.42 + 1e-6
            btry, res = newton_resid(atry, R, 'b', b)
            if btry > atry + 1e-9 and res < 1e-8:
                a = atry; b = btry
                break
        else:
            break
        try:
            vv = v_at(a, b, R, b - 1e-10)
        except Exception:
            break
        if not (vv < 0):
            break
        pts.append((a, b, res))
    return pts

for R in [1.05, 4.0, 100.0, 1000.0, 1500.0, 1e4]:
    print(f"===== R = {R} =====")
    g1 = trace_g1(R, a0 + 1e-3, n=200)
    g2 = trace_g2(R, b0 - 1e-3, n=200)
    print(f"  Gamma_1: {len(g1)} pts; a in [{g1[0][0]:.6f},{g1[-1][0]:.6f}]; b in [{min(p[1] for p in g1):.6f},{max(p[1] for p in g1):.6f}]")
    print(f"  Gamma_2: {len(g2)} pts; a in [{g2[-1][0]:.6f},{g2[0][0]:.6f}]; b in [{min(p[1] for p in g2):.6f},{max(p[1] for p in g2):.6f}]")
    # common range and h at ends
    aL = max(g1[0][0], g2[-1][0])
    aR = min(g1[-1][0], g2[0][0])
    # interpolate h at aL, aR from the two traces
    def interp(pts, aa):
        xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
        return np.interp(aa, xs, ys)
    if aL < aR:
        b1L, b2L = interp(g1, aL), interp(g2, aL)
        b1R, b2R = interp(g1, aR), interp(g2, aR)
        print(f"  common range [{aL:.6f}, {aR:.6f}]: h(aL)={b1L-b2L:+.6f} h(aR)={b1R-b2R:+.6f}")
    print()
