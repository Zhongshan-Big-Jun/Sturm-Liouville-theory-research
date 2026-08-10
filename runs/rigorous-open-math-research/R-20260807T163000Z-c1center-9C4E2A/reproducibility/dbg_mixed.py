# -*- coding: utf-8 -*-
import mpmath as mp
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
mp.mp.dps = 50
pi = mp.pi

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

a0m = mp.acos(mp.mpf(1)/4)/pi
eps = mp.mpf('0.001')
print("dR1_b/da (mixed partial) at (a0,b,eps=0.001):")
for b in (0.5, 0.7, 0.9, 0.99):
    da = float(mp.diff(lambda aa: mp.diff(lambda bb: f_at(aa, bb, eps), b, 1), a0m, 1))
    print("  b=%.2f: d_a R1_b = %.4f" % (b, da))
print("R1_aa at (a0,b,eps=0.001):")
for b in (0.5, 0.7, 0.9, 0.99):
    v = float(mp.diff(lambda aa: f_at(aa, b, eps), a0m, 2))
    print("  b=%.2f: R1_aa = %.2f" % (b, v))
print("R1_bb at (a0,b,eps=0.001):")
for b in (0.5, 0.7, 0.9, 0.99):
    v = float(mp.diff(lambda bb: f_at(a0m, bb, eps), b, 2))
    print("  b=%.2f: R1_bb = %.2f" % (b, v))
