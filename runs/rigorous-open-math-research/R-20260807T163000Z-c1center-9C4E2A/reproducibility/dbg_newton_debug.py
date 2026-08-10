# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_lib import F_iv, Fs_iv
from fast_lib import cfg

def P(x): return iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))
def I(lo, hi): return iv.mpf((mp.mpf(float(lo)), mp.mpf(float(hi))))
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
b = 0.6
s1f, s2f, _, _ = cfg(a0, b, 1.0005)
a_iv, b_iv, R_iv = I(a0-0.03, a0+0.03), I(b-0.01, b+0.01), I(1.0, 1.001)
sg = s1f; w = 0.02
s = I(sg - w, sg + w)
print("s1f = %.12f" % s1f)
for it in range(12):
    sm = P(0.5*(float(s.a)+float(s.b)))
    Fs = Fs_iv(s, a_iv, b_iv, R_iv)
    print("it%d: s=[%.10f, %.10f]  Fs=[%.3f, %.3f]" % (it, float(s.a), float(s.b), float(Fs.a), float(Fs.b)))
    if not (Fs.a > 0 or Fs.b < 0):
        print("  Fs sign fail"); break
    N = sm - F_iv(sm, a_iv, b_iv, R_iv) / Fs
    lo = max(s.a, N.a); hi = min(s.b, N.b)
    print("   N=[%.10f, %.10f] lo=%.10f hi=%.10f" % (float(N.a), float(N.b), float(lo), float(hi)))
    if lo > hi:
        print("  empty intersection"); break
    s = I(float(lo), float(hi))
