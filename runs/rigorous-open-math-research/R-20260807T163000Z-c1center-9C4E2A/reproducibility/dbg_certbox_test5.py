# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_lib import F_iv, Fs_iv
from fast_lib import cfg
import numpy as np

def P(x): return iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))
def I(lo, hi): return iv.mpf((mp.mpf(float(lo)), mp.mpf(float(hi))))

def cert_root_one(a_iv, b_iv, R_iv, sg, w=0.02, iters=20, wmin=1e-12):
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
# big box: a-ball full [a0-0.03,a0+0.03], b-cell 0.02, eps-cell [0,1e-3]
for b in (0.45, 0.6, 0.8, 0.99):
    s1f, s2f, _, _ = cfg(a0, b, 1.0005)
    t0 = time.time()
    s1 = cert_root_one(I(a0-0.03, a0+0.03), I(b-0.01, b+0.01), I(1.0, 1.001), s1f)
    s2 = cert_root_one(I(a0-0.03, a0+0.03), I(b-0.01, b+0.01), I(1.0, 1.001), s2f)
    dt = time.time()-t0
    if s1 and s2:
        print("b=%.2f bigbox: OK (%.2fs) w1=%.1e w2=%.1e" % (b, dt, float(s1.b-s1.a), float(s2.b-s2.a)))
    else:
        print("b=%.2f bigbox: FAIL (%.2fs) s1=%s s2=%s" % (b, dt, s1, s2))
