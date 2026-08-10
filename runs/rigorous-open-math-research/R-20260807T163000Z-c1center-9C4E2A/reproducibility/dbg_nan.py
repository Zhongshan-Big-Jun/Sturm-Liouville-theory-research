# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_lib import F_iv
from fast_lib import cfg
def P(x): return iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))
def I(lo, hi): return iv.mpf((mp.mpf(float(lo)), mp.mpf(float(hi))))
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
b = 0.6
s1f, s2f, _, _ = cfg(a0, b, 1.0005)
sm = P(s1f)
# test each sub-box of the big box separately
tests = [
    ("a-ball", I(a0-0.03, a0+0.03), P(b), P(1.0005)),
    ("b-cell", P(a0), I(b-0.01, b+0.01), P(1.0005)),
    ("R-cell", P(a0), P(b), I(1.0, 1.001)),
    ("a-ball x b-cell", I(a0-0.03, a0+0.03), I(b-0.01, b+0.01), P(1.0005)),
    ("full", I(a0-0.03, a0+0.03), I(b-0.01, b+0.01), I(1.0, 1.001)),
]
for name, ai, bi, Ri in tests:
    try:
        v = F_iv(sm, ai, bi, Ri)
        print("%-16s: [%s, %s]" % (name, mp.nstr(v.a, 6), mp.nstr(v.b, 6)))
    except Exception as e:
        print("%-16s: EXC %s" % (name, e))
