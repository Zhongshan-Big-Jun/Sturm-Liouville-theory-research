# -*- coding: utf-8 -*-
import sys, math
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import numpy as np
from gap_lib import lams_fast

def D_of(rho_blocks):
    s = lams_fast(rho_blocks, 2, npts=20000)
    return s[1]**2 - s[0]**2

# 1) R=4 symmetric critical values
R = 4.0
def sym_sup(u, R):
    return [ (u, 1.0), (1-2*u, R), (u, 1.0) ]
def sym_inf(u, R):
    return [ (u, R), (1-2*u, 1.0), (u, R) ]

for name, fam, ustar, Dstar in [
    ("SUP", sym_sup, 0.45148546584, 32.6139836177),
    ("INF", sym_inf, 0.3825982568, 6.7844823391),
]:
    D = D_of(fam(ustar, R))
    print(name, "D* computed %.8f  expected %.8f  diff %.2e" % (D, Dstar, abs(D-Dstar)))
    # scan around
    us = np.linspace(0.30, 0.49, 381)
    vals = [D_of(fam(u, R)) for u in us]
    print("  max/min over scan: %.8f / %.8f at u=%.6f, %.6f" % (max(vals), min(vals), us[np.argmax(vals)], us[np.argmin(vals)]))

# 2) two-block bound 3pi^2/R < D < 3pi^2
pi2 = math.pi**2
worst_lo = 1e9; worst_hi = -1e9
for R in [1.05, 1.5, 4.0, 100.0, 1e4]:
    for t in np.linspace(0.02, 0.98, 25):
        D = D_of([(t, 1.0), (1-t, R)])
        lo = 3*pi2/R; hi = 3*pi2
        assert D > lo and D < hi, (R, t, D, lo, hi)
        worst_lo = min(worst_lo, D-lo); worst_hi = min(worst_hi, hi-D)
print("two-block bound: min margin lo %.3e  hi %.3e  OK" % (worst_lo, worst_hi))

# 3) f_sym(1/2) = 2 pi^2 : rho=1 config
s = lams_fast([(1.0, 1.0)], 2)
lam1, lam2 = s[0]**2, s[1]**2
# u1(1/2) = sqrt(2) sin(pi/2)=sqrt2; u2(1/2)=0 (L2 normalized on [0,1] rho=1)
f = lam1*2.0 - lam2*0.0
print("f_sym(1/2) = %.6f vs 2pi^2 = %.6f" % (f, 2*pi2))

# 4) q=1 base value
v = 4*math.pi/(3*math.sqrt(3))
print("q=1 base 4pi/(3 sqrt3) = %.10f" % v)
print("minima from handoff: A-C>=2.8086, B-D>=-0.3751 -> sum %.4f > %.6f" % (2.8086-0.3751, v))