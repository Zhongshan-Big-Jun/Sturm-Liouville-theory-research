# -*- coding: utf-8 -*-
"""verify_sheet_exact.py - independent check of the sheet a*(b,eps) ~ a0 + eps*phi(b)
using the EXACT secular solver (fast_lib.R1R2).  EVIDENCE only."""
import numpy as np, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
pi = np.pi
a0 = float(np.arccos(0.25)/pi)
s15 = np.sqrt(15)
# closed form phi(b) (verified derivation)
def phi_cf(b):
    al = pi*a0
    m = 56*al - 6*s15
    n = 2*al + 3*s15
    u = np.cos(2*pi*b); v = np.sin(2*pi*b)
    # phi = -R1_1/fc; use the closed form expression from sym_phi_closedform3
    # phi(b) = sqrt(15)*(...)/(57600 pi^2); simpler: reconstruct from phi' formula? 
    # Use the exact closed form from sym_phi_closedform3 output:
    fc = 15*pi**3*s15/4
    R1_1 = pi*(1920*s15*pi**2*a0**2 - 1920*s15*pi**2*a0*b + 64*s15*pi*a0*np.sin(2*pi*b)
               + 448*s15*pi*a0*np.sin(4*pi*b) + 2700*pi*a0 - 1920*pi*b*np.cos(2*pi*b)**2
               + 960*pi*b*np.cos(2*pi*b) + 960*pi*b + 960*np.sin(2*pi*b) - 480*np.sin(4*pi*b)
               + 1920*pi*np.cos(2*pi*b)**2 - 960*pi*np.cos(2*pi*b) - 2310*pi - 225*s15)/1024
    return -R1_1/fc

def dphi_cf(b):
    u = np.cos(2*pi*b); v = np.sin(2*pi*b)
    N = (56*pi*a0 - 6*s15)*u**2 + (2*pi*a0 + 3*s15)*u + (3*s15 - 58*pi*a0) + 2*s15*pi*(1-b)*(1-4*u)*v
    return -N/(60*pi)

def find_sheet_a(b, eps, R):
    # solve R1(a,b,R)=0 for a in [a0-0.02, a0+0.02]
    lo, hi = a0-0.02, a0+0.02
    flo = R1R2(lo, b, R)[0]; fhi = R1R2(hi, b, R)[0]
    # R1 as function of a: sign change?
    for _ in range(60):
        md = 0.5*(lo+hi)
        fm = R1R2(md, b, R)[0]
        if np.signbit(fm) == np.signbit(flo): lo, flo = md, fm
        else: hi = md
    return 0.5*(lo+hi)

rows = []
for eps in (1e-3, 1e-4):
    R = 1 + eps
    print("=== eps = %.0e (R=%g) ===" % (eps, R))
    for b in (0.45, 0.5, 0.6, 0.7, 0.8, 0.9):
        astar = find_sheet_a(b, eps, R)
        ph = phi_cf(b)
        pred = a0 + eps*ph
        rows.append(dict(eps=eps, b=b, astar=astar, a0_eps_phi=pred, diff=astar-pred, phi=ph))
        print("  b=%.2f: a* = %.10f  a0+eps*phi = %.10f  diff = %.3e  phi=%.6f"
              % (b, astar, pred, astar-pred, ph))
# phi' check via finite differences of the exact sheet
print()
print("phi' closed form vs FD of the sheet (eps=1e-4):")
bs = np.linspace(0.45, 0.9, 20)
hh = 1e-5
for b in (0.5, 0.7, 0.9):
    astar_p = find_sheet_a(b+hh, 1e-4, 1.0001)
    astar_m = find_sheet_a(b-hh, 1e-4, 1.0001)
    fd = (astar_p - astar_m)/(2*hh)/1e-4
    print("  b=%.2f: FD phi' = %.6f  closed = %.6f" % (b, fd, dphi_cf(b)))
here = os.path.dirname(os.path.abspath(__file__))
json.dump(rows, open(os.path.join(here, "verify_sheet_exact.json"), "w"), indent=1)
