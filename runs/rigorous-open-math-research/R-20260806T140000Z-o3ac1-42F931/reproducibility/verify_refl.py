# -*- coding: utf-8 -*-
"""verify_refl.py: verify Gamma_2 = sigma(Gamma_1) and h'(a) = g1'(a) - 1/g1'(g1^{-1}(1-a))."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
from c1_sys import trace_g1, trace_g2, solve, F1sys, F2sys
from c1_lib import residual, roots2, partials

R = 1500.0
a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi
g1 = trace_g1(R, n=400)
g2 = trace_g2(R, n=400)
print("G1 a-range:", min(p[0] for p in g1), max(p[0] for p in g1))
print("G2 a-range:", min(p[0] for p in g2), max(p[0] for p in g2))

def interp(pts, aa):
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    o = np.argsort(xs)
    return np.interp(aa, xs[o], ys[o])

# Test sigma(Gamma_1) subset Gamma_2: for sample a in G1 domain, check sigma point satisfies R2=0, b'=x_+
for a in [0.42, 0.45, 0.5, 0.55, 0.57, 0.57364]:
    b1 = interp(g1, a)
    ap, bp = 1 - b1, 1 - a
    r2 = residual(ap, bp, R, at='b')
    # check b' = x_+ via v(b') < 0
    s1, s2 = roots2(ap, bp, R)
    from c1_lib import y_at
    vb = y_at(s2, ap, bp, R, bp)/y_at(s1, ap, bp, R, bp)
    g2at = interp(g2, ap)
    print(f"a={a:.5f}: g1={b1:.6f} -> sigma=({ap:.6f},{bp:.6f}) R2(sigma)={r2:+.3e} v(b')={vb:+.4f} g2(ap)={g2at:.6f} (should equal {bp:.6f})")

# Verify h(a) = g1(a) - 1 + phi(1-a) and h'(a) = g1'(a) - 1/g1'(phi(1-a))
print()
print("identity check (R=1500):")
def g1p_at(a, h=1e-5):
    return (interp(g1, a + h) - interp(g1, a - h)) / (2 * h)
for a in [0.45, 0.5, 0.55, 0.57364]:
    b1 = interp(g1, a); b2 = interp(g2, a)
    h_val = b1 - b2
    # phi(1-a): solve g1(u) = 1-a for u
    # find u in [a0, a_max1] with g1(u) = 1-a
    us = np.array([p[0] for p in g1]); bs = np.array([p[1] for p in g1])
    target = 1 - a
    o = np.argsort(us)
    u = np.interp(target, bs[o], us[o])
    h_val2 = b1 - 1 + u
    hp_id = g1p_at(a) - 1.0 / g1p_at(u)
    hp_fd = ((interp(g1, a+h) - interp(g1, a-h)) - (interp(g2, a+h) - interp(g2, a-h))) / (2e-5)
    print(f"a={a:.5f}: h={h_val:+.6f} h2={h_val2:+.6f} (diff {h_val-h_val2:+.2e}) | h'_id={hp_id:+.6f} h'_fd={hp_fd:+.6f}")
