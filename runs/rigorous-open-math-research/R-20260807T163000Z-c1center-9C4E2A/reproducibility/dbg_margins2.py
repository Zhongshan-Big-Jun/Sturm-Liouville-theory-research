# -*- coding: utf-8 -*-
"""dbg_margins2.py - EVIDENCE: E1-right/P0/U' margins for R->1+, fast version."""
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

def sheet_a_fast(b, eps, center=None):
    c = a0 + eps*phi(b) if center is None else center
    lo, hi = c-0.025, c+0.025
    flo = R1R2(lo, b, 1+eps)[0]
    for _ in range(60):
        md = 0.5*(lo+hi)
        if np.signbit(R1R2(md, b, 1+eps)[0]) == np.signbit(flo): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def dR1da(a, b, R, h=1e-6):
    return (R1R2(a+h, b, R)[0] - R1R2(a-h, b, R)[0])/(2*h)
def dR1db(a, b, R, h=1e-6):
    return (R1R2(a, b+h, R)[0] - R1R2(a, b-h, R)[0])/(2*h)

# --- E1-right ---
print("=== E1-right: b_top, a_max1, h(beta) ===")
for eps in (1e-3, 1e-2, 0.02, 0.05, 0.1):
    b = a0; a = a0; last_b = a0
    for _ in range(400):
        bn = b + 0.005
        if bn >= 1.0: break
        an = sheet_a_fast(bn, eps, center=a + eps*0.01)
        if not (a0-0.05 < an < bn) or abs(an-a) > 0.05: break
        b = bn; a = an
        last_b = b
        if b > 0.995: break
    b_top = last_b
    a_max1 = sheet_a_fast(b_top, eps)
    beta = min(a_max1, b0)
    if beta == a_max1:
        h_beta = b_top - 1 + sheet_a_fast(1 - a_max1, eps)
    else:
        h_beta = sheet_a_fast(b0, eps) - 1 + a0
    print("  eps=%.3f: b_top=%.6f  a_max1=%.6f  h(beta)=%.6f" % (eps, b_top, a_max1, h_beta))

# --- P0 ---
print("=== P0: A'(b) = -R1_b/R1_a, min over b in [a0, 0.99] ===")
for eps in (1e-3, 1e-2, 0.02, 0.05):
    amin_Ap = 1e9; aloc = None
    for b in np.linspace(a0, 0.99, 120):
        a = sheet_a_fast(b, eps)
        Ap = -dR1db(a, b, 1+eps)/dR1da(a, b, 1+eps)
        if Ap < amin_Ap: amin_Ap = Ap; aloc = b
    print("  eps=%.3f: min A'(b)=%.6e at b=%.4f" % (eps, amin_Ap, aloc))

# --- U' ---
print("=== U': Phi-1 = 1/(A'(b)*A'(1-A(b))) - 1 ===")
for eps in (1e-3, 1e-2, 0.05):
    vals = []
    for a in np.linspace(a0, min(a0+eps*phi(0.99), b0-1e-9), 40):
        lo, hi = a0, 0.99
        for _ in range(60):
            md = 0.5*(lo+hi)
            if sheet_a_fast(md, eps) < a: lo = md
            else: hi = md
        b = 0.5*(lo+hi)
        ap = sheet_a_fast(b, eps)
        Ap = -dR1db(ap, b, 1+eps)/dR1da(ap, b, 1+eps)
        b2 = 1 - a
        a2 = sheet_a_fast(b2, eps)
        Ap2 = -dR1db(a2, b2, 1+eps)/dR1da(a2, b2, 1+eps)
        vals.append((a, Ap*Ap2 - 1))
    mn = min(v[1] for v in vals)
    print("  eps=%.3f: min(Phi-1)=%.6e" % (eps, mn))
