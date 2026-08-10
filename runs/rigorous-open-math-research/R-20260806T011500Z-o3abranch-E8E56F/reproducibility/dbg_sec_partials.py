import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
import numpy as np
from clean_lib import sec as secf
from mpmath import iv, mp, mpf
mp.dps = 80; iv.prec = 240
ns = {}
exec(open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\cert_ce1.py", encoding="utf-8").read().split("if __name__")[0], ns)
IAD = ns['IAD']; ad_sec = ns['ad_sec']; pt = ns['pt']

a, b, R = 0.57364, 0.5832744756851049, 1500.0
s1 = 0.528586829  # from earlier profile (approx; refine later)

# high-precision FD via mpmath
def mpsec(s, a, b, R):
    m = mp.sqrt(R)
    alpha = s*a; beta = s*(1-b); theta = s*m*(b-a)
    return mp.cos(beta)*mp.cos(theta)*mp.sin(alpha) - m*mp.sin(beta)*mp.sin(theta)*mp.sin(alpha) + (mp.cos(beta)*mp.sin(theta)/m)*mp.cos(alpha) + mp.sin(beta)*mp.cos(theta)*mp.cos(alpha)

eps = mpf('1e-40')
sa, sb, ss, sR = mpf(repr(a)), mpf(repr(b)), mpf(repr(s1)), mpf(repr(R))
# d/ds
f0 = mpsec(ss, sa, sb, sR)
fp = mpsec(ss+eps, sa, sb, sR); fm = mpsec(ss-eps, sa, sb, sR)
print("d sec/ds high-prec FD:", (fp-fm)/(2*eps))
fp = mpsec(ss, sa+eps, sb, sR); fm = mpsec(ss, sa-eps, sb, sR)
print("d sec/da high-prec FD:", (fp-fm)/(2*eps))
fp = mpsec(ss, sa, sb+eps, sR); fm = mpsec(ss, sa, sb-eps, sR)
print("d sec/db high-prec FD:", (fp-fm)/(2*eps))
# mpmath 1e-8 FD (to compare with numpy FD)
eps2 = mpf('1e-8')
fp = mpsec(ss, sa+eps2, sb, sR); fm = mpsec(ss, sa-eps2, sb, sR)
print("d sec/da FD 1e-8:", (fp-fm)/(2*eps2))
# numpy FD with the same 1e-6
def npfd(f, *args, i, h=1e-6):
    a1 = list(args); a2 = list(args); a1[i] += h; a2[i] -= h
    return (f(*a1) - f(*a2))/(2*h)
print("d sec/da numpy FD 1e-6:", npfd(secf, s1, a, b, R, i=1))
print("d sec/s  numpy FD 1e-6:", npfd(secf, s1, a, b, R, i=0))
# AD
A = pt(sa); B = pt(sb); Rm = pt(sR); S = pt(ss)
a3 = IAD(A, [iv.mpf(1), iv.mpf(0), iv.mpf(0)])
b3 = IAD(B, [iv.mpf(0), iv.mpf(1), iv.mpf(0)])
s3 = IAD(S, [iv.mpf(0), iv.mpf(0), iv.mpf(1)])
sec1 = ad_sec(s3, a3, b3, Rm)
print("AD sec a:", sec1.g[0])
print("AD sec b:", sec1.g[1])
print("AD sec s:", sec1.g[2])
