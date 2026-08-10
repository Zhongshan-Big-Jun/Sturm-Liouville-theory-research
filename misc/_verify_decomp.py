# -*- coding: utf-8 -*-
import sys, math
import numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3")
from agentA_verify import PhaseSolver, Phi, G

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

# global min of A-C and B-D over q in [1.00025, 1e6], c in (0,1/2)
qs = [1.00025, 1.001, 1.01, 1.05, 1.1, 1.5, 2, 4, 10, 100, 1e4, 1e6]
minAC = (1e9, None); minBD = (1e9, None); minG = (1e9, None)
for q in qs:
    S = PhaseSolver(q, N=60000)
    cs = np.linspace(1e-4, 0.5-1e-5, 300)
    a1 = S.alpha1(cs); a2 = S.alpha2(cs)
    ACl = np.array([AC(q, c, S) for c in cs])
    BDl = np.array([BD(q, c, S) for c in cs])
    Gl = G(a2, cs, q) - G(a1, cs, q)
    i = np.argmin(ACl)
    if ACl[i] < minAC[0]: minAC = (ACl[i], (q, cs[i]))
    i = np.argmin(BDl)
    if BDl[i] < minBD[0]: minBD = (BDl[i], (q, cs[i]))
    i = np.argmin(Gl)
    if Gl[i] < minG[0]: minG = (Gl[i], (q, cs[i]))
print("min A-C  = %.6f at %s" % minAC)
print("min B-D  = %.6f at %s" % minBD)
print("min G2-G1= %.6f at %s" % minG)

# q-monotonicity: d/dq of A-C and B-D should be >= 0 (handoff: min pos increment ~9e-5)
print("q-monotonicity (min d/dq over sampled q, c):")
worst = (1e9, None)
for q in [1.001, 1.01, 1.05, 1.1, 1.5, 2, 4, 10, 100, 1e4, 1e6]:
    h = max(q*1e-5, 1e-5)
    S1 = PhaseSolver(q, N=60000); S2 = PhaseSolver(q+h, N=60000)
    for c in np.linspace(0.01, 0.49, 40):
        dAC = (AC(q+h, c, S2) - AC(q, c, S1))/h
        dBD = (BD(q+h, c, S2) - BD(q, c, S1))/h
        if dAC < worst[0]: worst = (dAC, ("AC", q, c))
        if dBD < worst[0]: worst = (dBD, ("BD", q, c))
print("  worst d/dq (should be >=0):", worst)