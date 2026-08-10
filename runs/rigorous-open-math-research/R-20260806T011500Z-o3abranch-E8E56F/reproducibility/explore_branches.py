# -*- coding: utf-8 -*-
"""explore_branches.py: precise branch structure for O3a (Lemmas A/B/C audit).
Reproduces and extends the prior run: fixed points, good branch ranges, slopes h'.
"""
import sys, json, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
import numpy as np
from agentB_lib import config, f_at, zeros_f

def R1(a, b, R):
    return float(f_at(a, b, R, a, config(a, b, R)))
def R2(a, b, R):
    return float(f_at(a, b, R, b, config(a, b, R)))

def good_roots_r1(a, R, nb=320, tol=1e-6):
    """all b in (a,1) with R1=0 and a=x_- (left good)."""
    bs = np.linspace(a+1e-6, 1-1e-6, nb)
    vals = np.array([R1(a, b, R) for b in bs])
    out = []
    for i in range(len(bs)-1):
        if vals[i]*vals[i+1] < 0:
            lo, hi = bs[i], bs[i+1]
            for _ in range(60):
                m = 0.5*(lo+hi)
                if R1(a,m,R)*R1(a,lo,R) < 0: hi = m
                else: lo = m
            b2 = 0.5*(lo+hi)
            z = zeros_f(a, b2, R)
            if z is not None and abs(a-z[0]) < tol:
                out.append(b2)
    return out

def good_roots_r2(a, R, nb=320, tol=1e-6):
    """all b in (a,1) with R2=0 and b=x_+ (right good)."""
    bs = np.linspace(a+1e-6, 1-1e-6, nb)
    vals = np.array([R2(a, b, R) for b in bs])
    out = []
    for i in range(len(bs)-1):
        if vals[i]*vals[i+1] < 0:
            lo, hi = bs[i], bs[i+1]
            for _ in range(60):
                m = 0.5*(lo+hi)
                if R2(a,m,R)*R2(a,lo,R) < 0: hi = m
                else: lo = m
            b2 = 0.5*(lo+hi)
            z = zeros_f(a, b2, R)
            if z is not None and abs(b2-z[1]) < tol:
                out.append(b2)
    return out

def branch_ranges(R, na=200):
    """direct-sample a-grid; returns g1 pts, g2 pts as (a,b) arrays over good branches."""
    a1lo, a1hi = 0.30, 0.75
    aa = np.linspace(a1lo, a1hi, na)
    g1 = []; g2 = []
    for a in aa:
        r1 = good_roots_r1(a, R)
        r2 = good_roots_r2(a, R)
        if len(r1) == 1: g1.append((a, r1[0]))
        elif len(r1) > 1: g1.append((a, r1))  # multiple - flag
        if len(r2) == 1: g2.append((a, r2[0]))
        elif len(r2) > 1: g2.append((a, r2))
    return g1, g2

def fp_find(R, seed=(0.45, 0.55), steps=200):
    """find good root of (R1,R2)=0 by least-squares-style search: minimize R1^2+R2^2."""
    from scipy.optimize import least_squares
    def res(p):
        a, b = p
        if not (1e-6 < a < b < 1-1e-6): return [1e3, 1e3]
        return [R1(a,b,R), R2(a,b,R)]
    sol = least_squares(res, seed, bounds=([1e-6,1e-6],[1-1e-6,1-1e-6]), xtol=1e-14, ftol=1e-14)
    a, b = sol.x
    z = zeros_f(a, b, R)
    if z is not None and abs(a-z[0]) < 1e-5 and abs(b-z[1]) < 1e-5:
        return (a, b)
    return None

def slopes_at(a, b, R, h=1e-5):
    """A=R1_a(total), B=R2_a, C=R2_b via central differences; g1',g2' via branch formulas."""
    A = (R1(a+h,b,R)-R1(a-h,b,R))/(2*h)
    B = (R2(a+h,b,R)-R2(a-h,b,R))/(2*h)
    C = (R2(a,b+h,R)-R2(a,b-h,R))/(2*h)
    # T3 check: R1_b + R2_a
    R1b = (R1(a,b+h,R)-R1(a,b-h,R))/(2*h)
    return dict(A=A, B=B, C=C, R1b=R1b, T3resid=R1b+B)

if __name__ == "__main__":
    Rs = [float(x) for x in sys.argv[1:]] or [1.05, 2.0, 4.0, 10.0, 100.0]
    for R in Rs:
        t0 = time.time()
        fp = fp_find(R)
        g1, g2 = branch_ranges(R, na=120)
        print(f"R={R}: fp={fp} t={time.time()-t0:.0f}s")
        if fp:
            s = slopes_at(*fp, R)
            print(f"   A={s['A']:.6g} B={s['B']:.6g} C={s['C']:.6g} T3={s['T3resid']:.2e}")
            g1p = s['A']/s['B']; g2p = -s['B']/s['C']
            print(f"   g1'(fp)={g1p:.6g} g2'(fp)={g2p:.6g} h'(fp)={g1p-g2p:.6g}")
        print(f"   Gamma_1 pts: {len(g1)}  Gamma_2 pts: {len(g2)}")
        if g1:
            a1 = [p[0] for p in g1 if isinstance(p[1], float)]
            print(f"   G1 a-range: [{min(a1):.4f}, {max(a1):.4f}]")
        if g2:
            a2 = [p[0] for p in g2 if isinstance(p[1], float)]
            print(f"   G2 a-range: [{min(a2):.4f}, {max(a2):.4f}]")
