# -*- coding: utf-8 -*-
"""dbg_chain_pieces.py - compare analytic F/Fa/Fb/Fs and ds/da, ds/db pieces vs FD."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp

s, s1, s2, a, b, R = sp.symbols("s s1 s2 a b R")
m = sp.sqrt(R); w = b - a
def Fexpr(sv):
    al = sv*a; be = sv*(1-b); th = sv*m*w
    ca, sa = sp.cos(al), sp.sin(al); cb, sb = sp.cos(be), sp.sin(be); ct, st = sp.cos(th), sp.sin(th)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca
Fs = sp.diff(Fexpr(s), s); Fa = sp.diff(Fexpr(s), a); Fb = sp.diff(Fexpr(s), b)
def nexp(sv):
    al = sv*a; th = sv*m*w; L = w; be1 = 1-b
    I1 = a/2 - sp.sin(2*al)/(4*sv)
    Icc = L/2 + sp.sin(2*th)/(4*sv*m); Iss = L/2 - sp.sin(2*th)/(4*sv*m)
    Ics = sp.sin(th)**2/(2*sv*m)
    sa_, ca_ = sp.sin(al), sp.cos(al)
    I2 = sa_**2*Icc + (ca_/m)**2*Iss + 2*sa_*(ca_/m)*Ics
    yb = sa_*sp.cos(th) + (ca_/m)*sp.sin(th)
    ypb = -m*sp.sin(th)*sa_ + sp.cos(th)*ca_
    Icc3 = be1/2 + sp.sin(2*sv*be1)/(4*sv); Iss3 = be1/2 - sp.sin(2*sv*be1)/(4*sv)
    Ics3 = sp.sin(sv*be1)**2/(2*sv)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/sv**2
    return (I1 + R*I2)/sv**2 + I3
R1expr = sp.sin(s1*a)**2/nexp(s1) - sp.sin(s2*a)**2/nexp(s2)
# total derivative pieces
d1da_an = -(Fa/Fs).subs(s, s1)
d1db_an = -(Fb/Fs).subs(s, s1)
d2da_an = -(Fa/Fs).subs(s, s2)
d2db_an = -(Fb/Fs).subs(s, s2)
dR1da_an = sp.diff(R1expr, a) + sp.diff(R1expr, s1)*d1da_an + sp.diff(R1expr, s2)*d2da_an
dR1db_an = sp.diff(R1expr, b) + sp.diff(R1expr, s1)*d1db_an + sp.diff(R1expr, s2)*d2db_an

lams = {s1: None, s2: None}
def ev(ex, sv):
    f = sp.lambdify((s1, s2, a, b, R), ex, "mpmath")
    return f(lams[s1], lams[s2], a0m, b0m, R0m)

def sec_mp(sv, a0v, b0v, R0v):
    q = mp.sqrt(R0v); al = sv*a0v; be = sv*(1-b0v); th = sv*q*(b0v-a0v)
    return (mp.cos(be)*mp.cos(th)*mp.sin(al) - q*mp.sin(be)*mp.sin(th)*mp.sin(al)
            + (mp.cos(be)*mp.sin(th)/q)*mp.cos(al) + mp.sin(be)*mp.cos(th)*mp.cos(al))
def root_mp(k, a0v, b0v, R0v):
    return mp.findroot(lambda sv: sec_mp(sv, a0v, b0v, R0v), k*mp.pi, tol=1e-55, maxsteps=80)
def norm_mp(sv, a0v, b0v, R0v):
    q = mp.sqrt(R0v); Lw = b0v-a0v; be = 1-b0v
    al = sv*a0v; th = sv*q*Lw
    I1 = a0v/2 - mp.sin(2*al)/(4*sv)
    Icc = Lw/2 + mp.sin(2*th)/(4*sv*q); Iss = Lw/2 - mp.sin(2*th)/(4*sv*q)
    Ics = mp.sin(th)**2/(2*sv*q)
    sa_, ca_ = mp.sin(al), mp.cos(al)
    I2 = sa_**2*Icc + (ca_/q)**2*Iss + 2*sa_*(ca_/q)*Ics
    yb = sa_*mp.cos(th) + (ca_/q)*mp.sin(th)
    ypb = -q*mp.sin(th)*sa_ + mp.cos(th)*ca_
    Icc3 = be/2 + mp.sin(2*sv*be)/(4*sv); Iss3 = be/2 - mp.sin(2*sv*be)/(4*sv)
    Ics3 = mp.sin(sv*be)**2/(2*sv)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/sv**2
    return (I1 + R0v*I2)/sv**2 + I3
def R1_mp(a0v, b0v, R0v):
    s1v = root_mp(1, a0v, b0v, R0v); s2v = root_mp(2, a0v, b0v, R0v)
    n1 = norm_mp(s1v, a0v, b0v, R0v); n2 = norm_mp(s2v, a0v, b0v, R0v)
    return mp.sin(s1v*a0v)**2/n1 - mp.sin(s2v*a0v)**2/n2

mp.mp.dps = 60
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
for (an, bn, Rn) in [(a0, 0.5, 1.01), (a0+0.005, 0.6, 1.05), (a0, 0.6, 1.0)]:
    a0m, b0m, R0m = mp.mpf(an), mp.mpf(bn), mp.mpf(Rn)
    lams[s1] = root_mp(1, a0m, b0m, R0m); lams[s2] = root_mp(2, a0m, b0m, R0m)
    print("point a=%.5f b=%.4f R=%.3f" % (an, bn, Rn))
    print("  s1=%.12f s2=%.12f" % (lams[s1], lams[s2]))
    # FD ds/da, ds/db
    h = mp.mpf("1e-9")
    ds1da = (root_mp(1, a0m+h, b0m, R0m) - root_mp(1, a0m-h, b0m, R0m))/(2*h)
    ds1db = (root_mp(1, a0m, b0m+h, R0m) - root_mp(1, a0m, b0m-h, R0m))/(2*h)
    ds2da = (root_mp(2, a0m+h, b0m, R0m) - root_mp(2, a0m-h, b0m, R0m))/(2*h)
    ds2db = (root_mp(2, a0m, b0m+h, R0m) - root_mp(2, a0m, b0m-h, R0m))/(2*h)
    print("  ds1da FD=%.10f  an=%.10f" % (ds1da, ev(d1da_an, s1)))
    print("  ds1db FD=%.10f  an=%.10f" % (ds1db, ev(d1db_an, s1)))
    print("  ds2da FD=%.10f  an=%.10f" % (ds2da, ev(d2da_an, s2)))
    print("  ds2db FD=%.10f  an=%.10f" % (ds2db, ev(d2db_an, s2)))
    dfa = (R1_mp(a0m+h, b0m, R0m) - R1_mp(a0m-h, b0m, R0m))/(2*h)
    dfb = (R1_mp(a0m, b0m+h, R0m) - R1_mp(a0m, b0m-h, R0m))/(2*h)
    print("  R1_a FD=%.10f  an=%.10f" % (dfa, ev(dR1da_an, s1)))
    print("  R1_b FD=%.10f  an=%.10f" % (dfb, ev(dR1db_an, s1)))
