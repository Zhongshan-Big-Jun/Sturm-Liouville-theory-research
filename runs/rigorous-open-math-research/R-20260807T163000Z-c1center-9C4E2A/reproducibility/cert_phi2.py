# -*- coding: utf-8 -*-
"""cert_phi2.py - CERTIFIED: interval bounds for the second-order constants
  D0 = max|R1^1|, W0 = max|R1^2| on the box [a0-0.03,a0+0.03] x [a0,1];
  max|phi_2|, max|phi_2'| and the ratio phi_2'/phi' on b in [a0, 0.999].
Uses the factored closed forms (R1_eps_coeffs.pkl, phi2_closed.pkl) with
mpmath.iv 200-bit cell-wise interval evaluation.
FIX 2026-08-09 (F-022): the constant atan(sqrt(15)) = pi*a0 inside the
pickled phi_2 expressions is not evaluable by mpmath.iv (no single-arg
atan); it is replaced by a dedicated symbol CAT15 passed as an argument
with the iv value atan2(sqrt(15), 1).  Output: cert_phi2.json (ASCII)."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()

dc = pickle.load(open(os.path.join(HERE, "R1_eps_coeffs.pkl"), "rb"))
R11 = sp.sympify(dc["R11"]); R12 = sp.sympify(dc["R12"])
d2 = pickle.load(open(os.path.join(HERE, "phi2_closed.pkl"), "rb"))
phi2 = sp.sympify(d2["phi2"]); phi2p = sp.sympify(d2["phi2p"])
CAT15 = sp.Symbol("CAT15")
phi2 = phi2.replace(sp.atan(sp.sqrt(15)), CAT15)
phi2p = phi2p.replace(sp.atan(sp.sqrt(15)), CAT15)
ab = sorted(R11.free_symbols | R12.free_symbols, key=str)
b_only = sorted((phi2.free_symbols | phi2p.free_symbols) - {CAT15}, key=str)
print("symbols: R11/R12:", ab, " phi2:", b_only, flush=True)

mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
fR11 = sp.lambdify((ab[0], ab[1]), R11, modules=mods)
fR12 = sp.lambdify((ab[0], ab[1]), R12, modules=mods)
b_sym = b_only[0]
fphi2 = sp.lambdify((b_sym, CAT15), phi2, modules=mods)
fphi2p = sp.lambdify((b_sym, CAT15), phi2p, modules=mods)
print("lambdified %.1fs" % (time.time()-t0), flush=True)

def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
piI = iv.pi
s15I = iv.sqrt(15)
a0I = iv.atan2(s15I/4, iv.mpf(1)/4)/piI
CAT = iv.atan2(s15I, iv.mpf(1))
print("CAT15 interval:", CAT, flush=True)

def dphi_iv(b):
    u = iv.cos(2*piI*b); v = iv.sin(2*piI*b)
    N = (56*piI*a0I - 6*s15I)*u**2 + (2*piI*a0I + 3*s15I)*u + (3*s15I - 58*piI*a0I) + 2*s15I*piI*(1-b)*(1-4*u)*v
    return -N/(60*piI)

# ---- D0, W0 over the box ----
Da = 0.03
Na, Nb = 10, 60
maxD0 = mp.mpf(0); maxW0 = mp.mpf(0); worstD0 = worstW0 = None
a_edges = [a0f-Da + 2*Da*i/Na for i in range(Na+1)]
b_edges = [a0f + (1.0-a0f)*i/Nb for i in range(Nb+1)]
for i in range(Na):
    for j in range(Nb):
        ac = box(a_edges[i], a_edges[i+1]); bc = box(b_edges[j], b_edges[j+1])
        v1 = fR11(ac, bc); v2 = fR12(ac, bc)
        if not (mp.isfinite(mp.mpf(v1.a)) and mp.isfinite(mp.mpf(v1.b))):
            print("NONFINITE R11 at cell", i, j); continue
        m1 = max(abs(mp.mpf(v1.a)), abs(mp.mpf(v1.b)))
        m2 = max(abs(mp.mpf(v2.a)), abs(mp.mpf(v2.b)))
        if m1 > maxD0: maxD0 = m1; worstD0 = (i, j, float(mp.mpf(v1.a)), float(mp.mpf(v1.b)))
        if m2 > maxW0: maxW0 = m2; worstW0 = (i, j, float(mp.mpf(v2.a)), float(mp.mpf(v2.b)))
print("D0 = max|R1^1| <= %.4f" % float(maxD0), flush=True)
print("W0 = max|R1^2| <= %.4f" % float(maxW0), flush=True)

# ---- phi_2, phi_2', ratio on b in [a0, 0.999] ----
Nb2 = 80
b_edges2 = [a0f + (0.999-a0f)*i/Nb2 for i in range(Nb2+1)]
maxP2 = mp.mpf(0); maxP2p = mp.mpf(0); maxRatio = mp.mpf(0)
worstP2 = worstP2p = worstRatio = None
for j in range(Nb2):
    bc = box(b_edges2[j], b_edges2[j+1])
    p2 = fphi2(bc, CAT); p2p = fphi2p(bc, CAT); dp = dphi_iv(bc)
    m2_ = max(abs(mp.mpf(p2.a)), abs(mp.mpf(p2.b)))
    m2p = max(abs(mp.mpf(p2p.a)), abs(mp.mpf(p2p.b)))
    if mp.mpf(dp.a) > 0:
        rat = p2p/dp
        mr = max(abs(mp.mpf(rat.a)), abs(mp.mpf(rat.b)))
        if mr > maxRatio: maxRatio = mr; worstRatio = (j, float(mp.mpf(rat.a)), float(mp.mpf(rat.b)))
    if m2_ > maxP2: maxP2 = m2_; worstP2 = (j, float(mp.mpf(p2.a)), float(mp.mpf(p2.b)))
    if m2p > maxP2p: maxP2p = m2p; worstP2p = (j, float(mp.mpf(p2p.a)), float(mp.mpf(p2p.b)))
print("max|phi_2| <= %.6f" % float(maxP2), flush=True)
print("max|phi_2'| <= %.6f" % float(maxP2p), flush=True)
print("max|phi_2'/phi'| <= %.6f" % float(maxRatio), flush=True)

out = dict(status="PASS" if (maxD0 < 1e3 and maxW0 < 1e3 and maxP2p < 1.0 and maxRatio < 0.9) else "CHECK",
           D0_ub=float(maxD0), W0_ub=float(maxW0), max_phi2=float(maxP2), max_phi2p=float(maxP2p),
           max_ratio_0999=float(maxRatio), worstD0=worstD0, worstW0=worstW0,
           worstP2=worstP2, worstP2p=worstP2p, worstRatio=worstRatio,
           note="interval eval of factored closed forms, mpmath.iv 200-bit; atan(sqrt(15)) replaced by atan2 interval (F-022)",
           runtime_s=round(time.time()-t0, 1))
with open(os.path.join(HERE, "cert_phi2.json"), "w") as f:
    json.dump(out, f, indent=1)
print("written cert_phi2.json, runtime=%.1fs" % (time.time()-t0))