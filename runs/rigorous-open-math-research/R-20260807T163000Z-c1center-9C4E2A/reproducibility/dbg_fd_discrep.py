# -*- coding: utf-8 -*-
"""dbg_fd_discrep.py - find why FD of R1_a differs between scripts at same point."""
import mpmath as mp
mp.mp.dps = 60

def sec_mp(s, a, b, eps):
    q = mp.sqrt(1+eps)
    al = s*a; be = s*(1-b); th = q*s*(b-a)
    return (mp.cos(be)*mp.cos(th)*mp.sin(al) - mp.sin(be)*mp.sin(th)*mp.sin(al)
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
    return (I1 + (1+eps)*I2)/s**2 + I3
def root_mp(k, a, b, eps):
    return mp.findroot(lambda s: sec_mp(s, a, b, eps), k*mp.pi, tol=1e-55, maxsteps=80)
def cfg_mp(a, b, eps):
    s1 = root_mp(1, a, b, eps); s2 = root_mp(2, a, b, eps)
    return s1, s2, norm_mp(s1, a, b, eps), norm_mp(s2, a, b, eps)
def R1_mp(a, b, eps):
    s1, s2, n1, n2 = cfg_mp(a, b, eps)
    return s1**2*(mp.sin(s1*a)/s1)**2/n1 - s2**2*(mp.sin(s2*a)/s2)**2/n2

a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
print("a0 (float) = %.17f" % a0f)
am, bm, em = mp.mpf(a0f), mp.mpf(0.5), mp.mpf(0.01)
print("am =", mp.nstr(am, 25), " bm =", mp.nstr(bm, 25), " em =", mp.nstr(em, 25))
for hh in ("1e-5", "1e-7", "1e-9", "1e-12"):
    h = mp.mpf(hh)
    vp = R1_mp(am+h, bm, em); vm = R1_mp(am-h, bm, em)
    dfa = (vp-vm)/(2*h)
    print("  h=%-6s R1(a+h)=%.15f R1(a-h)=%.15f dfa=%.12f" % (hh, vp, vm, dfa))
# also print roots at base and at am+h
c0 = cfg_mp(am, bm, em)
print("base roots: s1=%.12f s2=%.12f  n1=%.6f n2=%.6f" % (c0[0], c0[1], c0[2], c0[3]))
h = mp.mpf("1e-7")
c1 = cfg_mp(am+h, bm, em)
print("a+h roots: s1=%.12f s2=%.12f" % (c1[0], c1[1]))
