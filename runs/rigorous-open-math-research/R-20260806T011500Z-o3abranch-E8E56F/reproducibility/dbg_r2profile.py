import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from mpmath import iv, mp, mpf
mp.dps = 60; iv.prec = 220

def roots2(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 12000), np.linspace(1.2, 3*np.pi, 12000)])
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx[:6]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(70):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    roots = sorted(set(np.round(r, 13) for r in roots))
    return roots

def r2_float(a, b, R, s1, s2):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1*s1*y_at(s1, a, b, R, b)**2/n1 - s2*s2*y_at(s2, a, b, R, b)**2/n2

a, R = 0.57364, 1500.0
for b in [0.574, 0.575, 0.576, 0.57601, 0.577, 0.578, 0.579, 0.58]:
    rs = roots2(a, b, R)
    print(f"b={b}: nroots={len(rs)} s={[round(x,6) for x in rs[:4]]}")
    if len(rs) >= 2:
        v = r2_float(a, b, R, rs[0], rs[1])
        va = np.sin(rs[1]*a)/rs[1]/(np.sin(rs[0]*a)/rs[0])
        print(f"   R2={v:+.6e}  v(a)={va:+.4f}")
