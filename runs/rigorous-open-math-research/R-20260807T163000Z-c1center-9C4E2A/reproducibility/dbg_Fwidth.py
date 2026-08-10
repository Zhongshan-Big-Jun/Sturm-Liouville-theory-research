# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_lib import F_iv, Fs_iv, Fa_iv, Fb_iv
from fast_lib import cfg

def P(x): return iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))
def I(lo, hi): return iv.mpf((mp.mpf(float(lo)), mp.mpf(float(hi))))
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
b = 0.6
s1f, s2f, _, _ = cfg(a0, b, 1.0005)
# F(sm) width decomposition over the big box
sm = P(s1f)
a_iv = I(a0-0.03, a0+0.03); b_iv = I(b-0.01, b+0.01); R_iv = I(1.0, 1.001)
Ffull = F_iv(sm, a_iv, b_iv, R_iv)
Fa_only = F_iv(sm, a_iv, P(b), P(1.0005))
Fb_only = F_iv(sm, P(a0), b_iv, P(1.0005))
FR_only = F_iv(sm, P(a0), P(b), R_iv)
print("F(sm) full box : [%.6f, %.6f] width %.3e" % (float(Ffull.a), float(Ffull.b), float(Ffull.b-Ffull.a)))
print("F(sm) a-only   : [%.6f, %.6f] width %.3e" % (float(Fa_only.a), float(Fa_only.b), float(Fa_only.b-Fa_only.a)))
print("F(sm) b-only   : [%.6f, %.6f] width %.3e" % (float(Fb_only.a), float(Fb_only.b), float(Fb_only.b-Fb_only.a)))
print("F(sm) R-only   : [%.6f, %.6f] width %.3e" % (float(FR_only.a), float(FR_only.b), float(FR_only.b-FR_only.a)))
# measure F_R directly
for bb in (0.45, 0.6, 0.8, 0.99):
    s1f2, _, _, _ = cfg(a0, bb, 1.0005)
    fr = float(F_iv(P(s1f2), P(a0), P(bb), I(1.0, 1.001)).b - F_iv(P(s1f2), P(a0), P(bb), I(1.0, 1.001)).a)/0.001
    print("b=%.2f: |F_R| ~ %.1f" % (bb, fr))
