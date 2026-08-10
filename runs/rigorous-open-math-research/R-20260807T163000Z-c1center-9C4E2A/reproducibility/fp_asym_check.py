# -*- coding: utf-8 -*-
"""fp_asym_check.py: verify the R->inf fp asymptotics.
Leading-order system: xi = delta*sqrt(R) solves xi*tan(2*pi*xi) = 1/(2*sqrt(2)*pi);
kappa = s2 shift: lambda2 = 4 pi^2 - 4 pi kappa, kappa/(2 eps) = tan(2 pi xi) - 2 pi xi.
"""
import mpmath as mp
mp.mp.dps = 40
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n
from c1trace_lib import a_fp

# 1. solve xi*tan(2 pi xi) = 1/(2 sqrt2 pi)
target = mp.mpf(1)/(2*mp.sqrt(2)*mp.pi)
def F(x): return x*mp.tan(2*mp.pi*x) - target
lo, hi = mp.mpf('0.05'), mp.mpf('0.5')
for _ in range(80):
    md = (lo+hi)/2
    if F(md) < 0: lo = md
    else: hi = md
xi_star = (lo+hi)/2
print("xi_star =", mp.nstr(xi_star, 15), " 2pi xi =", mp.nstr(2*mp.pi*xi_star, 10))
print("check xi*tan =", mp.nstr(xi_star*mp.tan(2*mp.pi*xi_star), 15))

for R in [1e3, 1e4, 1e5, 1e6, 1e7]:
    fp = a_fp(R)
    delta = 0.5 - fp
    xi = delta*np.sqrt(R)
    print("R=%.0e: delta=%.6e xi=%.6f  err xi-xi* = %.2e" % (R, delta, xi, xi - float(xi_star)))
