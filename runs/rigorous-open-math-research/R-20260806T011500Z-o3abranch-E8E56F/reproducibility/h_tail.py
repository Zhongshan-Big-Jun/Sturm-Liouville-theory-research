# -*- coding: utf-8 -*-
"""h_tail.py: structure of h and h' on the tail [0.55, b0] for large R; h(b0), peak, dip."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at

def R1(a, b, R):
    return float(np.ravel(f_at(a, b, R, a, config(a, b, R)))[0])
def R2(a, b, R):
    return float(np.ravel(f_at(a, b, R, b, config(a, b, R)))[0])
def v_at(a, b, R, x):
    from agentB_lib import y_L
    s = config(a, b, R)[0]
    y = y_L(a, b, R, s, np.array([x]))[:, 0]
    return float(y[1]/y[0])

def branch(a, R, which):
    from scipy.optimize import brentq
    bb = np.linspace(a+1e-5, 1-1e-5, 60)
    f = (lambda b: R1(a, b, R)) if which=='g1' else (lambda b: R2(a, b, R))
    vals = [f(b) for b in bb]
    for i in range(len(bb)-1):
        if vals[i]*vals[i+1] < 0:
            try:
                b0 = brentq(f, bb[i], bb[i+1], xtol=1e-12)
            except Exception:
                continue
            if which=='g1' and v_at(a, b0, R, a) > 0: return b0
            if which=='g2' and v_at(a, b0, R, b0) < 0: return b0
    return None

for R in [1e4, 1e5, 1e6]:
    b0v = np.arccos(-0.25)/np.pi
    aa = np.linspace(0.54, b0v-3e-5, 25)
    rows = []
    for a in aa:
        g1 = branch(a, R, 'g1'); g2 = branch(a, R, 'g2')
        if g1 is None or g2 is None:
            rows.append((a, None, None, None)); continue
        rows.append((a, g1, g2, g1-g2))
    # h' via 5-point stencil where possible
    out = []
    for i, (a, g1, g2, h) in enumerate(rows):
        if h is None: continue
        # central difference using neighbors (branch re-solve at a +/- h_a)
        h_a = 1e-4
        g1p = None; g2p = None
        try:
            g1m = branch(a-h_a, R, 'g1'); g1q = branch(a+h_a, R, 'g1')
            g2m = branch(a-h_a, R, 'g2'); g2q = branch(a+h_a, R, 'g2')
            if g1m and g1q and g2m and g2q:
                g1p = (g1q-g1m)/(2*h_a); g2p = (g2q-g2m)/(2*h_a)
        except Exception:
            pass
        out.append((a, g1, g2, h, g1p, g2p))
    # summarize
    hs = [r[3] for r in out if r[3] is not None]
    hps = [r[5]-r[4] for r in out if r[4] is not None and r[5] is not None]
    imax = int(np.argmax(hs)); imin_hp = int(np.argmin(hps))
    print(f"R={R}: n={len(out)}")
    print(f"  h(0.54)={hs[0]:+.6e}  h_peak(a={out[imax][0]:.4f})={hs[imax]:+.6e}  h(b0-)={hs[-1]:+.6e}")
    print(f"  min h'={hps[imin_hp]:+.6e} at a={out[imin_hp][0]:.5f}  h'(0.54)={hps[0]:+.4f}")
    neg = [(out[i][0], hps[i]) for i in range(len(hps)) if hps[i] < 0]
    print(f"  h'<0 region: a in [{neg[0][0]:.5f},{neg[-1][0]:.5f}] n_neg={len(neg)}" if neg else "  h' >= 0 everywhere")
    print(f"  h(b0-) - h_peak = {hs[-1]-hs[imax]:+.3e}")
