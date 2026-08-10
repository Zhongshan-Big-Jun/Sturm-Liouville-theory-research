# -*- coding: utf-8 -*-
"""sym_g1p3.py: evaluate exact partials at branch points; check P2."""
import sympy as sp, mpmath as mp
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
    Fv = F.subs(s, sv)
    return -sp.diff(Fv, var)/sp.diff(Fv, s)
def total_part(Rexpr, var):
    return sp.diff(Rexpr, var) + sp.diff(Rexpr, s1)*s_part(s1, var) + sp.diff(Rexpr, s2)*s_part(s2, var)
R1_a = total_part(R1, a); R1_b = total_part(R1, b)

def yb_sym(sv):
    return (sa.subs(s,sv)*sp.cos(th.subs(s,sv)) + (ca.subs(s,sv)/m)*sp.sin(th.subs(s,sv)))/sv
def mk_R2(sv):
    ybv = yb_sym(sv)
    return sv**2*ybv**2/n.subs(s,sv)
R2 = mk_R2(s1) - mk_R2(s2)
R2_a = total_part(R2, a)

def secnum(sv, aa, bb, RR):
    mm = mp.sqrt(RR)
    return (mp.cos(sv*(1-bb))*mp.cos(sv*mm*(bb-aa))*mp.sin(sv*aa)
            - mm*mp.sin(sv*(1-bb))*mp.sin(sv*mm*(bb-aa))*mp.sin(sv*aa)
            + (mp.cos(sv*(1-bb))*mp.sin(sv*mm*(bb-aa))/mm)*mp.cos(sv*aa)
            + mp.sin(sv*(1-bb))*mp.cos(sv*mm*(bb-aa))*mp.cos(sv*aa))
def roots2_mp(aa, bb, RR):
    ns = 4000
    xs = [mp.mpf(k)*mp.mpf(7.0)/ns for k in range(ns+1)]
    vals = [secnum(x, aa, bb, RR) for x in xs]
    out = []
    for i in range(ns):
        if vals[i]*vals[i+1] < 0:
            lo, hi = xs[i], xs[i+1]; flo = vals[i]
            for _ in range(80):
                md = (lo+hi)/2
                if secnum(md, aa, bb, RR)*flo > 0: lo = md
                else: hi = md
            out.append((lo+hi)/2)
            if len(out)==2: break
    return out
def eval_expr(expr, aa, bb, RR, s1v, s2v):
    subs = {a: aa, b: bb, R: RR, s1: s1v, s2: s2v}
    return complex(sp.N(expr.subs(subs), 45))
def R1num(aa, bb, RR):
    s1v, s2v = roots2_mp(aa, bb, RR)
    n1 = eval_expr(n.subs(s,s1), aa, bb, RR, s1v, s2v)
    n2 = eval_expr(n.subs(s,s2), aa, bb, RR, s1v, s2v)
    return (mp.sin(s1v*aa)**2/n1 - mp.sin(s2v*aa)**2/n2).real

for RRs in ["4","100","1000","1e6"]:
    RR = mp.mpf(RRs)
    lo, hi = mp.mpf('0.40'), mp.mpf('0.5')
    for _ in range(60):
        md = (lo+hi)/2
        if R1num(md, 1-md, RR) < 0: lo = md
        else: hi = md
    fp = (lo+hi)/2
    aa = fp + mp.mpf('0.02')
    blo, bhi = 1-fp - mp.mpf('0.2'), 1-fp + mp.mpf('0.2')
    def r1b(bb): return R1num(aa, bb, RR)
    for _ in range(50):
        bmd = (blo+bhi)/2
        if r1b(bmd)*r1b(blo) < 0: bhi = bmd
        else: blo = bmd
    bb = (blo+bhi)/2
    s1v, s2v = roots2_mp(aa, bb, RR)
    v = eval_expr(R1_a, aa, bb, RR, s1v, s2v)
    w = eval_expr(R1_b, aa, bb, RR, s1v, s2v)
    u = eval_expr(R2_a, aa, bb, RR, s1v, s2v)
    G = -(v/w)
    print("R=%s  a=%s b=%s" % (RRs, mp.nstr(aa,12), mp.nstr(bb,12)))
    print("  R1_a=%s R1_b=%s R2_a=%s" % (mp.nstr(v.real,12), mp.nstr(w.real,12), mp.nstr(u.real,12)))
    print("  P2 check R1_b + R2_a = %s" % mp.nstr((w.real+u.real),3))
    print("  G = %s" % mp.nstr(G.real,15))
