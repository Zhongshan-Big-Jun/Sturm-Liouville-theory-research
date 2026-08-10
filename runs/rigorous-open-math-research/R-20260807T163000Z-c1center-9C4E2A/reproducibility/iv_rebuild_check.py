# -*- coding: utf-8 -*-
"""iv_rebuild_check.py v3 - rebuild R1/R1_a/R1_b from R1_partials_exprs.pkl and
compare interval evaluations against mpmath high-precision finite differences.
[EVIDENCE] only; sanity-check of the interval machinery before certification."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp
import pickle, os

HERE = os.path.dirname(os.path.abspath(__file__))
d = pickle.load(open(os.path.join(HERE, "R1_partials_exprs.pkl"), "rb"))
s1s, s2s, a_s, b_s, R_s = sp.symbols("s1 s2 a b R")

def fix_pow(expr):
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(1, 2),
                        lambda t: sp.sqrt(t.base))
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(-1, 2),
                        lambda t: 1/sp.sqrt(t.base))
    return expr

mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf}, "mpmath"]
fns = {}
for key in ("R1", "R1_a", "R1_b"):
    expr = fix_pow(sp.sympify(d[key]))
    fns[key] = sp.lambdify((s1s, s2s, a_s, b_s, R_s), expr, modules=mods)

def pt(x):
    xm = mp.mpf(x)
    return iv.mpf([xm, xm])

a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
print("a0 = %.15f" % a0)

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
    return (I1 + (1+eps)*I2)/s**2 + I3
def root_mp(k, a, b, eps):
    s0 = k*mp.pi
    f = lambda s: sec_mp(s, a, b, eps)
    return mp.findroot(f, s0, tol=1e-55, maxsteps=80)
def cfg_mp(a, b, eps):
    s1 = root_mp(1, a, b, eps); s2 = root_mp(2, a, b, eps)
    return s1, s2, norm_mp(s1, a, b, eps), norm_mp(s2, a, b, eps)
def R1_mp(a, b, eps, c=None):
    if c is None: c = cfg_mp(a, b, eps)
    s1, s2, n1, n2 = c
    return s1**2*(mp.sin(s1*a)/s1)**2/n1 - s2**2*(mp.sin(s2*a)/s2)**2/n2

mp.mp.dps = 60
tests = [(a0, 0.5, 0.01), (a0+0.005, 0.6, 0.05), (a0-0.01, 0.7, 0.02), (a0, 0.9, 0.1), (a0+0.02, 0.99, 0.001)]
print("point check R1:")
ok = True
for (an, bn, epsn) in tests:
    am, bm, em = mp.mpf(an), mp.mpf(bn), mp.mpf(epsn)
    c = cfg_mp(am, bm, em)
    ref = R1_mp(am, bm, em, c)
    s1, s2 = c[0], c[1]
    R1iv = fns["R1"](pt(s1), pt(s2), pt(am), pt(bm), pt(1+em))
    mid = (mp.mpf(R1iv.a) + mp.mpf(R1iv.b))/2
    rel = float(abs(mid - ref)/max(1, abs(ref))) if abs(ref) > 1e-40 else float(abs(mid))
    print("  a=%.5f b=%.4f eps=%.3f  iv=[%.6e, %.6e]  ref=%.6e  rel=%.2e"
          % (an, bn, epsn, float(R1iv.a), float(R1iv.b), ref, rel))
    if R1iv.a > ref or R1iv.b < ref:
        print("    MISMATCH (ref not in interval)"); ok = False

def dR1_da_num(an, bn, epsn):
    h = mp.mpf("1e-7")
    vp = R1_mp(mp.mpf(an)+h, mp.mpf(bn), mp.mpf(epsn))
    vm = R1_mp(mp.mpf(an)-h, mp.mpf(bn), mp.mpf(epsn))
    return (vp-vm)/(2*h)
def dR1_db_num(an, bn, epsn):
    h = mp.mpf("1e-7")
    vp = R1_mp(mp.mpf(an), mp.mpf(bn)+h, mp.mpf(epsn))
    vm = R1_mp(mp.mpf(an), mp.mpf(bn)-h, mp.mpf(epsn))
    return (vp-vm)/(2*h)

print("partials check:")
for (an, bn, epsn) in tests:
    c = cfg_mp(mp.mpf(an), mp.mpf(bn), mp.mpf(epsn))
    s1, s2 = c[0], c[1]
    R1aiv = fns["R1_a"](pt(s1), pt(s2), pt(mp.mpf(an)), pt(mp.mpf(bn)), pt(1+mp.mpf(epsn)))
    R1biv = fns["R1_b"](pt(s1), pt(s2), pt(mp.mpf(an)), pt(mp.mpf(bn)), pt(1+mp.mpf(epsn)))
    dfa = dR1_da_num(an, bn, epsn); dfb = dR1_db_num(an, bn, epsn)
    ca_, cb_ = (mp.mpf(R1aiv.a)+mp.mpf(R1aiv.b))/2, (mp.mpf(R1biv.a)+mp.mpf(R1biv.b))/2
    ra = float(abs(ca_-dfa)/max(1, abs(dfa))); rb = float(abs(cb_-dfb)/max(1, abs(dfb)))
    print("  a=%.5f b=%.4f eps=%.3f  R1_a iv=[%.4e,%.4e] FD=%.4e rel=%.2e | R1_b iv=[%.4e,%.4e] FD=%.4e rel=%.2e"
          % (an, bn, epsn, float(R1aiv.a), float(R1aiv.b), dfa, ra, float(R1biv.a), float(R1biv.b), dfb, rb))
    if R1aiv.a > dfa or R1aiv.b < dfa:
        print("    R1_a MISMATCH"); ok = False
    if R1biv.a > dfb or R1biv.b < dfb:
        print("    R1_b MISMATCH"); ok = False

print("ALL OK" if ok else "FAILURES PRESENT")
