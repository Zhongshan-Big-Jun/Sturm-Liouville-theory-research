# -*- coding: utf-8 -*-
"""analyze_4.py: roots of R1(b0,·) and v(b0) signs."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T200000Z-o3a-c1b-7F3A9B\reproducibility")
import fast_lib as F
A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0
for R in [2.0, 3.0, 4.0, 10.0, 100.0, 1000.0]:
    print(f"--- R={R} ---")
    bs = np.linspace(B0+1e-5, 0.999, 600)
    vals = np.array([F.R1R2(B0, b, R)[0] for b in bs])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    for i in np.nonzero(ch)[0]:
        lo, hi = bs[i], bs[i+1]
        for _ in range(50):
            md = 0.5*(lo+hi)
            if np.signbit(F.R1R2(B0, md, R)[0]) == np.signbit(F.R1R2(B0, lo, R)[0]): lo = md
            else: hi = md
        b = 0.5*(lo+hi)
        s1,s2 = F.roots2_fast(B0,b,R)
        n1,n2 = F.norm_n(s1,B0,b,R), F.norm_n(s2,B0,b,R)
        q = (s1/s2)*np.sqrt(n2/n1)
        vb = F.y_at(s2,B0,b,R,B0)/F.y_at(s1,B0,b,R,B0)
        typ = "x_- (v=+q)" if vb > 0 else "x_+ (v=-q)"
        print(f"   root b={b:.6f}: v(b0)={vb:+.6f} q={q:.6f} -> {typ} |v|-q={abs(vb)-q:+.2e}")
