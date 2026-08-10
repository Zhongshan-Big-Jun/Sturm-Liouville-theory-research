# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
d = pickle.load(open(os.path.join(HERE, "s3_bounds.pkl"), "rb"))
s_sym, a_s, b_s, R_s = sp.symbols("s a b R")
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
sp3_f = sp.lambdify((s_sym, a_s, b_s, R_s), sp.sympify(d["sp3"]), modules=mods)
def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
# time 100 evals on a medium cell
S = box(3.14-0.05, 3.14+0.05); A = box(a0f-0.005, a0f+0.005); B = box(0.5, 0.51); R = box(1.0, 1.025)
t0 = time.time()
for _ in range(50):
    v = sp3_f(S, A, B, R)
print("50 evals: %.2fs -> per eval %.1f ms" % (time.time()-t0, (time.time()-t0)*1000/50))
print("value:", mp.nstr(v, 8))
