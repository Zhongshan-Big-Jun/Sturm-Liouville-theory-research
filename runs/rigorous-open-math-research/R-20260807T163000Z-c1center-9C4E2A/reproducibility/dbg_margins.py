# -*- coding: utf-8 -*-
"""dbg_margins.py - EVIDENCE: quantify E1/P0/U' margins for R->1+ on b in [a0,0.99].
Uses exact secular solver (fast_lib) + high-precision mpmath FD. Not a proof."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
pi = np.pi
a0 = float(np.arccos(0.25)/pi)
b0 = 1 - a0
s15 = np.sqrt(15)

def phi(b):
    fc = 15*pi**3*s15/4
    R1_1 = pi*(1920*s15*pi**2*a0**2 - 1920*s15*pi**2*a0*b + 64*s15*pi*a0*np.sin(2*pi*b)
               + 448*s15*pi*a0*np.sin(4*pi*b) + 2700*pi*a0 - 1920*pi*b*np.cos(2*pi*b)**2
               + 960*pi*b*np.cos(2*pi*b) + 960*pi*b + 960*np.sin(2*pi*b) - 480*np.sin(4*pi*b)
               + 1920*pi*np.cos(2*pi*b)**2 - 960*pi*np.cos(2*pi*b) - 2310*pi - 225*s15)/1024
    return -R1_1/fc

def dphi(b):
    u = np.cos(2*pi*b); v = np.sin(2*pi*b)
    N = (56*pi*a0 - 6*s15)*u**2 + (2*pi*a0 + 3*s15)*u + (3*s15 - 58*pi*a0) + 2*s15*pi*(1-b)*(1-4*u)*v
    return -N/(60*pi)

def sheet_a(b, eps):
    lo, hi = a0-0.03, a0+0.03
    for _ in range(90):
        md = 0.5*(lo+hi)
        if np.signbit(R1R2(md, b, 1+eps)[0]) == np.signbit(R1R2(lo, b, 1+eps)[0]): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def dR1da(a, b, R, h=1e-6):
    return (R1R2(a+h, b, R)[0] - R1R2(a-h, b, R)[0])/(2*h)
def dR1db(a, b, R, h=1e-6):
    return (R1R2(a, b+h, R)[0] - R1R2(a, b-h, R)[0])/(2*h)

# --- sheet error: A_eps(b) - a0 - eps*phi(b) over b grid, few eps ---
print("=== sheet error / eps^2 (C_sheet evidence) ===")
for eps in (1e-3, 1e-2, 0.05, 0.1):
    errmax = 0.0; errmin = 1e9; bmin = None
    for b in np.linspace(a0, 0.99, 200):
        a = sheet_a(b, eps)
        err = (a - a0 - eps*phi(b))/eps**2
        errmax = max(errmax, abs(err)); errmin = min(errmin, err)
        if abs(err) > 0.9*errmax: bmin = b
    print("  eps=%.1e: max|err|/eps^2 = %.6f  (at b~%.3f), min err/eps^2 = %.6f" % (eps, errmax, bmin, errmin))

# --- A_eps(b0), h(a0) ---
print("=== E1-left: h(a0) = A_eps(b0) - b0 ===")
for eps in (1e-3, 1e-2, 0.02, 0.05):
    a = sheet_a(b0, eps)
    h0 = a - b0
    print("  eps=%.3f: A(b0)=%.8f  h(a0)=%.6f  (2a0-1+eps*phi(b0)=%.6f, second-order resid=%.5f)"
          % (eps, a, h0, 2*a0-1+eps*phi(b0), (h0-(2*a0-1)-eps*phi(b0))/eps**2))

# --- E1-right: a_max1, b_top, h(beta) ---
print("=== E1-right: b_top, a_max1, h(beta) ===")
for eps in (1e-3, 1e-2, 0.02, 0.05, 0.1):
    # follow the sheet upward from b=a0 (a=a0) increasing b; stop when root disappears
    b = a0; a = a0
    step = 0.01; last_good = b
    for it in range(5000):
        bn = b + step
        if bn >= 1.0: break
        an = sheet_a(bn, eps)
        if not (a0-0.05 < an < bn): break
        # check continuity: jump detection
        if abs(an - a) > 0.3: break
        b = bn; a = an
        if abs(R1R2(an, bn, 1+eps)[0]) > 1e-6: break
        last_good = b
        if b > 0.99: break
    b_top = last_good
    a_max1 = sheet_a(b_top, eps)
    u_beta = sheet_a(1 - a_max1, eps) if (1 - a_max1) >= a0-1e-12 else np.nan
    # h(beta) with beta = min(a_max1, b0)
    beta = min(a_max1, b0)
    if beta == a_max1:
        h_beta = b_top - 1 + sheet_a(1 - a_max1, eps)
    else:
        h_beta = sheet_a(b0) - 1 + a0  # u(b0)=a0
    print("  eps=%.3f: b_top=%.6f  a_max1=%.6f  h(beta)=%.6f  (b_top-1+a0=%.6f)" % (eps, b_top, a_max1, h_beta, b_top-1+a0))

# --- P0: A'(b) = -R1_b/R1_a on the sheet; margins ---
print("=== P0: A'(b) = -R1_b/R1_a on sheet, min over b in [a0,0.99] ===")
for eps in (1e-3, 1e-2, 0.02, 0.05):
    amin_Ap = 1e9; aloc = None
    for b in np.linspace(a0, 0.99, 200):
        a = sheet_a(b, eps)
        ra = dR1da(a, b, 1+eps); rb = dR1db(a, b, 1+eps)
        Ap = -rb/ra
        if Ap < amin_Ap: amin_Ap = Ap; aloc = b
    print("  eps=%.3f: min A'(b)=%.6e at b=%.4f   (eps*c_phi_099=%.3e)" % (eps, amin_Ap, aloc, eps*9.576e-4))

# --- U': Phi-1 = 1/(A'(b)*A'(1-A(b))) - 1 ---
print("=== U': Phi-1 on a-grid via b = g1(a) ===")
for eps in (1e-3, 1e-2, 0.05):
    vals = []
    for a in np.linspace(a0, min(sheet_a(0.99, eps), b0), 60):
        b = None
        # invert: b = g1(a) means sheet_a(b) = a; bisect on b
        lo, hi = a0, 0.99
        for _ in range(80):
            md = 0.5*(lo+hi)
            if sheet_a(md, eps) < a: lo = md
            else: hi = md
        b = 0.5*(lo+hi)
        ra = dR1da(sheet_a(b, eps), b, 1+eps); rb = dR1db(sheet_a(b, eps), b, 1+eps)
        Ap = -rb/ra
        b2 = 1 - a
        a2 = sheet_a(b2, eps) if b2 >= a0-1e-12 else np.nan
        ra2 = dR1da(a2, b2, 1+eps); rb2 = dR1db(a2, b2, 1+eps)
        Ap2 = -rb2/ra2
        vals.append((a, Ap*Ap2 - 1))
    mn = min(v[1] for v in vals)
    print("  eps=%.3f: min(Phi-1)=%.6e" % (eps, mn))
