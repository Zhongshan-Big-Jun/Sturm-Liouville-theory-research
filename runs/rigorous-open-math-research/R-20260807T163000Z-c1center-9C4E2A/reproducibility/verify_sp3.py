# -*- coding: utf-8 -*-
"""verify_sp3.py - numeric check of sp3 (3rd eps-derivative of s_k) vs FD. [EVIDENCE]"""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os

HERE = os.path.dirname(os.path.abspath(__file__))
d = pickle.load(open(os.path.join(HERE, "s3_bounds.pkl"), "rb"))
s_sym, a_s, b_s, R_s = sp.symbols("s a b R")
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf}, "mpmath"]
sp3_f = sp.lambdify((s_sym, a_s, b_s, R_s), sp.sympify(d["sp3"]), modules=mods)

def sec_mp(s, a, b, eps):
    q = mp.sqrt(1+eps); al = s*a; be = s*(1-b); th = q*s*(b-a)
    return (mp.cos(be)*mp.cos(th)*mp.sin(al) - q*mp.sin(be)*mp.sin(th)*mp.sin(al)
            + (mp.cos(be)*mp.sin(th)/q)*mp.cos(al) + mp.sin(be)*mp.cos(th)*mp.cos(al))
def root_mp(k, a, b, eps):
    return mp.findroot(lambda s: sec_mp(s, a, b, eps), k*mp.pi, tol=1e-55, maxsteps=80)
def pt(x): return iv.mpf([mp.mpf(x), mp.mpf(x)])

mp.mp.dps = 60
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
print("FD check of sp3 at selected points:")
for (an, bn, en) in [(a0, 0.5, 0.01), (a0, 0.7, 0.05), (a0+0.01, 0.9, 0.02), (a0-0.02, 0.6, 0.04)]:
    am, bm, em = mp.mpf(an), mp.mpf(bn), mp.mpf(en)
    # numeric 3rd derivative of s_k(eps) at em via 5-point formula
    h = mp.mpf("1e-4")
    vals = []
    for j in (-2, -1, 0, 1, 2):
        vals.append(root_mp(1, am, bm, em + j*h))
    d3 = (vals[4] - 2*vals[3] + 2*vals[1] - vals[0])/(2*h**3)
    s1 = root_mp(1, am, bm, em)
    iv_v = sp3_f(pt(s1), pt(am), pt(bm), pt(1+em))
    mid = (mp.mpf(iv_v.a)+mp.mpf(iv_v.b))/2
    print("  (a=%.4f b=%.3f e=%.2f)  sp3=[%.5f, %.5f]  FD=%.5f  rel=%.2e"
          % (an, bn, en, mp.mpf(iv_v.a), mp.mpf(iv_v.b), d3, float(abs(mid-d3)/abs(d3))))
