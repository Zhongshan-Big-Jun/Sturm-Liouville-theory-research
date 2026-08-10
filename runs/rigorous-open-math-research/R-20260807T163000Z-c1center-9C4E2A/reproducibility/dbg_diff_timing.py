# -*- coding: utf-8 -*-
import sympy as sp, time
pi = sp.pi
s, s1, s2, a, b, R = sp.symbols("s s1 s2 a b R", real=True)
m = sp.sqrt(R); w = b - a
def Fexpr(sv):
    al = sv*a; be = sv*(1-b); th = sv*m*w
    ca, sa = sp.cos(al), sp.sin(al); cb, sb = sp.cos(be), sp.sin(be); ct, st = sp.cos(th), sp.sin(th)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca
def nexp(sv):
    al = sv*a; th = sv*m*w; L = w; be1 = 1-b
    I1 = a/2 - sp.sin(2*al)/(4*sv)
    Icc = L/2 + sp.sin(2*th)/(4*sv*m); Iss = L/2 - sp.sin(2*th)/(4*sv*m)
    Ics = sp.sin(th)**2/(2*sv*m)
    sa, ca = sp.sin(al), sp.cos(al)
    I2 = sa**2*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
    yb = sa*sp.cos(th) + (ca/m)*sp.sin(th)
    ypb = -m*sp.sin(th)*sa + sp.cos(th)*ca
    Icc3 = be1/2 + sp.sin(2*sv*be1)/(4*sv); Iss3 = be1/2 - sp.sin(2*sv*be1)/(4*sv)
    Ics3 = sp.sin(sv*be1)**2/(2*sv)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/sv**2
    return (I1 + R*I2)/sv**2 + I3
t0 = time.time()
Fs = sp.diff(Fexpr(s), s); Fa = sp.diff(Fexpr(s), a); Fb = sp.diff(Fexpr(s), b)
print("F partials: %.1fs" % (time.time()-t0), flush=True)
R1 = sp.sin(s1*a)**2/nexp(s1) - sp.sin(s2*a)**2/nexp(s2)
t0 = time.time()
dR1da_fix = sp.diff(R1, a)
print("diff R1 w.r.t. a: %.1fs len=%d" % (time.time()-t0, len(str(dR1da_fix))), flush=True)
t0 = time.time()
dR1ds1 = sp.diff(R1, s1)
print("diff R1 w.r.t. s1: %.1fs len=%d" % (time.time()-t0, len(str(dR1ds1))), flush=True)
