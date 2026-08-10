# -*- coding: utf-8 -*-
"""verify_phi2_exact.py (v2) - numeric 2nd-order sheet via mpmath on the exact formulas.
Computes R1_1(a0,b), R1_2(a0,b), phi(b), phi2(b); checks the exact-solver residual
R1(a0 + eps*phi + eps^2*phi2, b, 1+eps) = O(eps^3).  EVIDENCE only."""
import mpmath as mp
import numpy as np, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2

mp.mp.dps = 60
pi = mp.pi
a0n = float(mp.acos(mp.mpf(1)/4)/pi)

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
    s0 = k*pi
    f = lambda s: sec_mp(s, a, b, eps)
    return mp.findroot(f, s0, tol=1e-50, maxsteps=80)

def f_at(a, b, eps):
    s1 = root_mp(1, a, b, eps); s2 = root_mp(2, a, b, eps)
    n1 = norm_mp(s1, a, b, eps); n2 = norm_mp(s2, a, b, eps)
    y1a = mp.sin(s1*a)/s1; y2a = mp.sin(s2*a)/s2
    return s1**2*y1a**2/n1 - s2**2*y2a**2/n2

def dcoef(fun, x0, order):
    # Taylor coefficient [f^(order)(x0)/order!] via mpmath diff (Richardson)
    return mp.diff(fun, x0, order) / mp.factorial(order)

fconst = lambda x: 2*pi**2*(mp.sin(pi*x)**2 - 4*mp.sin(2*pi*x)**2)
fca0 = float(mp.diff(fconst, a0n, 1))
fcpa0 = float(mp.diff(fconst, a0n, 2))
print("f_const'(a0) = %.10f (expect 15 pi^3 sqrt15/4 = %.10f)" % (fca0, float(15*pi**3*mp.sqrt(15)/4)))
print("f_const''(a0) = %.10f" % fcpa0)

def R1_1(a, b): return float(dcoef(lambda e: f_at(a, b, e), 0, 1))
def R1_2(a, b): return float(dcoef(lambda e: f_at(a, b, e), 0, 2))

bs = [0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9]
rows = []
for bn in bs:
    bm = mp.mpf(bn)
    r11 = R1_1(a0n, bn); r12 = R1_2(a0n, bn)
    phi = -r11/fca0
    h = mp.mpf('1e-5')
    dR = float((R1_1(a0n+float(h), bn) - R1_1(a0n-float(h), bn))/(2*float(h)))
    phi2 = -(0.5*fcpa0*phi**2 + dR*phi + r12)/fca0
    rows.append(dict(b=bn, R1_1=r11, R1_2=r12, phi=phi, dR1_1a=dR, phi2=phi2))
    print("b=%.2f  R1_1=%.8f  R1_2=%.5f  phi=%.8f  phi2=%.5f  dR1_1a=%.5f"
          % (bn, r11, r12, phi, phi2, dR), flush=True)

# phi vs known closed form
s15 = np.sqrt(15)
def phi_cf(bv):
    fc = 15*np.pi**3*s15/4
    R1_1 = np.pi*(1920*s15*np.pi**2*a0n**2 - 1920*s15*np.pi**2*a0n*bv + 64*s15*np.pi*a0n*np.sin(2*np.pi*bv)
               + 448*s15*np.pi*a0n*np.sin(4*np.pi*bv) + 2700*np.pi*a0n - 1920*np.pi*bv*np.cos(2*np.pi*bv)**2
               + 960*np.pi*bv*np.cos(2*np.pi*bv) + 960*np.pi*bv + 960*np.sin(2*np.pi*bv) - 480*np.sin(4*np.pi*bv)
               + 1920*np.pi*np.cos(2*np.pi*bv)**2 - 960*np.pi*np.cos(2*np.pi*bv) - 2310*np.pi - 225*s15)/1024
    return -R1_1/fc
print()
print("phi vs closed form:")
for r in rows:
    print("  b=%.2f  new=%.8f  cf=%.8f  diff=%.2e" % (r["b"], r["phi"], phi_cf(r["b"]), abs(r["phi"]-phi_cf(r["b"]))))

print()
print("exact-solver residual of 2nd-order sheet  R1/eps^3 (should be O(1) constant):")
for eps in (1e-2, 1e-3, 1e-4, 1e-5):
    line = "  eps=%.0e:" % eps
    for r in rows:
        an = a0n + eps*r["phi"] + eps**2*r["phi2"]
        R1v = R1R2(an, r["b"], 1+eps)[0]
        line += " b=%.2f:%.3e" % (r["b"], R1v/eps**3)
    print(line)
json.dump(rows, open("phi2_table_num.json", "w"), indent=1)
print("done")
