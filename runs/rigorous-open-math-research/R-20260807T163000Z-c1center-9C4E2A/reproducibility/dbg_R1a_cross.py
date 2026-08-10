# -*- coding: utf-8 -*-
"""dbg_R1a_cross.py - cross-check pickle R1_a vs sym_cert_partials.R1_a vs FD (two steps)."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cert_lib
from sym_cert_partials import R1_a as R1a_old, R1_b as R1b_old

d = pickle.load(open(os.path.join(HERE, "R1_partials_exprs.pkl"), "rb"))
s1s, s2s, a_s, b_s, R_s = sp.symbols("s1 s2 a b R")
def fix_pow(expr):
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(1, 2), lambda t: sp.sqrt(t.base))
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(-1, 2), lambda t: 1/sp.sqrt(t.base))
    return expr
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf}, "mpmath"]
R1a_new = sp.lambdify((s1s, s2s, a_s, b_s, R_s), fix_pow(sp.sympify(d["R1_a"])), modules=mods)
R1b_new = sp.lambdify((s1s, s2s, a_s, b_s, R_s), fix_pow(sp.sympify(d["R1_b"])), modules=mods)

def pt(x): return iv.mpf([mp.mpf(x), mp.mpf(x)])

def sec_mp(s, a, b, eps):
    q = mp.sqrt(1+eps); al = s*a; be = s*(1-b); th = q*s*(b-a)
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

mp.mp.dps = 60
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
for (an, bn, epsn) in [(a0, 0.5, 0.01), (a0+0.005, 0.6, 0.05)]:
    am, bm, em = mp.mpf(an), mp.mpf(bn), mp.mpf(epsn)
    c = cfg_mp(am, bm, em); s1, s2 = c[0], c[1]
    n1, n2 = c[2], c[3]
    new_a = R1a_new(pt(s1), pt(s2), pt(am), pt(bm), pt(1+em))
    new_b = R1b_new(pt(s1), pt(s2), pt(am), pt(bm), pt(1+em))
    old_a = R1a_old(s1, s2, am, bm, 1+em)
    old_b = R1b_old(s1, s2, am, bm, 1+em)
    print("point a=%.5f b=%.4f eps=%.3f" % (an, bn, epsn))
    print("  new R1_a = %s" % mp.nstr(new_a, 12))
    print("  old R1_a = %s" % mp.nstr(old_a, 12))
    print("  new R1_b = %s" % mp.nstr(new_b, 12))
    print("  old R1_b = %s" % mp.nstr(old_b, 12))
    for h in ("1e-7", "1e-9", "1e-12"):
        hh = mp.mpf(h)
        dfa = (R1_mp(am+hh, bm, em) - R1_mp(am-hh, bm, em))/(2*hh)
        dfb = (R1_mp(am, bm+hh, em) - R1_mp(am, bm-hh, em))/(2*hh)
        print("  FD h=%s: R1_a=%.10f  R1_b=%.10f" % (h, dfa, dfb))
