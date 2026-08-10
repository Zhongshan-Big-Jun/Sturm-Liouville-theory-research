import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import norm_n
from mpmath import iv, mp, mpf
mp.dps = 60; iv.prec = 220
ns = {}
exec(open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\cert_ce1.py", encoding="utf-8").read().split("if __name__")[0], ns)
IAD = ns['IAD']; _norm_ad = ns['_norm_ad']; pt = ns['pt']

a, b, R = 0.57364, 0.5832744756851049, 1500.0
s1 = 0.528586829
def fd_norm(s):
    return (norm_n(s+1e-6, a, b, R) - norm_n(s-1e-6, a, b, R))/(2e-6)
print("FD dn1/ds1:", fd_norm(s1))
print("FD n1:", norm_n(s1, a, b, R))
A = pt(mpf(repr(a))); B = pt(mpf(repr(b))); Rm = pt(iv.sqrt(pt(mpf(repr(R))))); S = pt(mpf(repr(s1)))
# AD with vars (a, b, s)
a3 = IAD(A, [iv.mpf(1), iv.mpf(0), iv.mpf(0)])
b3 = IAD(B, [iv.mpf(0), iv.mpf(1), iv.mpf(0)])
s3 = IAD(S, [iv.mpf(0), iv.mpf(0), iv.mpf(1)])
n = _norm_ad(s3, a3, b3, Rm, pt(mpf(repr(R))))
print("AD n1 value:", n.v)
print("AD dn1/da:", n.g[0])
print("AD dn1/db:", n.g[1])
print("AD dn1/ds:", n.g[2])
# also FD wrt a and b
def fd_norm_a(s, a_):
    return (norm_n(s, a_+1e-6, b, R) - norm_n(s, a_-1e-6, b, R))/(2e-6)
def fd_norm_b(s, b_):
    return (norm_n(s, a, b_+1e-6, R) - norm_n(s, a, b_-1e-6, R))/(2e-6)
print("FD dn1/da:", fd_norm_a(s1, a))
print("FD dn1/db:", fd_norm_b(s1, b))
