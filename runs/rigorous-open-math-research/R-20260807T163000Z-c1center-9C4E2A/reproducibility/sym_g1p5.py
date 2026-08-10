# -*- coding: utf-8 -*-
"""sym_g1p5.py: exact partials of R1/R2 evaluated on the branch, fast."""
import sympy as sp, mpmath as mp, numpy as np
mp.mp.dps = 40

a, b, R, s = sp.symbols("a b R s", positive=True)
m = sp.sqrt(R)
al = s*a; be = s*(1-b); th = s*m*(b-a)
ca, sa = sp.cos(al), sp.sin(al)
cb, sb = sp.cos(be), sp.sin(be)
ct, st = sp.cos(th), sp.sin(th)
F = cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca
Fs = sp.diff(F, s); Fa = sp.diff(F, a); Fb = sp.diff(F, b)

L = b - a
I1 = a/2 - sp.sin(2*al)/(4*s)
Icc = L/2 + sp.sin(2*th)/(4*s*m)
Iss = L/2 - sp.sin(2*th)/(4*s*m)
Ics = sp.sin(th)**2/(2*s*m)
I2 = sa*sa*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
yb = sa*sp.cos(th) + (ca/m)*sp.sin(th)
ypb = -m*sp.sin(th)*sp.sin(al) + sp.cos(th)*sp.cos(al)
Icc3 = (1-b)/2 + sp.sin(2*s*(1-b))/(4*s)
Iss3 = (1-b)/2 - sp.sin(2*s*(1-b))/(4*s)
Ics3 = sp.sin(s*(1-b))**2/(2*s)
I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/s**2
n = (I1 + R*I2)/s**2 + I3
s1, s2 = sp.symbols("s1 s2", positive=True)
R1 = sp.sin(s1*a)**2/n.subs(s,s1) - sp.sin(s2*a)**2/n.subs(s,s2)

def s_part(sv, var):
    return -sp.diff(F, var).subs(s, sv)/sp.diff(F, s).subs(s, sv)
def total_part(Rexpr, var):
    return sp.diff(Rexpr, var) + sp.diff(Rexpr, s1)*s_part(s1, var) + sp.diff(Rexpr, s2)*s_part(s2, var)
R1_a = total_part(R1, a); R1_b = total_part(R1, b)
def yb_sym(sv):
    return (sa*sp.cos(th) + (ca/m)*sp.sin(th)).subs(s, sv)/sv
def mk_R2(sv):
    ybv = yb_sym(sv)
    return sv**2*ybv**2/n.subs(s,sv)
R2 = mk_R2(s1) - mk_R2(s2)
R2_a = total_part(R2, a)

f_R1a = sp.lambdify((a,b,R,s1,s2), R1_a, "mpmath")
f_R1b = sp.lambdify((a,b,R,s1,s2), R1_b, "mpmath")
f_R2a = sp.lambdify((a,b,R,s1,s2), R2_a, "mpmath")

def sec_np(sv, aa, bb, RR):
    mm = np.sqrt(RR)
    return (np.cos(sv*(1-bb))*np.cos(sv*mm*(bb-aa))*np.sin(sv*aa)
            - mm*np.sin(sv*(1-bb))*np.sin(sv*mm*(bb-aa))*np.sin(sv*aa)
            + (np.cos(sv*(1-bb))*np.sin(sv*mm*(bb-aa))/mm)*np.cos(sv*aa)
            + np.sin(sv*(1-bb))*np.cos(sv*mm*(bb-aa))*np.cos(sv*aa))
def roots2_np(aa, bb, RR):
    s = np.linspace(1e-9, 7.0, 6001)
    M = sec_np(s, aa, bb, RR)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0][:2]
    out = []
    for i in idx:
        lo, hi = s[i], s[i+1]; flo = M[i]
        for _ in range(60):
            md = 0.5*(lo+hi)
            if np.signbit(sec_np(md, aa, bb, RR)) == np.signbit(flo): lo = md
            else: hi = md
        out.append(0.5*(lo+hi))
    return out
