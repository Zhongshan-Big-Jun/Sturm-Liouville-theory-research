# -*- coding: utf-8 -*-
"""dbg_b_top_trace.py v4 - trace S3 sheet to b=1 for eps>=0.02 (skip degenerate first point)."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
a0 = float(np.arccos(0.25)/np.pi)
s15 = np.sqrt(15)
def phi(b):
    return (s15*(-1920*s15*np.pi**2*a0**2 + 1920*s15*np.pi**2*a0*b - 64*s15*np.pi*a0*np.sin(2*np.pi*b)
            - 448*s15*np.pi*a0*np.sin(4*np.pi*b) - 2700*np.pi*a0 + 1920*np.pi*b*np.cos(2*np.pi*b)**2
            - 960*np.pi*b*np.cos(2*np.pi*b) - 960*np.pi*b - 960*np.sin(2*np.pi*b) + 480*np.sin(4*np.pi*b)
            - 1920*np.pi*np.cos(2*np.pi*b)**2 + 960*np.pi*np.cos(2*np.pi*b) + 225*s15 + 2310*np.pi)
            / (57600*np.pi**2))
def solve_a(b, eps, a_guess):
    a = a_guess
    for _ in range(200):
        fa = R1R2(a, b, 1+eps)[0]
        if abs(fa) < 1e-12: break
        h = 1e-6
        d = (R1R2(a+h, b, 1+eps)[0]-R1R2(a-h, b, 1+eps)[0])/(2*h)
        if abs(d) < 1e-10: break
        an = a - fa/d
        if not (0 < an < b): break
        if abs(R1R2(an, b, 1+eps)[0]) > abs(fa): break
        a = an
    return a, R1R2(a, b, 1+eps)[0]

for eps in (0.02, 0.05, 0.1):
    last = None; ok_cnt = 0; a_guess = a0
    bs = np.linspace(a0, 1.0, 1001)[1:]
    for b in bs:
        a, r = solve_a(b, eps, a0 + eps*phi(b))
        if abs(r) < 1e-6 and 0 < a < b:
            last = (b, a, r); ok_cnt += 1; a_guess = a
        else:
            break
    print("eps=%.2f: branch reaches b=%.6f (ok_cnt=%d), a=%.10f residual=%.2e" %
          (eps, last[0], ok_cnt, last[1], last[2]))
    a1, r1 = solve_a(1.0, eps, a0 + eps*phi(1.0))
    print("        b=1: a=%.10f residual=%.2e  (pred a0+eps*phi(1)=%.6f)" % (a1, r1, a0+eps*phi(1.0)))
