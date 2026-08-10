# -*- coding: utf-8 -*-
import sys
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3")
from agentA_verify import PhaseSolver, Phi

def Wf(a):
    return 3 + 2*a/np.tan(a)

def AC(q, c, S):
    a1 = S.alpha1(np.array([c]))[0]
    Ph = Phi(a1, q)
    return Ph*Wf(a1)/(q+c*Ph) - 2*c*(q*q-1)*a1*Ph*np.sin(a1)*np.cos(a1)/(q+c*Ph)**2

def BD(q, c, S):
    a2 = S.alpha2(np.array([c]))[0]
    Ph = Phi(a2, q)
    return -Ph*Wf(a2)/(q+c*Ph) + 2*c*(q*q-1)*a2*Ph*abs(np.sin(a2)*np.cos(a2))/(q+c*Ph)**2

print("A-C monotonicity in q (fine scan):")
for c in [0.005, 0.01, 0.05, 0.1, 0.3, 0.48]:
    qs = [5000, 8000, 10000, 12000, 15000, 20000]
    Ss = {q: PhaseSolver(q, N=200000) for q in qs}
    vals = [AC(q, c, Ss[q]) for q in qs]
    mono = all(vals[i+1] >= vals[i] - 1e-9 for i in range(len(vals)-1))
    print("c=%.3f: AC(q)=" % c, ["%.6f" % v for v in vals], "monotone_nondec:", mono)

# wide-grid scan of the SUM G2-G1 and its min location
print("min of sum G2-G1 over wide grid:")
qs = [1.00025, 1.001, 1.01, 1.05, 1.1, 1.5, 2, 4, 10, 100, 1000, 1e4, 1e5, 1e6]
best = (1e9, None)
for q in qs:
    S = PhaseSolver(q, N=80000)
    cs = np.linspace(1e-4, 0.5-1e-5, 400)
    a1 = S.alpha1(cs); a2 = S.alpha2(cs)
    sumv = np.array([AC(q, c, S)+BD(q, c, S) for c in cs])
    i = np.argmin(sumv)
    if sumv[i] < best[0]: best = (sumv[i], (q, cs[i]))
print("  min sum = %.6f at %s" % best)