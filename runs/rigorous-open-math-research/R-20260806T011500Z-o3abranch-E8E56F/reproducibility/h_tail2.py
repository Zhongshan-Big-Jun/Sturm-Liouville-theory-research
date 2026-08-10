# -*- coding: utf-8 -*-
"""h_tail2.py: optimized tail scan using continuation + grid FD for h'."""
import sys, numpy as np, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at
from scipy.optimize import brentq

def R1(a, b, R):
    return float(np.ravel(f_at(a, b, R, a, config(a, b, R)))[0])
def R2(a, b, R):
    return float(np.ravel(f_at(a, b, R, b, config(a, b, R)))[0])
def v_at(a, b, R, x):
    from agentB_lib import y_L
    s = config(a, b, R)[0]
    y = y_L(a, b, R, s, np.array([x]))[:, 0]
    return float(y[1]/y[0])

def branch(a, R, which, lo=None, hi=None):
    if lo is None: lo = a+1e-5
    if hi is None: hi = 1-1e-5
    f = (lambda b: R1(a, b, R)) if which=='g1' else (lambda b: R2(a, b, R))
    # try bracket around guess first (continuation), fall back to scan
    if lo < hi:
        try:
            b0 = brentq(f, lo, hi, xtol=1e-11)
            c = v_at(a, b0, R, a) if which=='g1' else v_at(a, b0, R, b0)
            if (which=='g1' and c > 0) or (which=='g2' and c < 0):
                return b0
        except Exception:
            pass
    bb = np.linspace(a+1e-5, 1-1e-5, 40)
    vals = [f(b) for b in bb]
    for i in range(len(bb)-1):
        if vals[i]*vals[i+1] < 0:
            try:
                b0 = brentq(f, bb[i], bb[i+1], xtol=1e-11)
            except Exception:
                continue
            c = v_at(a, b0, R, a) if which=='g1' else v_at(a, b0, R, b0)
            if (which=='g1' and c > 0) or (which=='g2' and c < 0):
                return b0
    return None

results = {}
for R in [1e4, 1e5, 1e6]:
    b0v = np.arccos(-0.25)/np.pi
    aa = np.linspace(0.52, b0v-5e-5, 41)
    rows = []; g1p = None; g2p = None
    for a in aa:
        # continuation: bracket around previous solution
        if rows:
            prev1 = rows[-1][1]; prev2 = rows[-1][2]
            g1 = branch(a, R, 'g1', prev1-2e-3, prev1+2e-3)
            g2 = branch(a, R, 'g2', prev2-2e-3, prev2+2e-3)
        else:
            g1 = branch(a, R, 'g1'); g2 = branch(a, R, 'g2')
        if g1 is None: g1 = branch(a, R, 'g1')
        if g2 is None: g2 = branch(a, R, 'g2')
        rows.append([a, g1, g2])
    # grid FD for h'
    for i, (a, g1, g2) in enumerate(rows):
        if g1 is None or g2 is None: continue
        h = g1-g2
        if 1 <= i < len(rows)-1:
            a0, g10, g20 = rows[i-1]; a2, g12, g22 = rows[i+1]
            if g10 and g12 and g20 and g22:
                hp = ((g12-g10) - (g22-g20))/(a2-a0)
                rows[i].append(h); rows[i].append(hp)
            else:
                rows[i].append(h); rows[i].append(None)
        else:
            rows[i].append(h); rows[i].append(None)
    out = [r for r in rows if r[1] is not None and r[2] is not None]
    hs = [r[3] for r in out]; hps = [r[4] for r in out if r[4] is not None]
    imax = int(np.argmax(hs))
    neg = [(out[i][0], out[i][4]) for i in range(len(out)) if out[i][4] is not None and out[i][4] < 0]
    results[str(int(R))] = dict(h_left=hs[0], h_peak=hs[imax], a_peak=out[imax][0], h_right=hs[-1],
                                min_hp=min(hps) if hps else None,
                                neg_region=[neg[0][0], neg[-1][0]] if neg else None, n_neg=len(neg))
    print(f"R={R}: h_peak={hs[imax]:+.6e} at a={out[imax][0]:.4f} h_right={hs[-1]:+.6e} min_hp={min(hps) if hps else None:+.3e} n_neg={len(neg)}" + (f" neg in [{neg[0][0]:.4f},{neg[-1][0]:.4f}]" if neg else ""))
    print(f"   h_right - h_peak = {hs[-1]-hs[imax]:+.3e}")
json.dump(results, open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\h_tail2.json","w"), indent=1)
