# -*- coding: utf-8 -*-
"""cell_test.py - test interval root enclosure via 2nd-order perturbation and
R1_a interval evaluation over a cell.  [EVIDENCE] feasibility probe."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

d = pickle.load(open(os.path.join(HERE, "pert_coeffs.pkl"), "rb"))
a_s, b_s = sp.symbols("a b")
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
coefs = {}
for k in ("s11", "s12", "s21", "s22"):
    coefs[k] = sp.lambdify((a_s, b_s), sp.sympify(d[k]), modules=mods)

d2 = pickle.load(open(os.path.join(HERE, "R1_partials_exprs.pkl"), "rb"))
s1s, s2s = sp.symbols("s1 s2")
def fix_pow(expr):
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(1, 2), lambda t: sp.sqrt(t.base))
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(-1, 2), lambda t: 1/sp.sqrt(t.base))
    return expr
R1a_f = sp.lambdify((s1s, s2s, a_s, b_s, sp.symbols("R")), fix_pow(sp.sympify(d2["R1_a"])), modules=mods)

def F_iv(s, a, b, R):
    m = iv.sqrt(R)
    ca, sa = iv.cos(s*a), iv.sin(s*a)
    cb, sb = iv.cos(s*(1-b)), iv.sin(s*(1-b))
    ct, st = iv.cos(s*m*(b-a)), iv.sin(s*m*(b-a))
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca
def Fs_iv(s, a, b, R):
    # dF/ds via sympy-free numeric chain: reuse cert_lib
    from cert_lib import Fs_iv as Fs_ref
    return Fs_ref(s, a, b, R)

piI = iv.pi
def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])

def s_k_iv(k, a_iv, b_iv, eps_iv, C):
    k1 = coefs["s%d1" % k](a_iv, b_iv)
    k2 = coefs["s%d2" % k](a_iv, b_iv)
    base = k*piI + k1*eps_iv + k2*eps_iv**2
    return base + box(-C, C)*eps_iv**3

def test_cell(a_lo, a_hi, b_lo, b_hi, e_lo, e_hi, C1, C2, label):
    a_iv, b_iv, e_iv = box(a_lo, a_hi), box(b_lo, b_hi), box(e_lo, e_hi)
    R_iv = 1 + e_iv
    S1 = s_k_iv(1, a_iv, b_iv, e_iv, C1)
    S2 = s_k_iv(2, a_iv, b_iv, e_iv, C2)
    F1 = F_iv(S1, a_iv, b_iv, R_iv)
    F2 = F_iv(S2, a_iv, b_iv, R_iv)
    Fs1 = Fs_iv(S1, a_iv, b_iv, R_iv)
    Fs2 = Fs_iv(S2, a_iv, b_iv, R_iv)
    R1a = R1a_f(S1, S2, a_iv, b_iv, R_iv)
    print("%-28s S1=[%.5f,%.5f] S2=[%.5f,%.5f]" % (label, mp.mpf(S1.a), mp.mpf(S1.b), mp.mpf(S2.a), mp.mpf(S2.b)))
    print("  F(S1) contains 0: %s   Fs(S1) sign excl 0: %s" % (F1.a < 0 < F1.b, Fs1.a > 0 or Fs1.b < 0))
    print("  F(S2) contains 0: %s   Fs(S2) sign excl 0: %s" % (F2.a < 0 < F2.b, Fs2.a > 0 or Fs2.b < 0))
    print("  R1_a over cell: [%.4f, %.4f]" % (mp.mpf(R1a.a), mp.mpf(R1a.b)))

# probe cells (a-cells of width 0.005, b-cells of width 0.02, eps-cells of width 0.025)
C1, C2 = 60.0, 120.0   # generous vs scan (43.3 with order-1 only for s2; s22 included now -> much smaller)
for (blo, bhi) in [(0.42, 0.44), (0.5, 0.52), (0.7, 0.72), (0.97, 0.99)]:
    for (alo, ahi) in [(a0_lo, a0_hi) for (a0_lo, a0_hi) in [(0.3896, 0.3946), (0.4196, 0.4246), (0.4446, 0.4496)]]:
        test_cell(alo, ahi, blo, bhi, 0.0, 0.025, C1, C2, "a=[%.3f,%.3f] b=[%.2f,%.2f] e=[0,.025]" % (alo, ahi, blo, bhi))
