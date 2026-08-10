# -*- coding: utf-8 -*-
"""cert_R1a_v2.py - CERTIFIED pipeline for the R->1+ main box:
Phase A: root-enclosure constants for s1, s2 on
  a in [a0-0.03,a0+0.03], b in [a0,0.99], R in [1,1+eps0]:
   (A1) F_s != 0 on s in [k*pi-0.5, k*pi+0.5] x cells (IFT regularity);
   (A2) C_k = sup|sp3|/6 (Taylor remainder |s_k - T2| <= C_k eps^3);
   (A3) consistency max|s_k - k*pi| < 0.5 (curve stays in the certified range).
Phase B: R1_a > 0 on the main box via cell-wise interval evaluation with the
  certified enclosures S_k = k*pi + s_k1 eps + s_k2 eps^2 +- C_k eps^3.
Output: cert_R1a_v2.json (ASCII)."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()

d = pickle.load(open(os.path.join(HERE, "s3_bounds.pkl"), "rb"))
d2 = pickle.load(open(os.path.join(HERE, "pert_coeffs.pkl"), "rb"))
d3 = pickle.load(open(os.path.join(HERE, "R1_partials_exprs.pkl"), "rb"))
s_sym, a_s, b_s, R_s = sp.symbols("s a b R")
s1s, s2s = sp.symbols("s1 s2")
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
sp3_f = sp.lambdify((s_sym, a_s, b_s, R_s), sp.sympify(d["sp3"]), modules=mods)
coefs = {}
for k in ("s11", "s12", "s21", "s22"):
    coefs[k] = sp.lambdify((a_s, b_s), sp.sympify(d2[k]), modules=mods)
def fix_pow(expr):
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(1, 2), lambda t: sp.sqrt(t.base))
    expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(-1, 2), lambda t: 1/sp.sqrt(t.base))
    return expr
R1a_f = sp.lambdify((s1s, s2s, a_s, b_s, R_s), fix_pow(sp.sympify(d3["R1_a"])), modules=mods)

def F_iv(s, a, b, R):
    m = iv.sqrt(R)
    ca, sa = iv.cos(s*a), iv.sin(s*a)
    cb, sb = iv.cos(s*(1-b)), iv.sin(s*(1-b))
    ct, st = iv.cos(s*m*(b-a)), iv.sin(s*m*(b-a))
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca
def Fs_iv(s, a, b, R):
    from cert_lib import Fs_iv as Fs_ref
    return Fs_ref(s, a, b, R)
def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
piI = iv.pi
eps0 = 0.05
a_iv = box(a0f-0.03, a0f+0.03)
R_iv = box(1.0, 1+eps0)
Nb = 57
b_edges = [a0f + (0.99-a0f)*i/Nb for i in range(Nb+1)]

# ---------- Phase A ----------
print("Phase A: root-enclosure constants", flush=True)
resA = {}
for k in (1, 2):
    c0 = float(k*mp.pi)
    Ck = mp.mpf("0")
    Fs_ok = True
    M1 = mp.mpf("0"); M2 = mp.mpf("0")
    Ns = 20
    for jb in range(Nb):
        b_cell = box(b_edges[jb], b_edges[jb+1])
        # M1, M2 over the a,b cell
        for jj in (0,):
            v1 = coefs["s%d1" % k](a_iv, b_cell); v2 = coefs["s%d2" % k](a_iv, b_cell)
            M1 = max(M1, max(abs(mp.mpf(v1.a)), abs(mp.mpf(v1.b))))
            M2 = max(M2, max(abs(mp.mpf(v2.a)), abs(mp.mpf(v2.b))))
        for js in range(Ns):
            S = box(c0-0.5+js*1.0/Ns, c0-0.5+(js+1)*1.0/Ns)
            Fs = Fs_iv(S, a_iv, b_cell, R_iv)
            if not (Fs.a > 0 or Fs.b < 0):
                Fs_ok = False
            v = sp3_f(S, a_iv, b_cell, R_iv)
            w = iv.fabs(v)/6
            if mp.mpf(w.b) > Ck: Ck = mp.mpf(w.b)
    dev = (M1 + M2*eps0 + Ck*eps0**2)*eps0
    resA[k] = dict(Fs_excl0=bool(Fs_ok), Ck=float(Ck), M1=float(M1), M2=float(M2), dev=float(dev), ok=bool(Fs_ok and dev < 0.5))
    print("  k=%d  Fs_excl0=%s  C_k=%.5f  M1=%.4f  M2=%.4f  dev=%.4f  ok=%s"
          % (k, resA[k]["Fs_excl0"], resA[k]["Ck"], resA[k]["M1"], resA[k]["M2"], resA[k]["dev"], resA[k]["ok"]), flush=True)

A_ok = all(resA[k]["ok"] for k in (1, 2))
print("Phase A status:", "PASS" if A_ok else "FAIL", flush=True)

# ---------- Phase B ----------
print("Phase B: R1_a > 0 on main box", flush=True)
Na, Ne = 12, 2
C1, C2 = resA[1]["Ck"], resA[2]["Ck"]
min_lb = mp.mpf("inf"); worst = None; nfail = 0; nf_info = None
for i in range(Na):
    for j in range(Nb):
        for kk in range(Ne):
            a_cell = box(a0f-0.03+0.06*i/Na, a0f-0.03+0.06*(i+1)/Na)
            b_cell = box(b_edges[j], b_edges[j+1])
            e_cell = box(eps0*kk/Ne, eps0*(kk+1)/Ne)
            Rc = 1 + e_cell
            S1 = piI + coefs["s11"](a_cell, b_cell)*e_cell + coefs["s12"](a_cell, b_cell)*e_cell**2 + box(-C1, C1)*e_cell**3
            S2 = 2*piI + coefs["s21"](a_cell, b_cell)*e_cell + coefs["s22"](a_cell, b_cell)*e_cell**2 + box(-C2, C2)*e_cell**3
            # soundness spot-check: F contains 0 on the enclosures
            F1 = F_iv(S1, a_cell, b_cell, Rc); F2 = F_iv(S2, a_cell, b_cell, Rc)
            Fs1 = Fs_iv(S1, a_cell, b_cell, Rc); Fs2 = Fs_iv(S2, a_cell, b_cell, Rc)
            if not ((F1.a < 0 < F1.b) and (F2.a < 0 < F2.b) and (Fs1.a > 0 or Fs1.b < 0) and (Fs2.a > 0 or Fs2.b < 0)):
                nfail += 1
                if nf_info is None:
                    nf_info = dict(i=i, j=j, k=kk, F1=[float(mp.mpf(F1.a)), float(mp.mpf(F1.b))],
                                   F2=[float(mp.mpf(F2.a)), float(mp.mpf(F2.b))],
                                   Fs1=[float(mp.mpf(Fs1.a)), float(mp.mpf(Fs1.b))],
                                   Fs2=[float(mp.mpf(Fs2.a)), float(mp.mpf(Fs2.b))])
                continue
            R1a = R1a_f(S1, S2, a_cell, b_cell, Rc)
            lb = mp.mpf(R1a.a)
            if lb < min_lb:
                min_lb = lb
                worst = dict(i=i, j=j, k=kk, a=[float(mp.mpf(a_cell.a)), float(mp.mpf(a_cell.b))],
                             b=[float(mp.mpf(b_cell.a)), float(mp.mpf(b_cell.b))],
                             e=[float(mp.mpf(e_cell.a)), float(mp.mpf(e_cell.b))],
                             lb=float(lb), ub=float(mp.mpf(R1a.b)))
B_ok = (nfail == 0 and min_lb > 0)
print("Phase B: nfail=%d  min_R1a_lb=%.4f  status=%s" % (nfail, float(min_lb), "PASS" if B_ok else "FAIL"), flush=True)
if worst: print("worst cell:", worst)

out = dict(status="PASS" if (A_ok and B_ok) else "FAIL", eps0=eps0,
           phaseA=resA, phaseB=dict(nfail=nfail, min_R1a_lb=float(min_lb), worst_cell=worst),
           runtime_s=round(time.time()-t0, 1),
           note="mpmath.iv 200-bit; C_k certified Taylor remainder; root enclosures valid via IFT+Taylor; R1_a evaluated cell-wise")
with open(os.path.join(HERE, "cert_R1a_v2.json"), "w") as f:
    json.dump(out, f, indent=1)
print("written cert_R1a_v2.json, runtime=%.1fs" % (time.time()-t0))
