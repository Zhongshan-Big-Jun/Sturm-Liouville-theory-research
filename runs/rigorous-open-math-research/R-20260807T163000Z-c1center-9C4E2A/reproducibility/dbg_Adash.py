# -*- coding: utf-8 -*-
"""dbg_Adash.py - A'(b) = -R1_b/R1_a on the sheet for b -> 1."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
pi = np.pi
a0 = float(np.arccos(0.25)/pi)

def dR1da(a, b, R, h=1e-6):
    return (R1R2(a+h, b, R)[0] - R1R2(a-h, b, R)[0])/(2*h)
def dR1db(a, b, R, h=1e-6):
    return (R1R2(a, b+h, R)[0] - R1R2(a, b-h, R)[0])/(2*h)
def sheet_a(b, R, a_guess, w=0.05):
    lo, hi = a_guess-w, a_guess+w
    for _ in range(80):
        md = 0.5*(lo+hi)
        if np.signbit(R1R2(md, b, R)[0]) == np.signbit(R1R2(lo, b, R)[0]): lo = md
        else: hi = md
    return 0.5*(lo+hi)

for eps in (0.02, 0.05, 0.1):
    R = 1+eps
    print("eps=%.2f:" % eps)
    ag = a0 + eps*0.13  # guess
    for b in (0.9, 0.99, 0.999, 0.9999, 0.99999):
        a_s = sheet_a(b, R, ag, 0.05)
        ra = dR1da(a_s, b, R); rb = dR1db(a_s, b, R)
        Ad = -rb/ra
        print("   b=%.5f a=%.6f  R1_a=%.3f R1_b=%.3e  A'(b)=%.3e" % (b, a_s, ra, rb, Ad))
