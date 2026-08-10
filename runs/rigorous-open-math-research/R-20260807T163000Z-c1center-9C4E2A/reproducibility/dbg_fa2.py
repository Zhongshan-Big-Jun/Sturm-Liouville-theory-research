# -*- coding: utf-8 -*-
import mpmath as mp
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import cfg, sec
mp.mp.dps = 30
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
b = 0.6; R = 1.0005
s1f, s2f, _, _ = cfg(a0, b, R)
print("s1f = %.10f" % s1f)
for a in (a0-0.03, a0-0.015, a0, a0+0.015, a0+0.03):
    print("  F(s1f; a=%.4f) = %.8f" % (a, sec(s1f, a, b, R)))
# F_a at (s1f, a0) via FD
h = 1e-6
fa = (sec(s1f, a0+h, b, R) - sec(s1f, a0-h, b, R))/(2*h)
print("F_a(s1f; a0) FD = %.6f" % fa)
