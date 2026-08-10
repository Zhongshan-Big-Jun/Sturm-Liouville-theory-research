# -*- coding: utf-8 -*-
"""explore1.py: reproduce branch structure, h, h' over R; check nondegeneracy."""
import sys, json, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
from c1_lib import residual, partials, branch1_root, branch2_root, a_fp, roots2

a0 = np.arccos(0.25) / np.pi
b0 = np.arccos(-0.25) / np.pi
print(f"a0 = {a0:.10f}, b0 = {b0:.10f}")

def g1g2(a, R):
    b1 = branch1_root(a, R)
    b2 = branch2_root(a, R)
    return b1, b2

def hp_fd(a, R, h=1e-5):
    b1p, b2p = g1g2(a + h, R); b1m, b2m = g1g2(a - h, R)
    return ((b1p - b1m) - (b2p - b2m)) / (2 * h)

results = {}
for R in [1.02, 1.05, 1.2, 1.5, 2.0, 3.0, 4.0, 10.0, 100.0, 1000.0, 1500.0, 1e4, 1e5, 1e6]:
    fp = a_fp(R)
    # common range: [a0, min(amax1, b0)]; find amax1 = largest a where branch1 exists
    amax = None
    for aa in np.linspace(a0 + 0.02, 0.999, 60):
        b1 = branch1_root(aa, R)
        if b1 is None:
            break
        amax = aa
    if amax is None:
        amax = a0 + 0.02
    beta = min(amax, b0)
    b1a0 = branch1_root(a0 + 1e-7, R)
    b2a0 = branch2_root(a0 + 1e-7, R)
    b1b0 = branch1_root(b0 - 1e-7, R) if b0 - 1e-7 > a0 else None
    b2b0 = branch2_root(b0 - 1e-7, R)
    # h at endpoints and at fp, h'(fp) via closed form
    P = partials(fp, 1 - fp, R)
    A, B, C = P['A'], P['B'], P['C']
    g1p_fp = A / B
    g2p_fp = -B / C
    hpfp = g1p_fp - g2p_fp
    detJ = A * C + B * B
    h_at_fp = 0.0  # by construction fp is good root: g1(fp)=g2(fp)=1-fp
    # verify fp is indeed a zero of h
    b1f, b2f = g1g2(fp, R)
    hfp_check = b1f - b2f
    results[R] = dict(fp=fp, beta=beta, amax=amax,
                      h_a0=(b1a0 - b2a0), h_b0=(b1b0 - b2b0) if b1b0 else None,
                      g1p_fp=g1p_fp, g2p_fp=g2p_fp, hpfp=hpfp, detJ=detJ,
                      hfp_check=hfp_check)
    print(f"R={R:>8g}: fp={fp:.9f} beta={beta:.6f} amax1={amax:.6f} h(a0)={b1a0-b2a0:+.6f} h(b0)={results[R]['h_b0']:+.6f} h'(fp)={hpfp:.6f} detJ={detJ:.3e} h(fp)={hfp_check:+.3e}")

with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility\explore1.json", "w") as f:
    json.dump(results, f, indent=1, default=float)
print("done")
