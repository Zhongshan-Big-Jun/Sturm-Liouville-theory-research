# -*- coding: utf-8 -*-
"""scan_s22_sp3.py - numeric scan of s22 and s2''' over the box (true ranges)."""
import numpy as np, mpmath as mp, sympy as sp, pickle, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = pickle.load(open(os.path.join(HERE, "pert_coeffs.pkl"), "rb"))
d3 = pickle.load(open(os.path.join(HERE, "s3_bounds.pkl"), "rb"))
a_s, b_s = sp.symbols("a b")
f22 = sp.lambdify((a_s, b_s), sp.sympify(d["s22"]), "numpy")
s_sym, a_s2, b_s2, R_s2 = sp.symbols("s a b R")
fsp3 = sp.lambdify((s_sym, a_s2, b_s2, R_s2), sp.sympify(d3["sp3"]), "numpy")
a0 = float(np.arccos(0.25)/np.pi)
aa = np.linspace(a0-0.03, a0+0.03, 101); bb = np.linspace(a0, 0.99, 501)
A, B = np.meshgrid(aa, bb, indexing="ij")
S22 = np.abs(f22(A, B))
print("true max|s22| over box: %.6f at a=%.4f b=%.4f" % (S22.max(), aa[np.unravel_index(S22.argmax(), S22.shape)[0]], bb[np.unravel_index(S22.argmax(), S22.shape)[1]]))
# sp3 over s in [2pi-0.5, 2pi+0.5], a,b box, R in [1,1.05]
ss = np.linspace(2*np.pi-0.5, 2*np.pi+0.5, 51)
RR = np.linspace(1.0, 1.05, 6)
mx = 0; loc = None
for ai in range(0, 101, 10):
    for bi in range(0, 501, 25):
        for si in range(0, 51, 5):
            for ri in range(6):
                v = abs(fsp3(ss[si], aa[ai], bb[bi], RR[ri]))
                if v > mx: mx = v; loc = (aa[ai], bb[bi], ss[si], RR[ri])
print("true max|s2'''| over [2pi-0.5,2pi+0.5]xboxxR: %.6f at (a,b,s,R)=%s" % (mx, tuple(round(x,4) for x in loc)))
# also s1''':
mx1 = 0
for ai in range(0, 101, 10):
    for bi in range(0, 501, 25):
        for si in range(0, 51, 5):
            for ri in range(6):
                v = abs(fsp3(np.pi-0.5+si*0.02, aa[ai], bb[bi], RR[ri]))
                if v > mx1: mx1 = v
print("true max|s1'''| (scan): %.6f" % mx1)
# s21 true max
f21 = sp.lambdify((a_s, b_s), sp.sympify(d["s21"]), "numpy")
S21 = np.abs(f21(A, B))
print("true max|s21|: %.6f" % S21.max())
