# -*- coding: utf-8 -*-
"""fp_largeR.py: symmetric-line fixed point + local A,B,C,h' at fp, large R. Cheap."""
import sys, json, time
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from scipy.optimize import brentq

def roots2_fast(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 9000), np.linspace(1.2, 3*np.pi, 9000)])
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
    return roots[0], roots[1]

def R1R2(a, b, R):
    rr = roots2_fast(a, b, R)
    if rr is None: return None
    s1, s2 = rr
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    return dict(s1=s1, s2=s2, l1=s1*s1, l2=s2*s2,
                R1=s1*s1*y1a*y1a/n1 - s2*s2*y2a*y2a/n2,
                R2=s1*s1*y1b*y1b/n1 - s2*s2*y2b*y2b/n2,
                va=y2a/y1a, vb=y2b/y1b)

def fp_sym(R, u0=None):
    """solve R1(u, 1-u) = 0 for u in (0,1/2)."""
    if u0 is None:
        u0 = 0.5 - 0.118/np.sqrt(R)
    def F(u):
        info = R1R2(u, 1-u, R)
        if info is None: return 1.0
        return info['R1']
    # bracket
    lo, hi = 1e-6, 0.5-1e-6
    for _ in range(60):
        md = 0.5*(lo+hi)
        if F(md)*F(lo) > 0: lo = md
        else: hi = md
    u = 0.5*(lo+hi)
    info = R1R2(u, 1-u, R)
    return u, info

def hp_at(a, b, R, h=1e-6):
    c = R1R2(a, b, R)
    ap = R1R2(a+h, b, R); am = R1R2(a-h, b, R)
    bp = R1R2(a, b+h, R); bm = R1R2(a, b-h, R)
    A = (ap['R1']-am['R1'])/(2*h)
    B = (ap['R2']-am['R2'])/(2*h)
    C = (bp['R2']-bm['R2'])/(2*h)
    R1b = (bp['R1']-bm['R1'])/(2*h)
    g1p = A/B; g2p = -B/C
    return dict(A=A, B=B, C=C, T3=R1b+B, g1p=g1p, g2p=g2p, hp=g1p-g2p)

if __name__ == "__main__":
    Rs = [float(x) for x in sys.argv[1:]] or [50.0, 100.0, 200.0, 500.0, 1000.0, 5000.0, 1e4, 1e5, 1e6, 1e7]
    results = []
    for R in Rs:
        t0 = time.time()
        u, info = fp_sym(R)
        row = dict(R=R, u=u, b=1-u, delta=0.5-u, l1=info['l1'], l2=info['l2'], D=info['l2']-info['l1'],
                   R1=info['R1'], R2=info['R2'], va=info['va'], vb=info['vb'])
        try:
            hp = hp_at(u, 1-u, R)
            row.update(hp)
        except Exception as e:
            row['hp_err'] = str(e)
        print(json.dumps(row))
        results.append(row)
    with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\fp_largeR.json", "w") as f:
        json.dump(results, f, indent=1)
    print("saved fp_largeR.json")
