# -*- coding: utf-8 -*-
"""constants_gap1r.py - empirical constants for the R->1+ Gap 1 (EVIDENCE).
Computes the constants in the A10 IFT estimates and the resulting eps_0."""
import mpmath as mp
import numpy as np, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
mp.mp.dps = 60
pi = mp.pi
a0n = float(mp.acos(mp.mpf(1)/4)/pi)
b0 = 1 - a0n
s15 = float(mp.sqrt(15))

# ---- closed forms ----
def phi_cf(bv):
    fc = 15*np.pi**3*s15/4
    R1_1 = np.pi*(1920*s15*np.pi**2*a0n**2 - 1920*s15*np.pi**2*a0n*bv + 64*s15*np.pi*a0n*np.sin(2*np.pi*bv)
               + 448*s15*np.pi*a0n*np.sin(4*np.pi*bv) + 2700*np.pi*a0n - 1920*np.pi*bv*np.cos(2*np.pi*bv)**2
               + 960*np.pi*bv*np.cos(2*np.pi*bv) + 960*np.pi*bv + 960*np.sin(2*np.pi*bv) - 480*np.sin(4*np.pi*bv)
               + 1920*np.pi*np.cos(2*np.pi*bv)**2 - 960*np.pi*np.cos(2*np.pi*bv) - 2310*np.pi - 225*s15)/1024
    return -R1_1/fc

def dphi_cf(bv):
    u = np.cos(2*np.pi*bv); v = np.sin(2*np.pi*bv)
    N = (56*np.pi*a0n - 6*s15)*u**2 + (2*np.pi*a0n + 3*s15)*u + (3*s15 - 58*np.pi*a0n) + 2*s15*np.pi*(1-bv)*(1-4*u)*v
    return -N/(60*np.pi)

def fconst(xn):
    return 2*np.pi**2*(np.sin(np.pi*xn)**2 - 4*np.sin(2*np.pi*xn)**2)
def fconst1(xn):  # derivative by hand
    return 2*np.pi**3*(np.sin(2*np.pi*xn) - 8*np.sin(4*np.pi*xn))
def fconst2(xn):
    return 4*np.pi**4*(np.cos(2*np.pi*xn) - 16*np.cos(4*np.pi*xn))
def fconst3(xn):
    return -8*np.pi**5*(np.sin(2*np.pi*xn) - 64*np.sin(4*np.pi*xn))

# ---- R1_1 and its a-derivative numerically (via f_at perturbation coefficients) ----
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
    return mp.findroot(lambda s: sec_mp(s, a, b, eps), k*pi, tol=1e-50, maxsteps=80)
def f_at(a, b, eps):
    s1 = root_mp(1, a, b, eps); s2 = root_mp(2, a, b, eps)
    n1 = norm_mp(s1, a, b, eps); n2 = norm_mp(s2, a, b, eps)
    y1a = mp.sin(s1*a)/s1; y2a = mp.sin(s2*a)/s2
    return s1**2*y1a**2/n1 - s2**2*y2a**2/n2
def R1_1(a, b): return float(mp.diff(lambda e: f_at(a, b, e), 0, 1))
def R1_2(a, b): return float(mp.diff(lambda e: f_at(a, b, e), 0, 2))

# ---- grids ----
Da = 0.03   # a-neighborhood half-width
ag = np.linspace(a0n-Da, a0n+Da, 9)
bg = np.linspace(a0n, 1.0, 21)

print("=== phi / phi' bounds (closed form) ===")
bg2 = np.linspace(a0n, 0.999999, 20001)
P = max(abs(phi_cf(b)) for b in bg2)
c_phi_099 = min(dphi_cf(b) for b in np.linspace(a0n, 0.99, 20001))
Phi_max_1 = max(abs(dphi_cf(b)) for b in bg2)
Phi_max = max(abs(dphi_cf(b)) for b in np.linspace(a0n, 1.0-1e-12, 20001))
print("P = max|phi| on [a0,1)       = %.6f" % P)
print("c_phi_099 = min phi' [a0,0.99]= %.6e" % c_phi_099)
print("Phi_max = max|phi'| on [a0,1) = %.6f" % Phi_max)
print("phi(b0) = %.8f, phi(0.99) = %.8f" % (phi_cf(b0), phi_cf(0.99)))

