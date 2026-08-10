# -*- coding: utf-8 -*-
"""h_trace.py: trace h=g1-g2 over common range, count zeros, check h(b0), for R in {1000, 3000, 1e4, 1e5}."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from scipy.optimize import brentq

def cfg(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 10000), np.linspace(1.2, 3*np.pi, 10000)])
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx[:4]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(80):
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

def branch(a, R, which):
    bb = np.linspace(a+1e-5, 1-1e-5, 60)
    f = (lambda b: cfg(a, b, R)['R1']) if which=='g1' else (lambda b: cfg(a, b, R)['R2'])
    vals = [f(b) for b in bb]
    for i in range(len(bb)-1):
        if vals[i]*vals[i+1] < 0:
            try:
                b0 = brentq(f, bb[i], bb[i+1], xtol=1e-13)
            except Exception:
                continue
            c = cfg(a, b0, R)
            if c is None: continue
            if which=='g1' and c['va'] > 0: return b0
            if which=='g2' and c['vb'] < 0: return b0
    return None

for R in [1000.0, 3000.0, 10000.0, 100000.0]:
    a0v = np.arccos(0.25)/np.pi; b0v = np.arccos(-0.25)/np.pi
    aa = np.linspace(a0v+1e-4, b0v-1e-4, 41)
    hh = []
    for a in aa:
        g1 = branch(a, R, 'g1'); g2 = branch(a, R, 'g2')
        if g1 is None or g2 is None:
            hh.append((a, None)); continue
        hh.append((a, g1-g2))
    # zeros by sign changes
    zs = []
    for i in range(len(hh)-1):
        h0, h1 = hh[i][1], hh[i+1][1]
        if h0 is None or h1 is None: continue
        if h0*h1 < 0:
            # refine
            f = lambda t: branch(aa[i]+t*(aa[i+1]-aa[i]), R, 'g1') - branch(aa[i]+t*(aa[i+1]-aa[i]), R, 'g2')
            t0 = brentq(f, 0, 1, xtol=1e-10)
            zs.append(aa[i]+t0*(aa[i+1]-aa[i]))
    # h at b0
    g1b = branch(b0v-1e-5, R, 'g1')
    hL = hh[0][1]; hR = hh[-1][1]
    print(f"R={R}: h(a0+)={hL:+.5f} h(b0-)={hR:+.5f} zeros={[round(z,6) for z in zs]} n_zeros={len(zs)}")
