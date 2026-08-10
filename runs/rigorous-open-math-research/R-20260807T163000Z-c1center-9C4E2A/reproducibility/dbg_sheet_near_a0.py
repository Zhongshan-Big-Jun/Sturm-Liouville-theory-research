# -*- coding: utf-8 -*-
"""dbg_sheet_near_a0.py - sheet A(b,eps) near b=a0: sign of A(b)-a0, slope."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
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
def dphi_cf(bv):
    u = np.cos(2*np.pi*bv); v = np.sin(2*np.pi*bv)
    N = (56*np.pi*a0 - 6*s15)*u**2 + (2*np.pi*a0 + 3*s15)*u + (3*s15 - 58*np.pi*a0) + 2*s15*np.pi*(1-bv)*(1-4*u)*v
    return -N/(60*np.pi)

def sheet(b, R, w=0.01):
    lo, hi = a0-w, a0+w
    flo = R1R2(lo, b, R)[0]
    for _ in range(80):
        md = 0.5*(lo+hi)
        if np.signbit(R1R2(md, b, R)[0]) == np.signbit(flo): lo = md
        else: hi = md
    return 0.5*(lo+hi)

print("phi'(a0) = %.8f" % dphi_cf(a0))
for eps in (1e-2, 1e-3, 1e-4, 1e-5):
    R = 1+eps
    print("eps=%.0e:" % eps)
    for db in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
        b = a0 + db
        a_s = sheet(b, R)
        pred = a0 + eps*phi_cf(b)
        print("   db=%.0e: A-a0=%.3e  eps*phi=%.3e  A-a0-eps*phi=%.3e"
              % (db, a_s-a0, eps*phi_cf(b), a_s-pred))
