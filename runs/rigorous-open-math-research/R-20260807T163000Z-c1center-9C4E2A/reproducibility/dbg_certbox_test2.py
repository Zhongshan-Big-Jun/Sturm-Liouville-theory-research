# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_c1 import cert_roots, I, P
from fast_lib import cfg, R1R2

a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
# point test
for (aa, bb, RR) in [(a0, 0.5, 1.0), (a0, 0.5, 1.001), (a0, 0.9, 1.001)]:
    r = cert_roots(P(aa), P(bb), P(RR), 3.141592653589793, 6.283185307179586)
    print("point (a0,%.2f,%.4f):" % (bb, RR), "OK" if r else "FAIL")
    if r:
        s1, s2 = r
        print("   s1=%.10f..%.10f  s2=%.10f..%.10f" % (float(s1.a), float(s1.b), float(s2.a), float(s2.b)))
# box with eps only
t0 = time.time()
r = cert_roots(P(a0), P(0.5), I(1.0, 1.001), 3.141592653589793, 6.283185307179586)
print("eps-box [1,1.001] at point b: ", "OK" if r else "FAIL", "(%.2fs)" % (time.time()-t0))
t0 = time.time()
r = cert_roots(P(a0), I(0.5,0.501), P(1.001), 3.141592653589793, 6.283185307179586)
print("b-box [0.5,0.501] at point eps: ", "OK" if r else "FAIL", "(%.2fs)" % (time.time()-t0))
