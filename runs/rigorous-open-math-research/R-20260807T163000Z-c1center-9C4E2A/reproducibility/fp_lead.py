# -*- coding: utf-8 -*-
"""fp_lead.py: solve xi*tan(2*pi*xi) = 1/(2*sqrt(2)*pi) and compare with data;
check kappa-bar = 2(tan(2pi xi)-2pi xi), lambda2 = 4pi^2 - 4pi*kappa/sqrt(R)."""
import mpmath as mp
mp.mp.dps = 30
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n
from c1trace_lib import a_fp

target = mp.mpf(1)/(2*mp.sqrt(2)*mp.pi)
def F(x): return x*mp.tan(2*mp.pi*x) - target
# root in (0.1, 0.13)
lo, hi = mp.mpf('0.10'), mp.mpf('0.13')
fl = F(lo)
for _ in range(80):
    md = (lo+hi)/2
    if F(md)*fl < 0: hi = md
    else: lo = md
xi_star = (lo+hi)/2
kap_star = 2*(mp.tan(2*mp.pi*xi_star) - 2*mp.pi*xi_star)
print("xi* =", mp.nstr(xi_star,14), " kappa-bar* =", mp.nstr(kap_star,12))

def roots2(a, b, R):
    s = np.linspace(1e-9, 2*np.pi+0.6, 4001)
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0][:2]
    out = []
    for i in idx:
        lo, hi = s[i], s[i+1]; flo = M[i]
        for _ in range(60):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        out.append(0.5*(lo+hi))
    return out

for R in [1e4, 1e6, 1e8]:
    fp = a_fp(R)
    delta = 0.5 - fp
    xi = delta*np.sqrt(R)
    s1, s2 = roots2(fp, 1-fp, R)
    kap = (2*np.pi - s2)*np.sqrt(R)
    l1R = s1**2*np.sqrt(R)          # lambda1*sqrt(R) -> 2/xi
    l2shift = (4*np.pi**2 - s2**2)*np.sqrt(R)   # -> 4*pi*kappa
    print("R=%.0e: xi=%.8f (xi*=%.8f) kap=%.8f (kap*=%.8f) l1*sqrtR=%.6f (2/xi=%.6f) l2shift*sqrtR=%.6f (4pi kap*=%.6f)" % (
        R, xi, float(xi_star), kap, float(kap_star), l1R, 2/float(xi_star), l2shift, 4*np.pi*float(kap_star)))

