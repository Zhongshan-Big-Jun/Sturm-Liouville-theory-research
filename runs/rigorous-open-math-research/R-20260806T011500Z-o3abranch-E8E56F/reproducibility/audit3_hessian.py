# -*- coding: utf-8 -*-
"""audit3.py: T3 exact check + Hessian of D over grids (negative-definiteness test)."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import roots2, R1_R2, sec

def sec_single(s, a, b, R):
    return float(sec(s, a, b, R))

def roots2s(a, b, R):
    from scipy.optimize import brentq
    s1 = brentq(lambda s: sec_single(s, a, b, R), 1e-8, np.pi)
    s2 = brentq(lambda s: sec_single(s, a, b, R), np.pi, 2*np.pi+0.5)
    return s1, s2

def lam2(a, b, R):
    s1, s2 = roots2s(a, b, R)
    return s1*s1, s2*s2

def D_ab_hess(a, b, R, h=1e-5):
    l_pp = lam2(a+h, b+h, R); l_pm = lam2(a+h, b-h, R); l_mp = lam2(a-h, b+h, R); l_mm = lam2(a-h, b-h, R)
    Dpp = l_pp[1]-l_pp[0]; Dpm = l_pm[1]-l_pm[0]; Dmp = l_mp[1]-l_mp[0]; Dmm = l_mm[1]-l_mm[0]
    Daa = (Dpp - 2*(lam2(a,b,R)[1]-lam2(a,b,R)[0]) + Dmm)/(h*h)
    Dbb = (Dpp - 2*(lam2(a,b,R)[1]-lam2(a,b,R)[0]) + Dpm)/(h*h)
    Dab = (Dpp - Dpm - Dmp + Dmm)/(4*h*h)
    return Daa, Dbb, Dab

print("=== T3 (dR1/db = -dR2/da) ===")
for (a, b, R) in [(0.42,0.56,4.0),(0.451485465757,0.548514534243,4.0),(0.45,0.55,10.0),(0.3,0.7,2.0)]:
    h = 1e-6
    R1p, R2p = R1_R2(a, b+h, R); R1m, R2m = R1_R2(a, b-h, R)
    R1b = (R1p-R1m)/(2*h)
    R1r, R2r = R1_R2(a+h, b, R); R1l, R2l = R1_R2(a-h, b, R)
    R2a = (R2r-R2l)/(2*h)
    print(f"  ({a},{b},R={R}): dR1/db={R1b:+.6f}  -dR2/da={-R2a:+.6f}  sum={R1b+R2a:.2e}")

print("=== Hessian of D (negative definiteness?) ===")
for R in [1.2, 2.0, 4.0, 10.0, 100.0]:
    nviol = 0; ntot = 0
    for a in np.linspace(0.08, 0.62, 14):
        for b in np.linspace(a+0.03, min(0.97, a+0.5), 10):
            ntot += 1
            try:
                Daa, Dbb, Dab = D_ab_hess(a, b, R)
            except Exception:
                continue
            negdef = (Daa < 0) and (Dbb < 0) and (Daa*Dbb - Dab*Dab > 0)
            if not negdef:
                nviol += 1
                if nviol <= 3:
                    print(f"  R={R}: VIOLATION at ({a:.3f},{b:.3f}): Daa={Daa:.2f} Dbb={Dbb:.2f} Dab={Dab:.2f}")
    print(f"  R={R}: {nviol}/{ntot} violations of negative definiteness")
