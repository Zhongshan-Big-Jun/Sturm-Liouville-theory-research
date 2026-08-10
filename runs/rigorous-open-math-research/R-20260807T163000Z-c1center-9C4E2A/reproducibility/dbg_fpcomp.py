# -*- coding: utf-8 -*-
"""dbg_fpcomp.py - trace the fp-component from the fp in both b-directions; find its endpoints."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
pi = np.pi
a0 = float(np.arccos(0.25)/pi); b0 = 1-a0
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

def sheet_a_near(b, R, a_guess, w=0.02):
    lo, hi = a_guess-w, a_guess+w
    for _ in range(80):
        md = 0.5*(lo+hi)
        fm = R1R2(md, b, R)[0]
        if np.signbit(fm) == np.signbit(R1R2(lo, b, R)[0]): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def find_fp(R):
    # solve a = ? on diagonal b=1-a with R1=0
    lo, hi = 0.3, 0.5
    for _ in range(80):
        am = 0.5*(lo+hi)
        if R1R2(am, 1-am, R)[0] * R1R2(lo, 1-lo, R)[0] < 0: hi = am
        else: lo = am
    return 0.5*(lo+hi)

for eps in (0.02, 0.05, 0.1):
    R = 1+eps
    afp = find_fp(R); bfp = 1-afp
    print("=== eps=%.2f: fp=(%.6f, %.6f) ===" % (eps, afp, bfp))
    # trace upward in b from bfp: b increases
    print("  tracing b upward from bfp:")
    b_cur = bfp; a_cur = afp
    for _ in range(10):
        b_new = b_cur + 0.05
        if b_new >= 1.0: break
        try:
            a_new = sheet_a_near(b_new, R, a_cur, 0.03)
        except Exception:
            print("    break at b=%.3f" % b_cur); break
        ra = dR1da(a_new, b_new, R)
        print("    b=%.4f a=%.6f R1_a=%.2f" % (b_new, a_new, ra))
        b_cur, a_cur = b_new, a_new
    # check b=1 exactly
    for b in (0.999, 0.9999, 1.0-1e-9):
        try:
            a_s = sheet_a_near(b, R, a_cur, 0.05)
            print("    b=%.6g a=%.6f R1=%.3e" % (b, a_s, R1R2(a_s, b, R)[0]))
        except Exception as e:
            print("    b=%.6g: %s" % (b, e))
    # trace downward in b from bfp
    print("  tracing b downward from bfp:")
    b_cur = bfp; a_cur = afp
    for _ in range(10):
        b_new = b_cur - 0.05
        if b_new <= a0: break
        try:
            a_new = sheet_a_near(b_new, R, a_cur, 0.03)
        except Exception:
            print("    break at b=%.3f" % b_cur); break
        print("    b=%.4f a=%.6f" % (b_new, a_new))
        b_cur, a_cur = b_new, a_new
    # endpoint at b=a0?
    try:
        a_s = sheet_a_near(a0, R, a_cur, 0.03)
        print("    b=a0: a=%.10f (expect a0=%.10f)" % (a_s, a0))
    except Exception as e:
        print("    b=a0: %s" % e)
