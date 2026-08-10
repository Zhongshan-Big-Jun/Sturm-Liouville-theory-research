# -*- coding: utf-8 -*-
"""cert_sheet_error.py - CERTIFIED sheet error bound:
  |A_eps(b) - a0 - eps*phi(b)| < C_sheet * eps^2
  for b in [a0, 0.99], eps in [0, eps0].
Method: for each (b,eps) cell, evaluate R1 (with FH root enclosures) at
  a_lo = a0 + e*phi(b) - C*e^2 and a_hi = a0 + e*phi(b) + C*e^2;
  if R1(a_lo) < 0 < R1(a_hi) strictly over the cell, then (R1_a > 0 on the
  box being certified) the unique root A_eps(b) lies in (a_lo, a_hi).
Output: cert_sheet_error.json."""
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
piI = iv.pi
s15I = iv.sqrt(15)
a0I = iv.atan2(s15I/4, iv.mpf(1)/4)/piI
def phi_iv(b):
    br = 57600*piI**2
    num = (-1920*s15I*piI**2*a0I**2 + 1920*s15I*piI**2*a0I*b
           - 64*s15I*piI*a0I*iv.sin(2*piI*b) - 448*s15I*piI*a0I*iv.sin(4*piI*b)
           - 2700*piI*a0I + 1920*piI*b*iv.cos(2*piI*b)**2 - 960*piI*b*iv.cos(2*piI*b)
           - 960*piI*b - 960*iv.sin(2*piI*b) + 480*iv.sin(4*piI*b)
           - 1920*piI*iv.cos(2*piI*b)**2 + 960*piI*iv.cos(2*piI*b)
           + 225*s15I + 2310*piI)
    return s15I*num/br

eps0 = 0.05; C = 0.1
S1 = box(float(mp.sqrt(mp.pi**2 - eps0)), float(mp.pi))
S2 = box(float(mp.sqrt(4*mp.pi**2 - eps0)), float(2*mp.pi))
Nb, Ne = 57, 2
b_edges = [a0f + (0.99-a0f)*i/Nb for i in range(Nb+1)]
nfail = 0; worst = None; min_margin_lo = mp.mpf("inf"); min_margin_hi = mp.mpf("inf")
for j in range(Nb):
    for kk in range(Ne):
        b_cell = box(b_edges[j], b_edges[j+1])
        e_cell = box(eps0*kk/Ne, eps0*(kk+1)/Ne)
        Rc = 1 + e_cell
        phi_c = phi_iv(b_cell)
        a_lo = a0I + e_cell*phi_c - C*e_cell**2
        a_hi = a0I + e_cell*phi_c + C*e_cell**2
        # R1 at the endpoints over the cell
        R1lo = R1_f(S1, S2, a_lo, b_cell, Rc)
        R1hi = R1_f(S1, S2, a_hi, b_cell, Rc)
        ok_lo = mp.mpf(R1lo.b) < 0
        ok_hi = mp.mpf(R1hi.a) > 0
        if not (ok_lo and ok_hi):
            nfail += 1
            if worst is None:
                worst = dict(j=j, k=kk, b=[float(mp.mpf(b_cell.a)), float(mp.mpf(b_cell.b))],
                             e=[float(mp.mpf(e_cell.a)), float(mp.mpf(e_cell.b))],
                             R1lo=[float(mp.mpf(R1lo.a)), float(mp.mpf(R1lo.b))],
                             R1hi=[float(mp.mpf(R1hi.a)), float(mp.mpf(R1hi.b))])
        min_margin_lo = min(min_margin_lo, -mp.mpf(R1lo.b))
        min_margin_hi = min(min_margin_hi, mp.mpf(R1hi.a))
status = "PASS" if nfail == 0 else "FAIL"
print("status=%s  nfail=%d  min -R1(a_lo)=%.4e  min R1(a_hi)=%.4e" %
      (status, nfail, float(min_margin_lo), float(min_margin_hi)))
if worst: print("worst:", worst)
out = dict(status=status, eps0=eps0, C_sheet=C, nfail=nfail, worst_cell=worst,
           min_margin_lo=float(min_margin_lo), min_margin_hi=float(min_margin_hi),
           runtime_s=round(time.time()-t0, 1),
           note="sign-change at a0+e*phi+-C*e^2 over (b,eps) cells; FH root enclosures; R1_a>0 certified => root in (a_lo,a_hi)")
with open(os.path.join(HERE, "cert_sheet_error.json"), "w") as f:
    json.dump(out, f, indent=1)
print("written cert_sheet_error.json, runtime=%.1fs" % (time.time()-t0))