def sec_mp(sv, aa, bb, RR):
    mm = mp.sqrt(RR)
    return (mp.cos(sv*(1-bb))*mp.cos(sv*mm*(bb-aa))*mp.sin(sv*aa)
            - mm*mp.sin(sv*(1-bb))*mp.sin(sv*mm*(bb-aa))*mp.sin(sv*aa)
            + (mp.cos(sv*(1-bb))*mp.sin(sv*mm*(bb-aa))/mm)*mp.cos(sv*aa)
            + mp.sin(sv*(1-bb))*mp.cos(sv*mm*(bb-aa))*mp.cos(sv*aa))
def roots2_mp(aa, bb, RR):
    r1, r2 = roots2_np(float(aa), float(bb), float(RR))
    out = []
    for r0 in [r1, r2]:
        x = mp.mpf(float(r0))
        for _ in range(12):
            fx = sec_mp(x, aa, bb, RR)
            h = mp.mpf('1e-8')
            fpx = (sec_mp(x+h, aa, bb, RR) - sec_mp(x-h, aa, bb, RR))/(2*h)
            x = x - fx/fpx
        out.append(x)
    return out
def n_mp(sv, aa, bb, RR):
    mm = mp.sqrt(RR); LL = bb-aa; be = 1-bb
    al = sv*aa; th = sv*mm*LL
    I1 = aa/2 - mp.sin(2*al)/(4*sv)
    Icc = LL/2 + mp.sin(2*th)/(4*sv*mm)
    Iss = LL/2 - mp.sin(2*th)/(4*sv*mm)
    Ics = mp.sin(th)**2/(2*sv*mm)
    sa, ca = mp.sin(al), mp.cos(al)
    I2 = sa*sa*Icc + (ca/mm)**2*Iss + 2*sa*(ca/mm)*Ics
    yb = sa*mp.cos(th) + (ca/mm)*mp.sin(th)
    ypb = -mm*mp.sin(th)*mp.sin(al) + mp.cos(th)*mp.cos(al)
    Icc3 = be/2 + mp.sin(2*sv*be)/(4*sv)
    Iss3 = be/2 - mp.sin(2*sv*be)/(4*sv)
    Ics3 = mp.sin(sv*be)**2/(2*sv)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/sv**2
    return (I1 + RR*I2)/sv**2 + I3
def R1num(aa, bb, RR):
    s1v, s2v = roots2_mp(aa, bb, RR)
    n1 = n_mp(s1v, aa, bb, RR); n2 = n_mp(s2v, aa, bb, RR)
    return (mp.sin(s1v*aa)**2/n1 - mp.sin(s2v*aa)**2/n2).real

for RRs in ["4","100","1000","1e6"]:
    RR = mp.mpf(RRs)
    lo, hi = mp.mpf('0.40'), mp.mpf('0.5')
    for _ in range(50):
        md = (lo+hi)/2
        if R1num(md, 1-md, RR) < 0: lo = md
        else: hi = md
    fp = (lo+hi)/2
    aa = fp + mp.mpf('0.02')
    blo, bhi = 1-fp - mp.mpf('0.2'), 1-fp + mp.mpf('0.2')
    for _ in range(50):
        bmd = (blo+bhi)/2
        if R1num(aa, bmd, RR)*R1num(aa, blo, RR) < 0: bhi = bmd
        else: blo = bmd
    bb = (blo+bhi)/2
    s1v, s2v = roots2_mp(aa, bb, RR)
    v = f_R1a(aa, bb, RR, s1v, s2v)
    w = f_R1b(aa, bb, RR, s1v, s2v)
    u = f_R2a(aa, bb, RR, s1v, s2v)
    print("R=%s  a=%s b=%s" % (RRs, mp.nstr(aa,12), mp.nstr(bb,12)))
    print("  R1_a=%s R1_b=%s R2_a=%s" % (mp.nstr(v.real,12), mp.nstr(w.real,12), mp.nstr(u.real,12)))
    print("  P2 check R1_b + R2_a = %s" % mp.nstr((w.real+u.real),3))
    print("  G = %s" % mp.nstr((-(v/w)).real,15))

