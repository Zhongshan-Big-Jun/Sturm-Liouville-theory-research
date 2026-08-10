# -*- coding: utf-8 -*-
"""num_phi2.py - EVIDENCE: compute phi_2(b) and phi_2'(b) numerically at high
precision via the exact secular solver (mpmath 40 digits). Not a proof."""
import mpmath as mp
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phi_num_helper import phi_num, pi, a0
mp.mp.dps = 40
b0 = 1 - a0
s15 = mp.sqrt(15)

def sec_mp(s, a, b, eps):
    q = mp.sqrt(1+eps)
    al = s*a; be = s*(1-b); th = q*s*(b-a)
    return (mp.cos(be)*mp.cos(th)*mp.sin(al) - q*mp.sin(be)*mp.sin(th)*mp.sin(al)
            + (mp.cos(be)*mp.sin(th)/q)*mp.cos(al) + mp.sin(be)*mp.cos(th)*mp.cos(al))
def norm_mp(s, a, b, eps):
    q = mp.sqrt(1+eps); Lw = b-a; be = 1-b
    al = s*a; th = q*s*Lw
    I1 = a/2 - mp.sin(2*al)/(4*s)
    Icc = Lw/2 + mp.sin(2*th)/(4*q*s); Iss = Lw/2 - mp.sin(2*th)/(4*q*s)
    Ics = mp.sin(th)**2/(2*q*s)
    sa, ca = mp.sin(al), mp.cos(al)
    I2 = sa**2*Icc + (ca/q)**2*Iss + 2*sa*(ca/q)*Ics
    yb = sa*mp.cos(th) + (ca/q)*mp.sin(th)
    ypb = -q*mp.sin(th)*sa + mp.cos(th)*ca
    Icc3 = be/2 + mp.sin(2*s*be)/(4*s); Iss3 = be/2 - mp.sin(2*s*be)/(4*s)
    Ics3 = mp.sin(s*be)**2/(2*s)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/s**2
    return (I1 + q**2*I2)/s**2 + I3
def root_mp(k, a, b, eps):
    return mp.findroot(lambda s: sec_mp(s, a, b, eps), k*pi, tol=1e-35, maxsteps=60)
def f_at(a, b, eps):
    s1 = root_mp(1, a, b, eps); s2 = root_mp(2, a, b, eps)
    n1 = norm_mp(s1, a, b, eps); n2 = norm_mp(s2, a, b, eps)
    y1a = mp.sin(s1*a)/s1; y2a = mp.sin(s2*a)/s2
    return s1**2*y1a**2/n1 - s2**2*y2a**2/n2
def dphi_cf(b):
    u = mp.cos(2*pi*b); v = mp.sin(2*pi*b)
    N = (56*pi*a0 - 6*s15)*u**2 + (2*pi*a0 + 3*s15)*u + (3*s15 - 58*pi*a0) + 2*s15*pi*(1-b)*(1-4*u)*v
    return -N/(60*pi)
def sheet_a(b, eps):
    lo, hi = a0-mp.mpf('0.03'), a0+mp.mpf('0.03')
    flo = f_at(lo, b, eps)
    for _ in range(70):
        md = 0.5*(lo+hi)
        if (f_at(md, b, eps) > 0) == (flo > 0): lo = md
        else: hi = md
    return 0.5*(lo+hi)
def Aprime2(b, eps):
    a = sheet_a(b, eps)
    h = mp.mpf('1e-5')
    R1a = (f_at(a+h, b, eps) - f_at(a-h, b, eps))/(2*h)
    R1b = (f_at(a, b+h, eps) - f_at(a, b-h, eps))/(2*h)
    return -R1b/R1a

print("=== phi_2(b) = (A_eps - a0 - eps*phi)/eps^2 (eps-independent if O(eps^3) small) ===")
for b in (mp.mpf('0.45'), mp.mpf('0.5'), mp.mpf('0.55'), b0, mp.mpf('0.7'),
          mp.mpf('0.8'), mp.mpf('0.9'), mp.mpf('0.95'), mp.mpf('0.99')):
    vals = []
    for eps in (mp.mpf('0.005'), mp.mpf('0.02'), mp.mpf('0.05')):
        a = sheet_a(b, eps)
        err = (a - a0 - eps*phi_num(b))/eps**2
        vals.append(float(err))
    print("b=%.4f: phi_2 = [%.5f, %.5f, %.5f]" % (float(b), vals[0], vals[1], vals[2]))

print()
print("=== phi_2'(b) = (A'(b) - eps*phi'(b))/eps^2 ===")
for b in (mp.mpf('0.45'), mp.mpf('0.5'), mp.mpf('0.55'), b0, mp.mpf('0.7'),
          mp.mpf('0.8'), mp.mpf('0.9'), mp.mpf('0.95'), mp.mpf('0.99')):
    vals = []
    for eps in (mp.mpf('0.005'), mp.mpf('0.02'), mp.mpf('0.05')):
        Ap = Aprime2(b, eps)
        p2 = (Ap - eps*dphi_cf(b))/eps**2
        vals.append(float(p2))
    print("b=%.4f: phi_2' = [%.5f, %.5f, %.5f]" % (float(b), vals[0], vals[1], vals[2]))
