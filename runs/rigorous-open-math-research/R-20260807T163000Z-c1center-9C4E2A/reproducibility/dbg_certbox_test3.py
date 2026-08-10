# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_lib import F_iv, Fs_iv
from fast_lib import cfg, sec
import numpy as np

def P(x): return iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))
def I(lo, hi): return iv.mpf((mp.mpf(float(lo)), mp.mpf(float(hi))))

def cert_root_one(a_iv, b_iv, R_iv, sg, w=2e-3, iters=12, wmin=1e-14):
    """interval Newton: s_{k+1} = N(s_k) intersect s_k, N(s)=s_mid-F(s_mid)/F_s(s)."""
    s = I(sg - w, sg + w)
    for _ in range(iters):
        sm = P(0.5*(float(s.a)+float(s.b)))
        Fs = Fs_iv(s, a_iv, b_iv, R_iv)
        if Fs.a > 0 or Fs.b < 0:
            N = sm - F_iv(sm, a_iv, b_iv, R_iv) / Fs
            s_new = iv.intersection(N, s) if hasattr(iv, 'intersection') else None
            # manual intersection
            lo = max(s.a, N.a); hi = min(s.b, N.b)
            if lo <= hi:
                s = I(float(lo), float(hi))
            else:
                return None
            if float(s.b - s.a) < wmin:
                return s
        else:
            return None
    return s if (float(s.b-s.a) < 5e-3) else None

a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
# eps box only
for (db, de) in [(1e-3, 1e-3), (1e-2, 1e-3)]:
    b0c = 0.5
    # float root at center
    s1f, s2f, _, _ = cfg(a0, b0c, 1.0 + de/2)
    t0 = time.time()
    s1 = cert_root_one(P(a0), I(b0c-db/2, b0c+db/2), I(1.0, 1.0+de), s1f)
    s2 = cert_root_one(P(a0), I(b0c-db/2, b0c+db/2), I(1.0, 1.0+de), s2f)
    dt = time.time()-t0
    if s1 and s2:
        print("db=%.0e de=%.0e: OK (%.2fs) w1=%.1e w2=%.1e" % (db, de, dt, float(s1.b-s1.a), float(s2.b-s2.a)))
    else:
        print("db=%.0e de=%.0e: FAIL (%.2fs)" % (db, de, dt))
