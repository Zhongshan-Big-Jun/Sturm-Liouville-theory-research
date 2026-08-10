# -*- coding: utf-8 -*-
"""dbg_Adash_sheet.py - A'(b) on the true sheet at b=0.99, eps=0.05 (EVIDENCE)."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
import mpmath as mp
mp.mp.dps = 40
a0 = float(np.arccos(0.25)/np.pi)
eps = 0.05
# sheet a = A(b) via Newton (continue)
def solve_a(b, a_guess):
    a = a_guess
    for _ in range(100):
        fa = R1R2(a, b, 1+eps)[0]
        if abs(fa) < 1e-13: break
        h = 1e-6
        d = (R1R2(a+h, b, 1+eps)[0]-R1R2(a-h, b, 1+eps)[0])/(2*h)
        if abs(d) < 1e-9: break
        an = a - fa/d
        if not (0 < an < b): break
        a = an
    return a
a_prev = a0
for b in np.linspace(a0+0.001, 0.99, 50):
    a_prev = solve_a(b, a_prev)
print("eps=0.05 sheet at b=0.99: a=%.8f" % a_prev)
# A'(0.99) via FD on the sheet
db = 1e-6
a_p = solve_a(0.99+db, a_prev); a_m = solve_a(0.99-db, a_prev)
Ap = (a_p - a_m)/(2*db)
print("A'(0.99) ~ %.6f   (eps*phi'(0.99) = %.6f)" % (Ap, eps*9.576e-4))
# also at b=0.9, 0.7
a_prev = a0
for b in np.linspace(a0+0.001, 0.9, 40):
    a_prev = solve_a(b, a_prev)
a_p = solve_a(0.9+db, a_prev); a_m = solve_a(0.9-db, a_prev)
print("A'(0.9) ~ %.6f   (eps*phi'(0.9) = %.6f)" % ((a_p-a_m)/(2*db), eps*np.interp(0.9, [0.4196,1.0], [0.4288,0.0])))
# R1_b / R1_a on the sheet at b=0.99
def R1b(a, b): return (R1R2(a, b+1e-6, 1+eps)[0]-R1R2(a, b-1e-6, 1+eps)[0])/(2e-6)
def R1a(a, b): return (R1R2(a+1e-6, b, 1+eps)[0]-R1R2(a-1e-6, b, 1+eps)[0])/(2e-6)
print("R1_b=%.4f R1_a=%.2f  -R1_b/R1_a=%.6f" % (R1b(a_prev, 0.9), R1a(a_prev, 0.9), -R1b(a_prev,0.9)/R1a(a_prev,0.9)))
