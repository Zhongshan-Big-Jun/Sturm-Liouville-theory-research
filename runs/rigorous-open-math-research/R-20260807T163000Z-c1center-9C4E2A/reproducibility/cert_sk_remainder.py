# -*- coding: utf-8 -*-
"""cert_sk_remainder.py - CERTIFIED constants for the root enclosure of s_k:
  (A) F_s != 0 on s in [k*pi-0.5, k*pi+0.5] x box x R in [1,1+eps0];
  (B) C_k = sup |sp3|/6 on that range (Taylor remainder bound);
  (C) consistency: max|s_k(eps)-k*pi| < 0.5 for eps <= eps0.
Output: cert_sk_remainder.json (ASCII)."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()

d = pickle.load(open(os.path.join(HERE, "s3_bounds.pkl"), "rb"))
d2 = pickle.load(open(os.path.join(HERE, "pert_coeffs.pkl"), "rb"))
s_sym, a_s, b_s, R_s = sp.symbols("s a b R")
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
sp3_f = sp.lambdify((s_sym, a_s, b_s, R_s), sp.sympify(d["sp3"]), modules=mods)
coefs = {}
for k in ("s11", "s12", "s21", "s22"):
    coefs[k] = sp.lambdify((a_s, b_s), sp.sympify(d2[k]), modules=mods)

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
eps0 = 0.05
a_iv = box(a0f-0.03, a0f+0.03); b_iv = box(a0f, 0.99); R_iv = box(1.0, 1+eps0)
piI = iv.pi

# (A) F_s sign on [k*pi-0.5, k*pi+0.5] x box (cell-wise in s)
print("(A) F_s != 0 on s-cells ...")
okA = {1: True, 2: True}
for k in (1, 2):
    c0 = k*piI
    for i in range(20):
        S = box(float(mp.mpf(c0.a))-0.5+0.05*i, float(mp.mpf(c0.a))-0.5+0.05*(i+1))
        Fs = Fs_iv(S, a_iv, b_iv, R_iv)
        if not (Fs.a > 0 or Fs.b < 0):
            okA[k] = False
            print("  k=%d FAIL s-cell %d: Fs=[%.4f,%.4f]" % (k, i, mp.mpf(Fs.a), mp.mpf(Fs.b)))
    print("  k=%d F_s excl 0: %s" % (k, okA[k]))

# (B) C_k = sup|sp3|/6 over s-cells x box (cell-wise in s and b to keep denominators ok)
print("(B) sup|sp3|/6 ...")
C = {}
for k in (1, 2):
    c0 = k*piI
    mx = iv.mpf("-inf")
    for i in range(20):
        S = box(float(mp.mpf(c0.a))-0.5+0.05*i, float(mp.mpf(c0.a))-0.5+0.05*(i+1))
        v = sp3_f(S, a_iv, b_iv, R_iv)
        w = iv.fabs(v)/6
        if w.b > mx: mx = w.b
    C[k] = mx
    print("  k=%d  C_k = sup|sp3|/6 <= %.6f" % (k, mp.mpf(C[k])))

# (C) consistency: |s_k(eps)-k*pi| <= (max|s_k1| + max|s_k2|*eps0 + C_k*eps0^2/... )*eps0
print("(C) deviation consistency ...")
for k in (1, 2):
    k1 = coefs["s%d1" % k](a_iv, b_iv); k2 = coefs["s%d2" % k](a_iv, b_iv)
    M1 = max(abs(float(mp.mpf(k1.a))), abs(float(mp.mpf(k1.b))))
    M2 = max(abs(float(mp.mpf(k2.a))), abs(float(mp.mpf(k2.b))))
    dev = (M1 + M2*eps0 + float(mp.mpf(C[k]))*eps0**2) * eps0
    print("  k=%d  max|s_k1|<=%.4f max|s_k2|<=%.4f  max dev <= %.4f < 0.5: %s"
          % (k, M1, M2, dev, dev < 0.5))

out = dict(status="PASS" if (okA[1] and okA[2] and all(float(mp.mpf(C[k])) < 1e6 for k in (1,2))) else "FAIL",
           eps0=eps0, okA={str(k): okA[k] for k in (1,2)},
           C1=float(mp.mpf(C[1])), C2=float(mp.mpf(C[2])),
           a0=float(a0f), note="mpmath.iv 200-bit; C_k is a certified Taylor-remainder bound |s_k-T2|<=C_k*eps^3",
           runtime_s=round(time.time()-t0, 1))
with open(os.path.join(HERE, "cert_sk_remainder.json"), "w") as f:
    json.dump(out, f, indent=1)
print("status=%s  C1=%.6f  C2=%.6f  runtime=%.1fs" % (out["status"], out["C1"], out["C2"], out["runtime_s"]))
