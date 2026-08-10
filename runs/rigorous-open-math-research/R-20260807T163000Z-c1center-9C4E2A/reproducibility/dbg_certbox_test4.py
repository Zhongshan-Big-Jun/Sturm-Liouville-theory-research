# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_lib import F_iv, Fs_iv, Fa_iv, Fb_iv
from fast_lib import cfg
import numpy as np

def P(x): return iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))
def I(lo, hi): return iv.mpf((mp.mpf(float(lo)), mp.mpf(float(hi))))

def cert_root_one(a_iv, b_iv, R_iv, sg, w=5e-3, iters=15, wmin=1e-10):
    s = I(sg - w, sg + w)
    for _ in range(iters):
        sm = P(0.5*(float(s.a)+float(s.b)))
        Fs = Fs_iv(s, a_iv, b_iv, R_iv)
        if not (Fs.a > 0 or Fs.b < 0):
            return None
        N = sm - F_iv(sm, a_iv, b_iv, R_iv) / Fs
        lo = max(s.a, N.a); hi = min(s.b, N.b)
        if lo > hi: return None
        s = I(float(lo), float(hi))
        if float(s.b - s.a) < wmin:
            return s
    return s if (float(s.b-s.a) < 1e-3) else None

a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
# measure |F_b|, |F_R|, |F_a| at points (s ~ k pi)
for b in (0.5, 0.7, 0.9, 0.99, 0.999):
    s1f, s2f, _, _ = cfg(a0, b, 1.0005)
    for (k, sf) in ((1, s1f), (2, s2f)):
        fb = float(abs(Fb_iv(P(sf), P(a0), P(b), P(1.0005)).a))
        fr = float(abs(mp.diff(lambda R: F_iv(P(sf), P(a0), P(b), P(R)).a, 1.0, 1)))
        fa = float(abs(Fa_iv(P(sf), P(a0), P(b), P(1.0005)).a))
        fs = float(abs(Fs_iv(P(sf), P(a0), P(b), P(1.0005)).a))
        print("b=%.3f k=%d: |F_b|=%.2f |F_R|=%.3f |F_a|=%.2f |F_s|=%.2f" % (b, k, fb, fr, fa, fs))
# Newton contraction test over cell db=1e-3 de=1e-3 at b=0.5 and b=0.99
print()
for b in (0.5, 0.99):
    s1f, s2f, _, _ = cfg(a0, b, 1.0005)
    t0 = time.time()
    s1 = cert_root_one(P(a0), I(b-5e-4, b+5e-4), I(1.0, 1.001), s1f)
    s2 = cert_root_one(P(a0), I(b-5e-4, b+5e-4), I(1.0, 1.001), s2f)
    print("b=%.2f cell(1e-3,1e-3): %s %s (%.2fs)" % (b, "OK w1=%.1e" % float(s1.b-s1.a) if s1 else "FAIL", "OK w2=%.1e" % float(s2.b-s2.a) if s2 else "FAIL", time.time()-t0))
