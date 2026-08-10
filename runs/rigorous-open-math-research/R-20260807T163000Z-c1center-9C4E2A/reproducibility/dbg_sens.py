# -*- coding: utf-8 -*-
import mpmath as mp
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import cfg, norm_n, sec, y_at
mp.mp.dps = 30
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
R = 1.001

def R1_expr(s1, s2, a, b, R):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return np.sin(s1*a)**2/n1 - np.sin(s2*a)**2/n2

for b in (0.5, 0.7, 0.9, 0.99):
    s1f, s2f, n1, n2 = cfg(a0, b, R)
    h = 1e-5
    # dR1/ds1 (fixed s2, a, b)
    dR1ds1 = (R1_expr(s1f+h, s2f, a0, b, R) - R1_expr(s1f-h, s2f, a0, b, R))/(2*h)
    # dR1_b/ds1: R1_b via finite diff in b, then diff in s1
    R1b = lambda s1: (R1_expr(s1, s2f, a0, b+h, R) - R1_expr(s1, s2f, a0, b-h, R))/(2*h)
    dR1bds1 = (R1b(s1f+h) - R1b(s1f-h))/(2*h)
    # dR1_a/ds1
    R1a = lambda s1: (R1_expr(s1, s2f, a0+h, b, R) - R1_expr(s1, s2f, a0-h, b, R))/(2*h)
    dR1ads1 = (R1a(s1f+h) - R1a(s1f-h))/(2*h)
    # actual R1_b, R1_a values
    r1b = (R1_expr(s1f, s2f, a0, b+h, R) - R1_expr(s1f, s2f, a0, b-h, R))/(2*h)
    r1a = (R1_expr(s1f, s2f, a0+h, b, R) - R1_expr(s1f, s2f, a0-h, b, R))/(2*h)
    print("b=%.2f: R1_a=%.2f R1_b=%.2e  dR1_a/ds1=%.2f dR1_b/ds1=%.2f dR1/ds1=%.2f"
          % (b, r1a, r1b, dR1ads1, dR1bds1, dR1ds1))
