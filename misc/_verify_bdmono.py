# -*- coding: utf-8 -*-
import sys, math
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3")
from agentA_verify import PhaseSolver, Phi

def Wf(a):
    return 3 + 2*a/np.tan(a)

def BD(q, c, S):
    a2 = S.alpha2(np.array([c]))[0]
    Ph = Phi(a2, q)
    return -Ph*Wf(a2)/(q+c*Ph) + 2*c*(q*q-1)*a2*Ph*abs(np.sin(a2)*np.cos(a2))/(q+c*Ph)**2

# fine q-dependence of BD at fixed c
for c in [0.005, 0.01, 0.05, 0.1, 0.3, 0.48]:
    qs = [5000, 8000, 10000, 12000, 15000, 20000]
    Ss = {q: PhaseSolver(q, N=200000) for q in qs}
    vals = [BD(q, c, Ss[q]) for q in qs]
    mono = all(vals[i+1] >= vals[i] - 1e-9 for i in range(len(vals)-1))
    print("c=%.3f: BD(q)=" % c, ["%.6f" % v for v in vals], "monotone_nondec:", mono)