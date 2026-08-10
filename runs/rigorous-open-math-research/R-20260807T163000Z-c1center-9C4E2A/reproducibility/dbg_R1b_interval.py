# -*- coding: utf-8 -*-
"""dbg_R1b_interval.py - EVIDENCE: interval width of R1_b with FH root enclosures
near b=1. Determines whether cell-wise sign certification of R1_b<0 is feasible."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os
HERE = os.path.dirname(os.path.abspath(__file__))
d3 = pickle.load(open(os.path.join(HERE, "R1_partials_exprs.pkl"), "rb"))
s1s, s2s, a_s, b_s, R_s = sp.symbols("s1 s2 a b R")
def fix_pow(expr):
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(1, 2), lambda t: sp.sqrt(t.base))
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(-1, 2), lambda t: 1/sp.sqrt(t.base))
    return expr
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
R1b_f = sp.lambdify((s1s, s2s, a_s, b_s, R_s), fix_pow(sp.sympify(d3["R1_b"])), modules=mods)
def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
eps0 = 0.05
S1 = box(float(mp.sqrt(mp.pi**2 - eps0)), float(mp.pi))
S2 = box(float(mp.sqrt(4*mp.pi**2 - eps0)), float(2*mp.pi))
print("S1 width=%.2e S2 width=%.2e" % (float(mp.mpf(S1.b)-mp.mpf(S1.a)), float(mp.mpf(S2.b)-mp.mpf(S2.a))))

# sheet a at eps, near b=1 (true values for center)
import numpy as np, sys
sys.path.insert(0, HERE)
from fast_lib import R1R2
def sheet_a(b, eps):
    lo, hi = a0f-0.02, a0f+0.02
    for _ in range(60):
        md = 0.5*(lo+hi)
        if np.signbit(R1R2(md, b, 1+eps)[0]) == np.signbit(R1R2(lo, b, 1+eps)[0]): lo = md
        else: hi = md
    return 0.5*(lo+hi)

print("=== R1_b interval over (a,b,eps) cells; FH enclosures ===")
for (blo, bhi) in [(0.90,0.95),(0.95,0.98),(0.98,0.99),(0.99,0.995),(0.995,0.999),(0.999,1.0)]:
    for e in (0.025, 0.05):
        # a-cell around the sheet at eps=e, b=(blo+bhi)/2
        a_c = sheet_a(0.5*(blo+bhi), e)
        for dA in (0.005, 0.01):
            acell = box(a_c-dA, a_c+dA)
            bcell = box(blo, bhi)
            ecell = box(0.0, e) if e==0.025 else box(0.025, e)
            Rc = 1 + ecell
            R1b = R1b_f(S1, S2, acell, bcell, Rc)
            w = float(mp.mpf(R1b.b)-mp.mpf(R1b.a))
            # true value at center
            ac = 0.5*(float(mp.mpf(acell.a))+float(mp.mpf(acell.b)))
            bc = 0.5*(blo+bhi)
            print("  b=[%.3f,%.3f] e=[%.3f,%.3f] dA=%.3f: R1_b=[%+.2e,%+.2e] width=%.2e"
                  % (blo,bhi,float(mp.mpf(ecell.a)),float(mp.mpf(ecell.b)),dA,float(mp.mpf(R1b.a)),float(mp.mpf(R1b.b)),w))