print()
print("=== f_const derivative bounds on [a0-Da, a0+Da] ===")
F0 = min(abs(fconst1(x)) for x in np.linspace(a0n-Da, a0n+Da, 2001))
F2 = max(abs(fconst2(x)) for x in np.linspace(a0n-Da, a0n+Da, 2001))
F3 = max(abs(fconst3(x)) for x in np.linspace(a0n-Da, a0n+Da, 2001))
print("min|f_const'| = %.4f  (f_const'(a0)=%.4f)" % (F0, fconst1(a0n)))
print("max|f_const''| = %.4f" % F2)
print("max|f_const'''| = %.4f" % F3)

print()
print("=== R1_1 / d_a R1_1 / R1_2 bounds over [a0-Da,a0+Da] x [a0,1] ===")
D0 = D1 = W2max = 0.0
for bv in bg:
    for av in ag:
        r11 = R1_1(av, bv); r12 = R1_2(av, bv)
        D0 = max(D0, abs(r11))
        W2max = max(W2max, abs(r12))
h = 2e-4
for bv in bg:
    for av in ag:
        d = (R1_1(av+h, bv) - R1_1(av-h, bv))/(2*h)
        D1 = max(D1, abs(d))
print("D0 = max|R1_1|      = %.4f" % D0)
print("D1 = max|d_a R1_1|  = %.4f" % D1)
print("W2max = max|R1_2|   = %.4f" % W2max)

print()
print("=== W(a,b,eps) = (R1 - f_const - eps*R1_1)/eps^2 over the domain ===")
def W_val(a, b, eps):
    R1v = float(f_at(a, b, eps))
    return (R1v - fconst(a) - eps*R1_1(a, b))/eps**2
for eps in (1e-2, 1e-3, 1e-4):
    wm = 0.0
    for bv in bg:
        for av in ag:
            wm = max(wm, abs(W_val(av, bv, eps)))
    print("eps=%.0e: max|W| = %.4f" % (eps, wm))

print()
print("=== IFT estimate: |A_eps - a0 - eps*phi| <= C1*eps^2 (crude quadratic solve) ===")
F0n, F2n, Pn, D1n, W0 = F0, F2, P, D1, W2max
# |r| <= [0.5*F2*(eps*P+|r|)^2 + eps*D1*(eps*P+|r|) + W0*eps^2]/F0
for eps in (1e-3, 1e-2, 5e-2, 0.1):
    r = 0.0
    for _ in range(30):
        r = (0.5*F2*(eps*P+r)**2 + eps*D1*(eps*P+r) + W0*eps**2)/F0
    print("eps=%.2g: |r| <= %.4e (eps^2*C1 with C1=%.3f)" % (eps, r, r/eps**2))

print()
print("=== b_top(eps) <= 0.99 check: |f_const(a)| vs eps*(D0+W0*eps) on a in [a0-0.02,a0+0.02], b in [0.99,1] ===")
amin = min(abs(fconst(x)) for x in np.linspace(a0n-0.02, a0n+0.02, 4001))
print("min|f_const| on [a0-0.02,a0+0.02] = %.6f" % amin)
for eps in (1e-2, 5e-2, 0.1):
    print("  eps=%.2g: eps*(D0+W0*eps) = %.4f  vs amin = %.4f  %s"
          % (eps, eps*(D0+W0*eps), amin, "OK" if eps*(D0+W0*eps) < amin else "FAIL"))
# D0 over b in [0.99,1] might be larger than over [a0,1] grid; refine
D0_hi = 0.0
for bv in np.linspace(0.99, 1.0, 21):
    for av in ag:
        D0_hi = max(D0_hi, abs(R1_1(av, bv)))
print("D0 over b in [0.99,1]: %.4f" % D0_hi)

print()
print("=== P0: eps*c - C2*eps^2 > 0 with C2 = crude (D1*P + ...)/F0 * factor ===")
# A_eps'(b) = eps*phi'(b) + E'(b); |E'| <= C2*eps^2; crude C2 from d/db of the IFT estimate
C2_est = 3*(D1*P + W0)/F0   # heuristic factor
print("heuristic C2 = %.3f" % C2_est)
print("eps threshold for c_phi_099: %.3e" % (c_phi_099/C2_est))
print()
print("=== U': eps^2*Phi_max^2*(1+O(eps)) < 1 ===")
print("1/Phi_max = %.4f  (eps must be below this)" % (1/Phi_max))
