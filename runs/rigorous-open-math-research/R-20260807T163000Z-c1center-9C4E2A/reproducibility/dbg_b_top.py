# -*- coding: utf-8 -*-
"""dbg_b_top.py - trace the sheet a = A(b,eps) near its end b_top; inspect R1_a, R1_b."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2, cfg, y_at
pi = np.pi
a0 = float(np.arccos(0.25)/pi)
s15 = np.sqrt(15)

def phi_cf(bv):
    fc = 15*np.pi**3*s15/4
    R1_1 = np.pi*(1920*s15*np.pi**2*a0**2 - 1920*s15*np.pi**2*a0*bv + 64*s15*np.pi*a0*np.sin(2*np.pi*bv)
               + 448*s15*np.pi*a0*np.sin(4*np.pi*bv) + 2700*np.pi*a0 - 1920*np.pi*bv*np.cos(2*np.pi*bv)**2
               + 960*np.pi*bv*np.cos(2*np.pi*bv) + 960*np.pi*bv + 960*np.sin(2*np.pi*bv) - 480*np.sin(4*np.pi*bv)
               + 1920*np.pi*np.cos(2*np.pi*bv)**2 - 960*np.pi*np.cos(2*np.pi*bv) - 2310*np.pi - 225*s15)/1024
    return -R1_1/fc

def dR1da(a, b, R, h=1e-6):
    return (R1R2(a+h, b, R)[0] - R1R2(a-h, b, R)[0])/(2*h)
def dR1db(a, b, R, h=1e-6):
    return (R1R2(a, b+h, R)[0] - R1R2(a, b-h, R)[0])/(2*h)

def sheet_a(b, R, lo, hi):
    flo = R1R2(lo, b, R)[0]; fhi = R1R2(hi, b, R)[0]
    for _ in range(70):
        md = 0.5*(lo+hi)
        fm = R1R2(md, b, R)[0]
        if np.signbit(fm) == np.signbit(flo): lo, flo = md, fm
        else: hi = md
    return 0.5*(lo+hi)

for eps in (0.02, 0.05, 0.1):
    R = 1+eps
    print("=== eps =", eps, "===")
    # scan b from a0 to 0.98, look for where the sheet root near a0 disappears
    last = None
    for b in np.linspace(a0+0.02, 0.985, 40):
        # find root of R1(a,b,R) near a0+eps*phi(b): scan bracket [a0-0.05, a0+0.05]
        lo, hi = a0-0.05, a0+0.05
        vals = [R1R2(a, b, R)[0] for a in np.linspace(lo, hi, 401)]
        signs = np.signbit(np.array(vals))
        idx = np.nonzero(signs[1:] != signs[:-1])[0]
        if len(idx) == 1:
            a_s = sheet_a(b, R, lo + idx[0]*(hi-lo)/400, lo + (idx[0]+1)*(hi-lo)/400)
            ra = dR1da(a_s, b, R); rb = dR1db(a_s, b, R)
            last = (b, a_s, ra, rb)
        else:
            print("  b=%.3f: %d roots in a-bracket" % (b, len(idx)))
    if last:
        b, a_s, ra, rb = last
        print("  last sheet point found: b=%.4f a=%.6f  R1_a=%.4f R1_b=%.4f  G=db/da=%.4f"
              % (b, a_s, ra, rb, -ra/rb))
    # also probe b=0.99, 0.999
    for b in (0.99, 0.999, 0.9999):
        lo, hi = a0-0.05, a0+0.05
        vals = [R1R2(a, b, R)[0] for a in np.linspace(lo, hi, 401)]
        signs = np.signbit(np.array(vals))
        idx = np.nonzero(signs[1:] != signs[:-1])[0]
        print("  b=%.4f: %d roots in a-bracket [a0-0.05,a0+0.05]" % (b, len(idx)))
