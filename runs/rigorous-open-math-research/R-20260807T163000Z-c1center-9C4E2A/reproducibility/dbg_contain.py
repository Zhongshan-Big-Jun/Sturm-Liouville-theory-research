# -*- coding: utf-8 -*-
"""dbg_contain.py - EVIDENCE: interval feasibility of the containment
a0 < A_eps(b) < a0+0.03 via R1(a0,b)<0<R1(a0+0.03,b) with FH enclosures."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
d3 = pickle.load(open(os.path.join(HERE, "R1_partials_exprs.pkl"), "rb"))
s1s, s2s, a_s, b_s, R_s = sp.symbols("s1 s2 a b R")
def fix_pow(expr):
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(1, 2), lambda t: sp.sqrt(t.base))
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(-1, 2), lambda t: 1/sp.sqrt(t.base))
    return expr
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
R1_f = sp.lambdify((s1s, s2s, a_s, b_s, R_s), fix_pow(sp.sympify(d3["R1"])), modules=mods)
def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
eps0 = 0.05
S1 = box(float(mp.sqrt(mp.pi**2 - eps0)), float(mp.pi))
S2 = box(float(mp.sqrt(4*mp.pi**2 - eps0)), float(2*mp.pi))

def phi_cf(bv):
    s15 = float(np.sqrt(15)); pi = float(np.pi)
    fc = 15*pi**3*s15/4
    R1_1 = pi*(1920*s15*pi**2*a0f**2 - 1920*s15*pi**2*a0f*bv + 64*s15*pi*a0f*np.sin(2*pi*bv)
               + 448*s15*pi*a0f*np.sin(4*pi*bv) + 2700*pi*a0f - 1920*pi*bv*np.cos(2*pi*bv)**2
               + 960*pi*bv*np.cos(2*pi*bv) + 960*pi*bv + 960*np.sin(2*pi*bv) - 480*np.sin(4*pi*bv)
               + 1920*pi*np.cos(2*pi*bv)**2 - 960*pi*np.cos(2*pi*bv) - 2310*pi - 225*s15)/1024
    return -R1_1/fc

# phi at some points
for b in (0.50, 0.52, 0.55, 0.5504, 0.56, 0.58):
    print("phi(%.4f) = %.6f" % (b, phi_cf(b)))

print()
print("=== R1(a0, b, e) and R1(a0+0.03, b, e) over cells (FH enclosures) ===")
nb = 9
for (blo, bhi) in [(0.50,0.55),(0.55,0.60),(0.60,0.70),(0.70,0.85),(0.85,0.95),(0.95,1.0)]:
    for (elo, ehi) in [(1e-3, 0.025), (0.025, 0.05)]:
        bcell = box(blo, bhi); ecell = box(elo, ehi); Rc = 1 + ecell
        v_lo = R1_f(S1, S2, box(a0f, a0f), bcell, Rc)
        v_hi = R1_f(S1, S2, box(a0f+0.03, a0f+0.03), bcell, Rc)
        ok = (mp.mpf(v_lo.b) < 0) and (mp.mpf(v_hi.a) > 0)
        print("  b=[%.2f,%.2f] e=[%.1e,%.3f]: R1(a0)=[%+.3e,%+.3e] R1(a0+.03)=[%+.3e,%+.3e]  %s"
              % (blo,bhi,elo,ehi, float(mp.mpf(v_lo.a)), float(mp.mpf(v_lo.b)),
                 float(mp.mpf(v_hi.a)), float(mp.mpf(v_hi.b)), "OK" if ok else "FAIL"))
