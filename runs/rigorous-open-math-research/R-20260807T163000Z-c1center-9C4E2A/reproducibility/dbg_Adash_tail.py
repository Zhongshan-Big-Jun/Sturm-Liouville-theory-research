# -*- coding: utf-8 -*-
"""dbg_Adash_tail.py - A'(b) near b=1 at several eps (EVIDENCE)."""
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
    for _ in range(120):
        fa = R1R2(a, b, 1+eps)[0]
        if abs(fa) < 1e-13: break
        h = 1e-6
        d = (R1R2(a+h, b, 1+eps)[0]-R1R2(a-h, b, 1+eps)[0])/(2*h)
        if abs(d) < 1e-9: break
        an = a - fa/d
        if not (0 < an < b): break
        a = an
    return a
for eps in (0.02, 0.05, 0.1):
    a_prev = a0 + eps*phi(0.995)
    row = []
    for b in np.linspace(0.96, 1.0, 21):
        a = solve_a(b, eps, a_prev)
        db = 1e-5
        ap = solve_a(min(b+db, 1.0), eps, a); am = solve_a(b-db, eps, a)
        Ap = (ap - am)/(2*db)
        row.append((b, a, Ap))
        a_prev = a
    print("eps=%.2f:" % eps)
    for (b, a, Ap) in row[::2]:
        print("   b=%.4f  a=%.8f  A'(b)=%+.3e" % (b, a, Ap))
