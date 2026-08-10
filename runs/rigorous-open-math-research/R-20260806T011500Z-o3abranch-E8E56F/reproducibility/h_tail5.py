# -*- coding: utf-8 -*-
"""h_tail5.py: h over [0.55, b0] for R=1e5, 1e6 with fast solver + continuation in R."""
import sys, numpy as np, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from scipy.optimize import brentq

def cfg(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 8000), np.linspace(1.2, 3*np.pi, 8000)])
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx[:4]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(70):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    roots = sorted(set(np.round(r, 13) for r in roots))
    if len(roots) < 2: return None
    s1, s2 = roots[0], roots[1]
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    return dict(s1=s1, s2=s2, R1=s1*s1*y1a*y1a/n1 - s2*s2*y2a*y2a/n2,
                R2=s1*s1*y1b*y1b/n1 - s2*s2*y2b*y2b/n2, va=y2a/y1a, vb=y2b/y1b)

def branch(a, R, which, lo=None, hi=None):
    f = (lambda b: cfg(a, b, R)['R1']) if which=='g1' else (lambda b: cfg(a, b, R)['R2'])
    if lo is not None and hi is not None and lo > a:
        try:
            b0 = brentq(f, lo, hi, xtol=1e-11)
            c = cfg(a, b0, R)
            if (which=='g1' and c['va'] > 0) or (which=='g2' and c['vb'] < 0): return b0
        except Exception: pass
    bb = np.linspace(a+1e-5, 1-1e-5, 40)
    vals = [f(b) for b in bb]
    for i in range(len(bb)-1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i+1]) and vals[i]*vals[i+1] < 0:
            try: b0 = brentq(f, bb[i], bb[i+1], xtol=1e-11)
            except Exception: continue
            c = cfg(a, b0, R)
            if (which=='g1' and c['va'] > 0) or (which=='g2' and c['vb'] < 0): return b0
    return None

for R in [1e5, 1e6]:
    b0v = np.arccos(-0.25)/np.pi
    aa = np.linspace(0.55, b0v-2e-5, 21)
    g1s = []; g2s = []
    for j, a in enumerate(aa):
        g1 = None; g2 = None
        if j > 0 and g1s and g2s and g1s[-1] and g2s[-1]:
            g1 = branch(a, R, 'g1', g1s[-1]-1.5e-3, g1s[-1]+1.5e-3)
            g2 = branch(a, R, 'g2', g2s[-1]-1.5e-3, g2s[-1]+1.5e-3)
        if g1 is None: g1 = branch(a, R, 'g1')
        if g2 is None: g2 = branch(a, R, 'g2')
        g1s.append(g1); g2s.append(g2)
    hs = [g1-g2 if (g1 and g2) else None for g1, g2 in zip(g1s, g2s)]
    hps = [None]*len(aa)
    for j in range(1, len(aa)-1):
        if hs[j-1] is None or hs[j+1] is None: continue
        hps[j] = (hs[j+1]-hs[j-1])/(aa[j+1]-aa[j-1])
    print(f"R={R}:")
    for j in range(len(aa)):
        if hs[j] is not None:
            print(f"  a={aa[j]:.5f}: h={hs[j]:+.3e} h'={hps[j] if hps[j] is not None else 0:+.3e}")
