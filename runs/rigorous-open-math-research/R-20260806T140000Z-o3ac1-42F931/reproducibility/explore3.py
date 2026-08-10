# -*- coding: utf-8 -*-
"""explore3.py: final robust exploration: h, h', h'' shapes; endpoint facts; save json."""
import sys, json, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
import c1_lib as L

a0 = np.arccos(0.25) / np.pi
b0 = np.arccos(-0.25) / np.pi

def solve_branch(an, b, R, at, vpos):
    for w in [0.02, 0.06, 0.15]:
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

def trace_g1_from_fp(R, n_down=150, n_up=400):
    fpf = L.a_fp(R)
    pts = [(a0, a0)]  # analytic endpoint
    a, b = fpf, 1 - fpf
    # down toward a0
    for i in range(n_down):
        an = a - (a - (a0 + 5e-3)) / (n_down - i)
        if a - an < 1e-9: break
        b2 = solve_branch(an, b, R, 'a', True)
        if b2 is None: break
        pts.append((an, b2)); a, b = an, b2
    a, b = fpf, 1 - fpf
    for i in range(n_up):
        an = a + (0.999 - a) / (n_up - i)
        if an - a < 1e-9: break
        b2 = solve_branch(an, b, R, 'a', True)
        if b2 is None: break
        pts.append((an, b2)); a, b = an, b2
    # dedupe by a
    d = {}
    for p in pts:
        d[round(p[0], 10)] = p
    return sorted(d.values())

def trace_g2_from_fp(R, n_down=150, n_up=200):
    fpf = L.a_fp(R)
    pts = [(fpf, 1 - fpf)]
    a, b = fpf, 1 - fpf
    for i in range(n_down):
        an = a - (a - 0.0005) / (n_down - i)
        if a - an < 1e-9: break
        b2 = solve_branch(an, b, R, 'b', False)
        if b2 is None: break
        pts.append((an, b2)); a, b = an, b2
    a, b = fpf, 1 - fpf
    for i in range(n_up):
        an = a + (b0 - 3e-3 - a) / (n_up - i)
        if an - a < 1e-9: break
        b2 = solve_branch(an, b, R, 'b', False)
        if b2 is None: break
        pts.append((an, b2)); a, b = an, b2
    pts.append((b0, b0))  # analytic endpoint
    d = {}
    for p in pts:
        d[round(p[0], 10)] = p
    return sorted(d.values())

def hp_closed(a, R, g1b, g2b):
    try:
        P1 = L.partials(a, g1b, R)
        P2 = L.partials(a, g2b, R)
        return P1['A'] / P1['B'] + P2['B'] / P2['C']
    except Exception:
        return None

out = {}
for R in [1.02, 1.05, 1.2, 1.5, 2.0, 3.0, 4.0, 10.0, 50.0, 100.0, 200.0, 500.0, 1000.0, 1500.0, 2000.0, 3000.0, 1e4, 3e4, 1e5, 1e6]:
    g1 = trace_g1_from_fp(R)
    g2 = trace_g2_from_fp(R)
    a1 = np.array([p[0] for p in g1]); b1 = np.array([p[1] for p in g1])
    a2 = np.array([p[0] for p in g2]); b2 = np.array([p[1] for p in g2])
    a_max1 = a1[-1]; b_min2 = a2[0]
    beta = min(a_max1, b0)
    fpf = L.a_fp(R)
    grid = np.linspace(a0, beta, 250)
    g1v = np.interp(grid, a1, b1); g2v = np.interp(grid, a2, b2)
    h = g1v - g2v
    hp = np.array([hp_closed(x, R, float(np.interp(x, a1, b1)), float(np.interp(x, a2, b2))) for x in grid])
    ok = ~np.isnan(hp)
    hpp = np.gradient(hp, grid)
    neg = grid[ok & (hp < 0)]
    rec = dict(R=R, fp=fpf, a_max1=a_max1, b_min2=b_min2, beta=beta,
               h_a0=float(h[0]), h_beta=float(h[-1]),
               min_hp=float(np.min(hp[ok])) if ok.any() else None,
               argmin_hp=float(grid[ok][np.argmin(hp[ok])]) if ok.any() else None,
               max_hp=float(np.max(hp[ok])) if ok.any() else None,
               h_at_fp=float(np.interp(fpf, grid, h)),
               hp_at_fp=float(np.interp(fpf, grid, hp)),
               hpp_at_fp=float(np.interp(fpf, grid, hpp)),
               n_zeros=int(np.sum(np.signbit(h[1:]) != np.signbit(h[:-1]))),
               hp_neg_range=[float(neg[0]), float(neg[-1])] if len(neg) else [],
               fp_in_neg=bool(len(neg) and neg[0] <= fpf <= neg[-1]),
               g1_b0=float(np.interp(b0, a1, b1)) if a_max1 >= b0 else None,
               g2_a0=float(np.interp(a0, a2, b2)))
    out[R] = rec
    print(f"R={R:>7g}: fp={fpf:.6f} I=[{a0:.4f},{beta:.4f}] h(a0)={rec['h_a0']:+.5f} h(beta)={rec['h_beta']:+.5f} "
          f"min h'={rec['min_hp']:+.5f}@{rec['argmin_hp']:.4f} h'(fp)={rec['hp_at_fp']:.4f} zeros={rec['n_zeros']} "
          f"neg={rec['hp_neg_range']} hpp(fp)={rec['hpp_at_fp']:+.2f}")

with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility\explore3.json", "w") as f:
    json.dump(out, f, indent=1, default=float)
print("saved explore3.json")
