# -*- coding: utf-8 -*-
"""h_tail4.py: R=1e5,1e6 tail scan, robust continuation."""
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
    f = (lambda b: R1(a, b, R)) if which=='g1' else (lambda b: R2(a, b, R))
    if lo is not None and hi is not None and lo < hi and lo > a and hi < 1:
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
        if np.isfinite(vals[i]) and np.isfinite(vals[i+1]) and vals[i]*vals[i+1] < 0:
            try:
                b0 = brentq(f, bb[i], bb[i+1], xtol=1e-11)
            except Exception:
                continue
            c = v_at(a, b0, R, a) if which=='g1' else v_at(a, b0, R, b0)
            if (which=='g1' and c > 0) or (which=='g2' and c < 0):
                return b0
    return None

results = {}
for R in [1e5, 1e6]:
    b0v = np.arccos(-0.25)/np.pi
    aa = np.linspace(0.52, b0v-5e-5, 33)
    g1s = []; g2s = []
    for j, a in enumerate(aa):
        g1 = None; g2 = None
        if j > 0 and g1s and g2s and g1s[-1] and g2s[-1]:
            g1 = branch(a, R, 'g1', g1s[-1]-2e-3, g1s[-1]+2e-3)
            g2 = branch(a, R, 'g2', g2s[-1]-2e-3, g2s[-1]+2e-3)
        if g1 is None: g1 = branch(a, R, 'g1')
        if g2 is None: g2 = branch(a, R, 'g2')
        g1s.append(g1); g2s.append(g2)
    hs = [g1-g2 if (g1 and g2) else None for g1, g2 in zip(g1s, g2s)]
    hps = [None]*len(aa)
    for j in range(1, len(aa)-1):
        if hs[j-1] is None or hs[j+1] is None: continue
        hps[j] = (hs[j+1]-hs[j-1])/(aa[j+1]-aa[j-1])
    vals = [(aa[j], g1s[j], g2s[j], hs[j], hps[j]) for j in range(len(aa)) if hs[j] is not None]
    hs_ = [v[3] for v in vals]; hps_ = [v[4] for v in vals if v[4] is not None]
    imax = int(np.argmax(hs_))
    neg = [(v[0], v[4]) for v in vals if v[4] is not None and v[4] < 0]
    results[str(int(R))] = dict(h_left=hs_[0], h_peak=hs_[imax], a_peak=vals[imax][0], h_right=hs_[-1],
                                min_hp=min(hps_) if hps_ else None,
                                neg_region=[neg[0][0], neg[-1][0]] if neg else None, n_neg=len(neg))
    print(f"R={R}: h_peak={hs_[imax]:+.6e} at a={vals[imax][0]:.4f} h_right={hs_[-1]:+.6e} min_hp={min(hps_) if hps_ else 0:+.3e} n_neg={len(neg)}" + (f" neg in [{neg[0][0]:.4f},{neg[-1][0]:.4f}]" if neg else ""))
    print(f"   h_right - h_peak = {hs_[-1]-hs_[imax]:+.3e}")
json.dump(results, open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\h_tail4.json","w"), indent=1)
