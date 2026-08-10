# -*- coding: utf-8 -*-
"""cert_R1a_v5.py - CERTIFIED: R1_a > 0 on the main box
  a in [a0-0.03, a0+0.03], b in [a0, 1.0], R in [1, 1+eps0], eps0 = 0.05.
CORRECTION (F-020): cert_R1a_v4.py used the enclosure [sqrt(k^2 pi^2 - eps0), k*pi]
justified by "FH |lambda_k'| <= 1", which is FALSE on the box (true min s1 over
the box is 3.11396 < sqrt(pi^2 - 0.05) = 3.13362).  The sound enclosure is
  s_k in [k*pi/sqrt(1+eps0), k*pi]
from the elementary comparison 1 <= rho <= 1+eps:
  lambda_k(1+eps) = k^2 pi^2/(1+eps) <= lambda_k(rho) <= lambda_k(1) = k^2 pi^2.
Cell-wise mpmath.iv 200-bit.  Output: cert_R1a_v5.json (ASCII)."""
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
R1a_f = sp.lambdify((s1s, s2s, a_s, b_s, R_s), fix_pow(sp.sympify(d3["R1_a"])), modules=mods)
R1_f  = sp.lambdify((s1s, s2s, a_s, b_s, R_s), fix_pow(sp.sympify(d3["R1"])),  modules=mods)
def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)

eps0 = 0.05
sq = float(mp.sqrt(mp.mpf('1.05')))
S1 = box(mp.pi/sq, mp.pi)
S2 = box(2*mp.pi/sq, 2*mp.pi)
print("S1 = [%.6f, %.6f]  S2 = [%.6f, %.6f]  (sound enclosure, F-020)" % (mp.mpf(S1.a), mp.mpf(S1.b), mp.mpf(S2.a), mp.mpf(S2.b)))

Na, Nb, Ne = 12, 80, 2
min_lb = mp.mpf("inf"); worst = None; nfail = 0; nf_info = None
b_edges = [a0f + (1.0-a0f)*i/Nb for i in range(Nb+1)]
for i in range(Na):
    for j in range(Nb):
        for kk in range(Ne):
            a_cell = box(a0f-0.03+0.06*i/Na, a0f-0.03+0.06*(i+1)/Na)
            b_cell = box(b_edges[j], b_edges[j+1])
            e_cell = box(eps0*kk/Ne, eps0*(kk+1)/Ne)
            Rc = 1 + e_cell
            R1a = R1a_f(S1, S2, a_cell, b_cell, Rc)
            if not (mp.isfinite(mp.mpf(R1a.a)) and mp.isfinite(mp.mpf(R1a.b))):
                nfail += 1
                if nf_info is None:
                    nf_info = dict(i=i, j=j, k=kk)
                continue
            lb = mp.mpf(R1a.a)
            if lb < min_lb:
                min_lb = lb
                worst = dict(i=i, j=j, k=kk, a=[float(mp.mpf(a_cell.a)), float(mp.mpf(a_cell.b))],
                             b=[float(mp.mpf(b_cell.a)), float(mp.mpf(b_cell.b))],
                             e=[float(mp.mpf(e_cell.a)), float(mp.mpf(e_cell.b))],
                             lb=float(lb), ub=float(mp.mpf(R1a.b)))
status = "PASS" if (nfail == 0 and min_lb > 0) else "FAIL"
print("status=%s  nfail=%d  min_R1a_lb=%.4f" % (status, nfail, float(min_lb)))
if worst: print("worst:", worst)
out = dict(status=status, eps0=eps0, Na=Na, Nb=Nb, Ne=Ne, bmax=1.0,
           S1=[str(S1.a), str(S1.b)], S2=[str(S2.a), str(S2.b)],
           enclosure="k*pi/sqrt(1+eps0) <= s_k <= k*pi (elementary weight comparison, F-020)",
           min_R1a_lb=float(min_lb), worst_cell=worst, nfail=nfail, nfail_info=nf_info,
           correction="v4 enclosure invalid: true min s1 = 3.11396 < sqrt(pi^2-0.05); v5 uses sound enclosure",
           runtime_s=round(time.time()-t0, 1),
           note="root enclosure via 1<=rho<=1+eps comparison, elementary and sound; mpmath.iv 200-bit cell-wise")
with open(os.path.join(HERE, "cert_R1a_v5.json"), "w") as f:
    json.dump(out, f, indent=1)
print("written cert_R1a_v5.json, runtime=%.1fs" % (time.time()-t0))