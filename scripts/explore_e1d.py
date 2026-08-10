# -*- coding: utf-8 -*-
"""E1 exploration v7: small-R endpoint h(a_max1); branch end structure (evidence only)."""
import numpy as np, time
src = open(r"F:\LaTeX\BVE research\scripts\explore_e1.py", encoding="utf-8").read()
exec(src.split('a0 = np.arccos')[0])
a0 = np.arccos(0.25)/np.pi; b0 = 1-a0

def trace_g1(R, n=60):
    """trace Gamma_1 from (a0,a0)-side: for each a, find b=g1(a) with R1(a,b)=0, a=x_-."""
    pts = []
    for a in np.linspace(a0+1e-4, 0.999, n):
        # find b in (a,1) with R1(a,b)=0 (x- sheet: a = x_-)
        bb = np.linspace(a+1e-5, 1-1e-5, 400)
        vals = np.array([residual_both(a, b, R)[0] for b in bb])
        ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
        idx = np.nonzero(ch)[0]
        best = None
        for i in idx:
            lo, hi = bb[i], bb[i+1]
            flo = residual_both(a, lo, R)[0]
            for _ in range(50):
                md = 0.5*(lo+hi)
                if np.signbit(residual_both(a, md, R)[0]) == np.signbit(flo): lo = md
                else: hi = md
            b = 0.5*(lo+hi)
            xm, xp = band(a, b, R)
            if xm == xm and abs(a-xm) < 3e-4:
                best = b; break
        if best is None: break
        pts.append((a, best))
    return pts

for R in [1.05, 1.1, 1.2, 1.5, 2.0, 3.0, 4.0]:
    t0=time.time()
    pts = trace_g1(R)
    if not pts:
        print(f"R={R}: no branch points"); continue
    a_last, b_last = pts[-1]
    # h(a_last): g2(a_last) via reflection formula g2(a)=1-g1^{-1}(1-a); approximate by locating b with R2=0 sign-consistent x+
    # simpler: g2(a) = 1 - a1 where a1 solves g1(a1)=1-a, i.e. R1(a1, 1-a)=0 with a1=x_-... approximate via the trace: find a1 in pts with b1 ~ 1-a
    # Use direct: g2(a) is b with R2(a,b)=0, b=x_+  -> solve R2(a,b)=0 in b with band check b=x_+
    def g2(a):
        bb = np.linspace(a+1e-5, 1-1e-5, 300)
        vals = np.array([residual_both(a, b, R)[1] for b in bb])
        ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
        for i in np.nonzero(ch)[0]:
            lo, hi = bb[i], bb[i+1]
            flo = residual_both(a, lo, R)[1]
            for _ in range(50):
                md = 0.5*(lo+hi)
                if np.signbit(residual_both(a, md, R)[1]) == np.signbit(flo): lo = md
                else: hi = md
            b = 0.5*(lo+hi)
            xm, xp = band(a, b, R)
            if xp == xp and abs(b-xp) < 3e-4:
                return b
        return None
    g2v = g2(a_last)
    print(f"R={R:g}: a_max1={a_last:.6f} g1(a_max1)={b_last:.6f}  g2(a_max1)={g2v if g2v is None else round(g2v,6)}  h(beta)={None if g2v is None else b_last-g2v:+.6f}  ({time.time()-t0:.1f}s)")