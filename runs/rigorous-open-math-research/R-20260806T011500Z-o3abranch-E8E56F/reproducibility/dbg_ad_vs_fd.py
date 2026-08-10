import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
import numpy as np
from clean_lib import sec, norm_n, y_at
from mpmath import iv, mp, mpf
mp.dps = 60; iv.prec = 220
ns = {}
exec(open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\cert_ce1.py", encoding="utf-8").read().split("if __name__")[0], ns)
IAD = ns['IAD']; ad_sec = ns['ad_sec']; ad_r1 = ns['ad_r1']; ad_r2 = ns['ad_r2']; pt = ns['pt']

a, b, R = 0.57364, 0.5832744756851049, 1500.0
s1, s2 = 0.528586829, 5.452887300

def fd(f, *args, i, h=1e-6):
    a1 = list(args); a2 = list(args); a1[i] += h; a2[i] -= h
    return (f(*a1) - f(*a2))/(2*h)

def r1f(a, b, R, s1, s2):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1*s1*(np.sin(s1*a)/s1)**2/n1 - s2*s2*(np.sin(s2*a)/s2)**2/n2

def r2f(a, b, R, s1, s2):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    yb1 = s1 * y_at(s1, a, b, R, b); yb2 = s2 * y_at(s2, a, b, R, b)
    return yb1*yb1/n1 - yb2*yb2/n2

print("FD sec: a=%+.6f b=%+.6f s=%+.6f" % (fd(sec, s1, a, b, R, i=1), fd(sec, s1, a, b, R, i=2), fd(sec, s1, a, b, R, i=0)))
print("FD r1 : a=%+.6f b=%+.6f s1=%+.6f s2=%+.6f" % (fd(r1f, a, b, R, s1, s2, i=0), fd(r1f, a, b, R, s1, s2, i=1), fd(r1f, a, b, R, s1, s2, i=3), fd(r1f, a, b, R, s1, s2, i=4)))
print("FD r2 : a=%+.6f b=%+.6f s1=%+.6f s2=%+.6f" % (fd(r2f, a, b, R, s1, s2, i=0), fd(r2f, a, b, R, s1, s2, i=1), fd(r2f, a, b, R, s1, s2, i=3), fd(r2f, a, b, R, s1, s2, i=4)))

A = pt(mpf(repr(a))); B = pt(mpf(repr(b))); Rm = pt(iv.sqrt(pt(mpf(repr(R))))); Rd = pt(mpf(repr(R))); S1 = pt(mpf(repr(s1))); S2 = pt(mpf(repr(s2)))
a3 = IAD(A, [iv.mpf(1), iv.mpf(0), iv.mpf(0)])
b3 = IAD(B, [iv.mpf(0), iv.mpf(1), iv.mpf(0)])
s13 = IAD(S1, [iv.mpf(0), iv.mpf(0), iv.mpf(1)])
sec1 = ad_sec(s13, a3, b3, Rm)
print("AD sec: a=%s b=%s s=%s" % tuple(sec1.g))
a4 = IAD(A, [iv.mpf(1), iv.mpf(0), iv.mpf(0), iv.mpf(0)])
b4 = IAD(B, [iv.mpf(0), iv.mpf(1), iv.mpf(0), iv.mpf(0)])
s14 = IAD(S1, [iv.mpf(0), iv.mpf(0), iv.mpf(1), iv.mpf(0)])
s24 = IAD(S2, [iv.mpf(0), iv.mpf(0), iv.mpf(0), iv.mpf(1)])
r1 = ad_r1(a4, b4, s14, s24, Rm, Rd)
print("AD r1 : a=%s b=%s s1=%s s2=%s" % tuple(r1.g))
r2 = ad_r2(a4, b4, s14, s24, Rm, Rd)
print("AD r2 : a=%s b=%s s1=%s s2=%s" % tuple(r2.g))