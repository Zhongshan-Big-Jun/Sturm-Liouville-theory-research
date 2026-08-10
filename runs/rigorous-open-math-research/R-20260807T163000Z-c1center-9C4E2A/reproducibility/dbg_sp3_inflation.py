# -*- coding: utf-8 -*-
"""dbg_sp3_inflation.py - locate the cells where sp3's interval evaluation inflates."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = pickle.load(open(os.path.join(HERE, "s3_bounds.pkl"), "rb"))
s_sym, a_s, b_s, R_s = sp.symbols("s a b R")
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt, "mpf": iv.mpf, "pi": iv.pi}, "mpmath"]
sp3_f = sp.lambdify((s_sym, a_s, b_s, R_s), sp.sympify(d["sp3"]), modules=mods)
def box(lo, hi): return iv.mpf([mp.mpf(lo), mp.mpf(hi)])
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
# grid over representative cells (k=2): report interval upper bound
for (al, ah, bl, bh) in [(a0f-0.03, a0f-0.025, a0f, a0f+0.01), (a0f+0.025, a0f+0.03, 0.42, 0.43),
                         (a0f, a0f+0.005, 0.5, 0.51), (a0f, a0f+0.005, 0.7, 0.71),
                         (a0f+0.025, a0f+0.03, 0.95, 0.96), (a0f+0.025, a0f+0.03, 0.98, 0.99),
                         (a0f-0.005, a0f, 0.96, 0.97)]:
    A = box(al, ah); B = box(bl, bh); R = box(1.0, 1.025); S = box(6.28-0.05, 6.28+0.05)
    v = sp3_f(S, A, B, R)
    print("a=[%.4f,%.4f] b=[%.4f,%.4f]: sp3=[%.3f, %.3f] width=%.2f" %
          (al, ah, bl, bh, mp.mpf(v.a), mp.mpf(v.b), mp.mpf(v.b)-mp.mpf(v.a)))
    # point samples within the cell
    import numpy as np
    pts = []
    for ai in np.linspace(al, ah, 3):
        for bi in np.linspace(bl, bh, 3):
            for ri in (1.0, 1.025):
                pts.append(abs(float(v if False else None)) if False else None)
    # quick numeric with numpy version
    import numpy as np
    s_sym2, a_s2, b_s2, R_s2 = sp.symbols("s a b R")
    sp3n = sp.lambdify((s_sym2, a_s2, b_s2, R_s2), sp.sympify(d["sp3"]), "numpy")
    vals = np.abs(sp3n(6.28, np.linspace(al, ah, 5)[:,None,None], np.linspace(bl, bh, 5)[None,:,None], np.linspace(1.0, 1.025, 3)[None,None,:]))
    print("    numeric max|sp3| in cell: %.3f" % vals.max())
