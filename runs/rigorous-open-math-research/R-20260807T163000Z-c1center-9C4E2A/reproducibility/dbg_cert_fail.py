# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = pickle.load(open(os.path.join(HERE, "pert_coeffs.pkl"), "rb"))
a_s, b_s = sp.symbols("a b")
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
coefs = {}
for k in ("s11", "s12", "s21", "s22"):
    coefs[k] = sp.lambdify((a_s, b_s), sp.sympify(d[k]), modules=mods)
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
def sk_brackets(k, a_iv, b_iv, e_iv, C):
    k1 = coefs["s%d1" % k](a_iv, b_iv)
    k2 = coefs["s%d2" % k](a_iv, b_iv)
    base = k*piI + k1*e_iv + k2*e_iv**2
    w = C*e_iv**3
    return base - w, base + w
a_iv = box(a0f-0.03, a0f+0.03-0.005)
b_iv = box(a0f, a0f+0.01)
e_iv = box(0.0, 0.025)
R_iv = 1 + e_iv
S1m, S1p = sk_brackets(1, a_iv, b_iv, e_iv, 60.0)
S2m, S2p = sk_brackets(2, a_iv, b_iv, e_iv, 120.0)
print("S1m=[%.6f,%.6f] S1p=[%.6f,%.6f]" % (mp.mpf(S1m.a), mp.mpf(S1m.b), mp.mpf(S1p.a), mp.mpf(S1p.b)))
print("S2m=[%.6f,%.6f] S2p=[%.6f,%.6f]" % (mp.mpf(S2m.a), mp.mpf(S2m.b), mp.mpf(S2p.a), mp.mpf(S2p.b)))
S1 = iv.mpf([S1m.a, S1p.b]); S2 = iv.mpf([S2m.a, S2p.b])
print("S1 width:", mp.mpf(S1.b)-mp.mpf(S1.a), " S2 width:", mp.mpf(S2.b)-mp.mpf(S2.a))
Fs1 = Fs_iv(S1, a_iv, b_iv, R_iv); Fs2 = Fs_iv(S2, a_iv, b_iv, R_iv)
print("Fs1=[%.4f,%.4f] excl0: %s   Fs2=[%.4f,%.4f] excl0: %s" %
      (mp.mpf(Fs1.a), mp.mpf(Fs1.b), Fs1.a > 0 or Fs1.b < 0, mp.mpf(Fs2.a), mp.mpf(Fs2.b), Fs2.a > 0 or Fs2.b < 0))
F1m = F_iv(S1m, a_iv, b_iv, R_iv); F1p = F_iv(S1p, a_iv, b_iv, R_iv)
F2m = F_iv(S2m, a_iv, b_iv, R_iv); F2p = F_iv(S2p, a_iv, b_iv, R_iv)
print("F1m=[%.4e,%.4e] F1p=[%.4e,%.4e]  bracket: %s" %
      (mp.mpf(F1m.a), mp.mpf(F1m.b), mp.mpf(F1p.a), mp.mpf(F1p.b), (F1m.b < 0 < F1p.a) or (F1p.b < 0 < F1m.a)))
print("F2m=[%.4e,%.4e] F2p=[%.4e,%.4e]  bracket: %s" %
      (mp.mpf(F2m.a), mp.mpf(F2m.b), mp.mpf(F2p.a), mp.mpf(F2p.b), (F2m.b < 0 < F2p.a) or (F2p.b < 0 < F2m.a)))
