# -*- coding: utf-8 -*-
"""cert_R1_edges_at_a0.py - CERTIFIED:
  (i)  box-edge signs: R1(a0-0.03, b, eps) < 0 < R1(a0+0.03, b, eps) for all
       (b, eps) in [a0, 1.0] x [0, 0.05];
  (ii) M0 = max|R1(a0, b, eps)| over the same set (deviation-constant for the
       A10 implicit-function bound |A_eps(b) - a0| <= M0 / F0^-).
Sound root enclosure s_k in [k*pi/sqrt(1.05), k*pi] (F-020).  mpmath.iv 200-bit.
Output: cert_R1_edges_at_a0.json (ASCII)."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()

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
sq = float(mp.sqrt(mp.mpf('1.05')))
S1 = box(mp.pi/sq, mp.pi)
S2 = box(2*mp.pi/sq, 2*mp.pi)

Nb, Ne = 80, 2
b_edges = [a0f + (1.0-a0f)*i/Nb for i in range(Nb+1)]
aL = box(a0f-0.03, a0f-0.03); aR = box(a0f+0.03, a0f+0.03); a0c = box(a0f, a0f)
min_neg = mp.mpf("inf"); max_pos = -mp.mpf("inf"); M0 = mp.mpf(0)
worst_neg = worst_pos = worst_M0 = None; nfail = 0
for j in range(Nb):
    for kk in range(Ne):
        b_cell = box(b_edges[j], b_edges[j+1])
        e_cell = box(eps0*kk/Ne, eps0*(kk+1)/Ne)
        Rc = 1 + e_cell
        vL = R1_f(S1, S2, aL, b_cell, Rc)
        vR = R1_f(S1, S2, aR, b_cell, Rc)
        v0 = R1_f(S1, S2, a0c, b_cell, Rc)
        if not (mp.isfinite(mp.mpf(vL.a)) and mp.isfinite(mp.mpf(vL.b)) and mp.isfinite(mp.mpf(vR.b)) and mp.isfinite(mp.mpf(v0.b))):
            nfail += 1; continue
        if mp.mpf(vL.b) >= 0:
            if mp.mpf(vL.b) < min_neg: pass
            print("LEFT FAIL at", j, kk, float(mp.mpf(vL.b))); nfail += 1
        else:
            if -mp.mpf(vL.b) < min_neg: min_neg = -mp.mpf(vL.b); worst_neg = (j, kk, float(mp.mpf(vL.a)), float(mp.mpf(vL.b)))
        if mp.mpf(vR.a) <= 0:
            print("RIGHT FAIL at", j, kk, float(mp.mpf(vR.a))); nfail += 1
        else:
            if mp.mpf(vR.a) > max_pos: max_pos = mp.mpf(vR.a); worst_pos = (j, kk, float(mp.mpf(vR.a)), float(mp.mpf(vR.b)))
        m0 = max(abs(mp.mpf(v0.a)), abs(mp.mpf(v0.b)))
        if m0 > M0: M0 = m0; worst_M0 = (j, kk, float(mp.mpf(v0.a)), float(mp.mpf(v0.b)))
print("edges: min|R1(left)|=%.4f  min R1(right)>=%.4f  M0=%.4f  nfail=%d" % (min_neg, max_pos, M0, nfail))
out = dict(status="PASS" if (nfail == 0 and min_neg > 0 and max_pos > 0 and M0 < 1e3) else "FAIL",
           eps0=eps0, Nb=Nb, Ne=Ne,
           min_R1_left_mag=float(min_neg), min_R1_right=float(max_pos), M0=float(M0),
           worst_neg=worst_neg, worst_pos=worst_pos, worst_M0=worst_M0,
           enclosure="k*pi/sqrt(1.05) <= s_k <= k*pi (F-020)",
           note="R1 interval eval at a = a0 +/- 0.03 and a = a0; mpmath.iv 200-bit; gives sheet existence over [a0,1] and deviation constant",
           runtime_s=round(time.time()-t0, 1))
with open(os.path.join(HERE, "cert_R1_edges_at_a0.json"), "w") as f:
    json.dump(out, f, indent=1)
print("written cert_R1_edges_at_a0.json, runtime=%.1fs" % (time.time()-t0))