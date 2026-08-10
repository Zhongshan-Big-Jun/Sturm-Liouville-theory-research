# -*- coding: utf-8 -*-
"""cert_R1a_mainbox.py - CERTIFIED: R1_a > 0 on the main box
  a in [a0-0.03, a0+0.03], b in [a0, 0.99], eps in [0, eps0].
Method: cell-wise interval evaluation.  Root enclosures S_k via the exact
2nd-order perturbation s_k(eps) = k*pi + s_k1(a,b) eps + s_k2(a,b) eps^2 +-
C_k eps^3, validated cell-wise by the secular bracketing test:
  (i) F_s keeps sign on S_k (monotonicity),
  (ii) F(S_k^-) and F(S_k^+) have opposite signs (root in S_k for every
       parameter point of the cell).
Then R1_a(S1,S2,a,b,R) over the cell is a sound enclosure; we record the min
lower bound.  Output: cert_R1a_mainbox.json (ASCII).  [CERTIFIED]
Runtime note: 12 x 57 x ne cells, each ~4 iv evaluations of trig-heavy exprs."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()

d = pickle.load(open(os.path.join(HERE, "pert_coeffs.pkl"), "rb"))
a_s, b_s = sp.symbols("a b")
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
coefs = {}
for k in ("s11", "s12", "s21", "s22"):
    coefs[k] = sp.lambdify((a_s, b_s), sp.sympify(d[k]), modules=mods)

d2 = pickle.load(open(os.path.join(HERE, "R1_partials_exprs.pkl"), "rb"))
s1s, s2s, R_s = sp.symbols("s1 s2 R")
def fix_pow(expr):
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(1, 2), lambda t: sp.sqrt(t.base))
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(-1, 2), lambda t: 1/sp.sqrt(t.base))
    return expr
R1a_f = sp.lambdify((s1s, s2s, a_s, b_s, R_s), fix_pow(sp.sympify(d2["R1_a"])), modules=mods)

def F_iv(s, a, b, R):
    m = iv.sqrt(R)
    ca, sa = iv.cos(s*a), iv.sin(s*a)
    cb, sb = iv.cos(s*(1-b)), iv.sin(s*(1-b))
    ct, st = iv.cos(s*m*(b-a)), iv.sin(s*m*(b-a))
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca
def Fs_iv(s, a, b, R):
    from cert_lib import Fs_iv as Fs_ref
    return Fs_ref(s, a, b, R)

piI = iv.pi
def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
a0I = iv.atan2(iv.sqrt(15)/4, iv.mpf(1)/4)/piI

def sk_brackets(k, a_iv, b_iv, e_iv, C):
    k1 = coefs["s%d1" % k](a_iv, b_iv)
    k2 = coefs["s%d2" % k](a_iv, b_iv)
    base = k*piI + k1*e_iv + k2*e_iv**2
    w = C*e_iv**3
    return base - w, base + w

def cell_check(a_iv, b_iv, e_iv, C1, C2):
    """return (ok, min_R1a_lb, info) - ok if brackets valid and R1_a evaluated."""
    R_iv = 1 + e_iv
    S1m, S1p = sk_brackets(1, a_iv, b_iv, e_iv, C1)
    S2m, S2p = sk_brackets(2, a_iv, b_iv, e_iv, C2)
    S1 = iv.mpf([S1m.a, S1p.b]); S2 = iv.mpf([S2m.a, S2p.b])
    Fs1 = Fs_iv(S1, a_iv, b_iv, R_iv); Fs2 = Fs_iv(S2, a_iv, b_iv, R_iv)
    ok1s = Fs1.a > 0 or Fs1.b < 0
    ok2s = Fs2.a > 0 or Fs2.b < 0
    F1m = F_iv(S1m, a_iv, b_iv, R_iv); F1p = F_iv(S1p, a_iv, b_iv, R_iv)
    F2m = F_iv(S2m, a_iv, b_iv, R_iv); F2p = F_iv(S2p, a_iv, b_iv, R_iv)
    ok1b = (F1m.b < 0 < F1p.a) or (F1p.b < 0 < F1m.a)
    ok2b = (F2m.b < 0 < F2p.a) or (F2p.b < 0 < F2m.a)
    if not (ok1s and ok2s and ok1b and ok2b):
        return False, None, dict(ok1s=ok1s, ok2s=ok2s, ok1b=ok1b, ok2b=ok2b)
    R1a = R1a_f(S1, S2, a_iv, b_iv, R_iv)
    return True, mp.mpf(R1a.a), dict(lb=mp.mpf(R1a.a), ub=mp.mpf(R1a.b))

# grid
eps0 = 0.05
Na, Nb, Ne = 12, 57, 2   # a-cell 0.005, b-cell 0.01, eps-cell 0.025
C1, C2 = 60.0, 120.0
a_lo, a_hi = a0f-0.03, a0f+0.03
b_lo, b_hi = a0f, 0.99
min_lb = mp.mpf("inf")
worst = None
nfail = 0
nfail_info = None
total = Na*Nb*Ne
done = 0
for i in range(Na):
    for j in range(Nb):
        for k in range(Ne):
            a_iv = box(a_lo + (a_hi-a_lo)*i/Na, a_lo + (a_hi-a_lo)*(i+1)/Na)
            b_iv = box(b_lo + (b_hi-b_lo)*j/Nb, b_lo + (b_hi-b_lo)*(j+1)/Nb)
            e_iv = box(eps0*k/Ne, eps0*(k+1)/Ne)
            ok, lb, info = cell_check(a_iv, b_iv, e_iv, C1, C2)
            done += 1
            if not ok:
                nfail += 1
                if nfail_info is None:
                    nfail_info = dict(i=i, j=j, k=k, a=[float(mp.mpf(a_iv.a)), float(mp.mpf(a_iv.b))],
                                      b=[float(mp.mpf(b_iv.a)), float(mp.mpf(b_iv.b))],
                                      e=[float(mp.mpf(e_iv.a)), float(mp.mpf(e_iv.b))], info=str(info))
            else:
                if lb < min_lb:
                    min_lb = lb
                    worst = dict(i=i, j=j, k=k, a=[float(mp.mpf(a_iv.a)), float(mp.mpf(a_iv.b))],
                                 b=[float(mp.mpf(b_iv.a)), float(mp.mpf(b_iv.b))],
                                 e=[float(mp.mpf(e_iv.a)), float(mp.mpf(e_iv.b))], lb=float(lb), ub=float(info["ub"]))

out = dict(
    status="PASS" if nfail == 0 and min_lb > 0 else "FAIL",
    a0=float(a0f), eps0=eps0, Na=Na, Nb=Nb, Ne=Ne, C1=C1, C2=C2,
    min_R1a_lb=float(min_lb), worst_cell=worst, nfail=nfail, nfail_info=nfail_info,
    cells=total, runtime_s=round(time.time()-t0, 1),
    note="interval arithmetic mpmath.iv 200-bit; root enclosures validated by secular bracketing per cell")
with open(os.path.join(HERE, "cert_R1a_mainbox.json"), "w") as f:
    json.dump(out, f, indent=1)
print("status=%s  min_R1a_lb=%.4f  nfail=%d  cells=%d  runtime=%.1fs"
      % (out["status"], out["min_R1a_lb"], nfail, total, out["runtime_s"]))
if worst: print("worst cell:", worst)
