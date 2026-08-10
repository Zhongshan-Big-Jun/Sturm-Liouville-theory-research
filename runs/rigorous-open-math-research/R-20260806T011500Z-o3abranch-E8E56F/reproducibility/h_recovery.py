# -*- coding: utf-8 -*-
"""h_recovery.py: h on [0.574, b0] at R=1e5 (recovery check) + h(b0) via cfg."""
import sys, numpy as np
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

R = 1e5; b0v = np.arccos(-0.25)/np.pi
print("=== R=1e5 recovery region [0.5745, b0] ===")
for a in [0.5745, 0.5755, 0.5765, 0.5775, 0.5785, 0.5795, 0.58030, 0.58040]:
    g1 = branch(a, R, 'g1'); g2 = branch(a, R, 'g2')
    if g1 and g2:
        print(f"  a={a:.5f}: g1={g1:.6f} g2={g2:.6f} h={g1-g2:+.3e}")
    else:
        print(f"  a={a:.5f}: branch missing (g1={g1}, g2={g2})")
# h(b0) via cfg with fine scan
a = b0v - 1e-7
bb = np.linspace(a+1e-6, a+0.01, 150)
vals = [cfg(a, b, R)['R1'] for b in bb]
for i in range(len(bb)-1):
    if vals[i]*vals[i+1] < 0:
        g1 = brentq(lambda b: cfg(a, b, R)['R1'], bb[i], bb[i+1], xtol=1e-12)
        c = cfg(a, g1, R)
        print(f"  h(b0) via cfg: g1={g1:.8f} h={g1-b0v:+.3e} va={c['va']:.2e} h*sqrtR={(g1-b0v)*np.sqrt(R):.4f}")
        break
