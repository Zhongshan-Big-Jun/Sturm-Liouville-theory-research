# -*- coding: utf-8 -*-
"""minhp_largeR.py: min h' over common range [a0, b0] for large R; branch points via brentq."""
import sys, json, time
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from scipy.optimize import brentq

def cfg(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 7000), np.linspace(1.2, 3*np.pi, 7000)])
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
                R2=s1*s1*y1b*y1b/n1 - s2*s2*y2b*y2b/n2,
                va=y2a/y1a, vb=y2b/y1b)

def branch(a, R, which):
    """which='g1': solve R1(a,b)=0 with va>0; 'g2': R2(a,b)=0 with vb<0."""
    bb = np.linspace(a+1e-4, 1-1e-4, 40)
    vals = []
    for b in bb:
        c = cfg(a, b, R)
        vals.append(c['R1'] if which=='g1' else c['R2'] if c else np.nan)
    for i in range(len(bb)-1):
        v0, v1 = vals[i], vals[i+1]
        if not (np.isfinite(v0) and np.isfinite(v1) and v0*v1 < 0):
            continue
        lo, hi = bb[i], bb[i+1]
        f = (lambda b: cfg(a, b, R)['R1']) if which=='g1' else (lambda b: cfg(a, b, R)['R2'])
        try:
            b0 = brentq(f, lo, hi, xtol=1e-12)
        except Exception:
            continue
        c = cfg(a, b0, R)
        if c is None: continue
        if which=='g1' and c['va'] > 0: return b0
        if which=='g2' and c['vb'] < 0: return b0
    return None

def hp_at_branch(a, b, R, h=1e-6):
    ap = cfg(a+h, b, R); am = cfg(a-h, b, R); bp = cfg(a, b+h, R); bm = cfg(a, b-h, R)
    if None in (ap, am, bp, bm): return None
    A = (ap['R1']-am['R1'])/(2*h)
    B = (ap['R2']-am['R2'])/(2*h)
    C = (bp['R2']-bm['R2'])/(2*h)
    return A, B, C

if __name__ == "__main__":
    a0v = np.arccos(0.25)/np.pi; b0v = np.arccos(-0.25)/np.pi
    Rs = [float(x) for x in sys.argv[1:]] or [100.0, 1000.0, 1e4]
    out = []
    for R in Rs:
        t0 = time.time()
        aa = np.linspace(a0v+1e-4, b0v-1e-4, 25)
        rows = []
        for a in aa:
            g1 = branch(a, R, 'g1'); g2 = branch(a, R, 'g2')
            if g1 is None or g2 is None: continue
            h1 = hp_at_branch(a, g1, R); h2 = hp_at_branch(a, g2, R)
            if h1 is None or h2 is None: continue
            A1, B1, C1 = h1; A2, B2, C2 = h2
            g1p = A1/B1; g2p = -B2/C2
            rows.append(dict(a=a, g1=g1, g2=g2, h=g1-g2, g1p=g1p, g2p=g2p, hp=g1p-g2p))
        rows = [r for r in rows if r['g1'] < 1-1e-3 and r['g2'] > r['a']+1e-3]
        if rows:
            hpmin = min(rows, key=lambda r: r['hp'])
            print(f"R={R}: n={len(rows)} min_hp={hpmin['hp']:.5f} at a={hpmin['a']:.5f} h_L={rows[0]['hp']:.4f} h_R={rows[-1]['hp']:.4f} t={time.time()-t0:.0f}s")
            out.append(dict(R=R, min_hp=hpmin['hp'], at=hpmin['a'], rows=rows))
        else:
            print(f"R={R}: no branch rows")
    json.dump(out, open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\minhp_largeR.json","w"), indent=1)
