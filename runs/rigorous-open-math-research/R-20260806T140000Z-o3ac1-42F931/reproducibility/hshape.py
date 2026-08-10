# -*- coding: utf-8 -*-
"""hshape.py: compute g1, g2, h, h' on the common range for a set of R; save to json.
Uses b-continuation for G1 (a = a1(b)) and a-continuation for G2 (b = g2(a)),
then inverts G1 numerically to get g1(a) on [a0, a_max1].
"""
import sys, json, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
from c1_sys import trace_g1, trace_g2, solve, F2sys
from c1_lib import residual, a_fp, partials, roots2, y_at, v_at

a0 = np.arccos(0.25) / np.pi
b0 = np.arccos(-0.25) / np.pi

def g1_from_trace(g1pts, a):
    xs = np.array([p[0] for p in g1pts]); ys = np.array([p[1] for p in g1pts])
    o = np.argsort(xs)
    return np.interp(a, xs[o], ys[o])

def g2_from_trace(g2pts, a):
    xs = np.array([p[0] for p in g2pts]); ys = np.array([p[1] for p in g2pts])
    o = np.argsort(xs)
    return np.interp(a, xs[o], ys[o])

def hp_centered(a, R, g1pts, g2pts, h=1e-5):
    b1p = g1_from_trace(g1pts, a + h); b1m = g1_from_trace(g1pts, a - h)
    b2p = g2_from_trace(g2pts, a + h); b2m = g2_from_trace(g2pts, a - h)
    return ((b1p - b1m) - (b2p - b2m)) / (2 * h)

out = {}
for R in [1.02, 1.05, 1.2, 1.5, 2.0, 3.0, 4.0, 10.0, 50.0, 100.0, 200.0, 500.0, 1000.0, 1500.0, 2000.0, 3000.0, 1e4, 3e4, 1e5, 1e6]:
    g1 = trace_g1(R, n=500)
    g2 = trace_g2(R, n=500)
    a_max1 = max(p[0] for p in g1)
    b_min2 = min(p[0] for p in g2)
    beta = min(a_max1, b0)
    fp = a_fp(R)
    # fine grid on [a0, beta]
    Na = 400
    aa = np.linspace(a0, beta, Na)
    hh = np.array([g1_from_trace(g1, x) - g2_from_trace(g2, x) for x in aa])
    # h' via g1', g2' separately with local slopes from traces (better: direct eval)
    hp = np.array([hp_centered(x, R, g1, g2) for x in aa])
    # check fp
    hfp = g1_from_trace(g1, fp) - g2_from_trace(g2, fp)
    # sign of h at endpoints, min h', location
    rec = dict(R=R, fp=fp, a_max1=a_max1, b_min2=b_min2, beta=beta,
               h_a0=float(hh[0]), h_beta=float(hh[-1]),
               h_fp=float(hfp),
               min_hp=float(np.min(hp)), argmin_hp=float(aa[np.argmin(hp)]),
               max_hp=float(np.max(hp)),
               h_positive_tail=bool(np.all(hh[aa > fp] > 0)) if np.any(aa > fp) else None,
               n_zeros=None)
    # count zeros of h on grid by sign changes
    ch = np.signbit(hh[1:]) != np.signbit(hh[:-1])
    rec['n_zeros_grid'] = int(np.sum(ch))
    out[R] = rec
    print(f"R={R:>7g}: fp={fp:.6f} I=[{a0:.4f},{beta:.4f}] h(a0)={rec['h_a0']:+.5f} h(beta)={rec['h_beta']:+.5f} h(fp)={hfp:+.2e} min h'={rec['min_hp']:+.5f} @ {rec['argmin_hp']:.4f} max h'={rec['max_hp']:.5f} zeros={rec['n_zeros_grid']}")

with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility\hshape.json", "w") as f:
    json.dump(out, f, indent=1, default=float)
print("saved hshape.json")
