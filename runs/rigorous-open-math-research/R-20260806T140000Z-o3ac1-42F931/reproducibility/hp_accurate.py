# -*- coding: utf-8 -*-
"""hp_accurate.py: accurate h' for large R: tiny-step traces + FD, vs closed form."""
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
            cand = brentq(f, xs[j], xs[j + 1], xtol=1e-13)
            if not (cand > an + 1e-4 and abs(cand - b) <= 2.5 * w):
                continue
            try:
                L.roots2(an, cand, R)
                vv = L.v_at(an, cand, R, (an + 1e-9) if at == 'a' else (cand - 1e-9))
            except Exception:
                continue
            if (vv > 0) == vpos:
                return cand
    return None

def trace(R, astart, bstart, adir, target, n, step):
    a, b = astart, bstart
    pts = []
    for i in range(n):
        an = a + adir * step
        if adir > 0 and an > target: break
        if adir < 0 and an < target: break
        b2 = solve_branch(an, b, R, 'a' if adir < 0 else 'a', True) if False else None
        # decide 'at' by branch: we always pass at and vpos
        raise NotImplementedError
    return pts

def trace_br(R, astart, bstart, adir, target, at, vpos, n=3000, step=1e-4):
    a, b = astart, bstart
    pts = [(a, b)]
    for i in range(n):
        an = a + adir * step
        if adir > 0 and an > target: break
        if adir < 0 and an < target: break
        b2 = solve_branch(an, b, R, at, vpos)
        if b2 is None:
            break
        pts.append((an, b2))
        a, b = an, b2
    return pts

for R in [500.0, 1000.0, 1500.0, 1e4, 1e5]:
    fpf = L.a_fp(R)
    # g1 trace: down from fp to a0, up from fp to 0.999
    g1d = trace_br(R, fpf, 1 - fpf, -1, a0 + 1e-5, 'a', True)
    g1u = trace_br(R, fpf, 1 - fpf, +1, 0.999, 'a', True)
    # g2 trace: down from fp to 0.001, up from fp to b0-1e-4
    g2d = trace_br(R, fpf, 1 - fpf, -1, 0.001, 'b', False)
    g2u = trace_br(R, fpf, 1 - fpf, +1, b0 - 1e-4, 'b', False)
    pts1 = g1d + g1u[1:]
    pts2 = g2d + g2u[1:]
    a1 = np.array([p[0] for p in pts1]); b1 = np.array([p[1] for p in pts1])
    a2 = np.array([p[0] for p in pts2]); b2 = np.array([p[1] for p in pts2])
    o1 = np.argsort(a1); o2 = np.argsort(a2)
    a1, b1 = a1[o1], b1[o1]; a2, b2 = a2[o2], b2[o2]
    beta = min(a1[-1], b0)
    # h on [a0, beta]
    grid = np.linspace(a0, beta, 120)
    g1v = np.interp(grid, a1, b1); g2v = np.interp(grid, a2, b2)
    h = g1v - g2v
    hp = np.gradient(h, grid)
    # closed form at a few points
    hpc = []
    for x in grid[::10]:
        try:
            P1 = L.partials(x, float(np.interp(x, a1, b1)), R)
            P2 = L.partials(x, float(np.interp(x, a2, b2)), R)
            hpc.append((x, P1['A']/P1['B'] + P2['B']/P2['C']))
        except Exception:
            hpc.append((x, np.nan))
    neg = grid[hp < 0]
    print(f"R={R}: fp={fpf:.5f} beta={beta:.5f} g1pts={len(pts1)} g2pts={len(pts2)}")
    print(f"   h(a0)={h[0]:+.6f} h(beta)={h[-1]:+.6f} min h'={np.min(hp):+.6f}@{grid[np.argmin(hp)]:.5f} max h'={np.max(hp):+.4f}")
    print(f"   h'(fp)={np.interp(fpf, grid, hp):+.5f}  neg region: {([round(float(neg[0]),4), round(float(neg[-1]),4)] if len(neg) else [])}")
    print(f"   h'(fp) closed: {[v for x,v in hpc if abs(x-fpf)<0.01]}")
    # check h' > 0 on [a0, fp]
    left = grid <= fpf
    print(f"   min h' on [a0, fp]: {np.min(hp[left]):+.6f}")
    print()
