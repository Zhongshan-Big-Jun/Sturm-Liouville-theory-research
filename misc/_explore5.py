# -*- coding: utf-8 -*-
import math, numpy as np, sys
sys.path.insert(0, r"F:\LaTeX\BVE research\misc")
from _explore1 import Phi, Wf

def brackets(q, c):
    def f1(a): return q*math.tan(a)*math.tan(c*a) - 1.0
    lo, hi = 1e-12, math.pi/2 - 1e-12
    for _ in range(200):
        m = 0.5*(lo+hi)
        if f1(lo)*f1(m) <= 0: hi = m
        else: lo = m
    a1 = 0.5*(lo+hi)
    def f2(x): return q*math.tan(x) - math.tan(c*(math.pi - x))
    lo, hi = 1e-12, math.pi/2 - 1e-12
    for _ in range(200):
        m = 0.5*(lo+hi)
        if f2(lo)*f2(m) <= 0: hi = m
        else: lo = m
    g = 0.5*(lo+hi)
    a2 = math.pi - g
    P1, P2 = Phi(a1,q), Phi(g,q)
    W1, W2 = Wf(a1), Wf(a2)
    q1, q2 = q+c*P1, q+c*P2
    B1 = P1*W1/q1 - P2*W2/q2
    B2 = 2*c*(q*q-1)*( a2*P2*math.sin(g)*math.cos(g)/q2**2 - a1*P1*math.sin(a1)*math.cos(a1)/q1**2 )
    return B1, B2, B1+B2

bestB1 = (1e9, None); bestB2 = (1e9, None); bestS = (1e9, None)
negB2 = 0; n=0
for q in np.geomspace(1.000001, 1e6, 300):
    for c in np.concatenate([np.linspace(1e-5, 0.49, 120), np.linspace(0.49, 0.5-1e-6, 80)]):
        B1, B2, S = brackets(float(q), float(c)); n+=1
        if B1 < bestB1[0]: bestB1 = (B1, (float(q), float(c)))
        if B2 < bestB2[0]: bestB2 = (B2, (float(q), float(c)))
        if S < bestS[0]: bestS = (S, (float(q), float(c)))
        if B2 < 0: negB2 += 1
print("points:", n)
print("min B1 = %.6f at %s   (corner 2.41840)" % bestB1)
print("min B2 = %.6f at %s   (corner 0)" % bestB2)
print("min SUM = %.6f at %s" % bestS)
print("B2<0 count:", negB2)