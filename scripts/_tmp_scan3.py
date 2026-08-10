# -*- coding: utf-8 -*-
"""Scan the 3-block family for self-consistency solutions f(a)=f(b)=0."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

R = 4.0

def fval(a, b, x):
    blocks = [(a,1.0),(b-a,R),(1-b,1.0)]
    s = lams_fast(blocks, 3)
    lam = s**2
    out = []
    for k in (0,1):
        y = y_at(blocks, s[k], np.array([x]))[0]
        out.append(y/np.sqrt(norm2(blocks, s[k])))
    u1, u2 = out
    return lam[0]*u1**2 - lam[1]*u2**2

Na, Nb = 50, 50
aa = np.linspace(0.02, 0.48, Na)
bb = np.linspace(0.52, 0.98, Nb)
zeros_a = []; zeros_b = []
for a in aa:
    prev = None
    for b in bb:
        fa = fval(a, b, a)
        if prev is not None and prev*fa < 0:
            zeros_a.append((a, b))
        prev = fa
for b in bb:
    prev = None
    for a in aa:
        fb = fval(a, b, b)
        if prev is not None and prev*fb < 0:
            zeros_b.append((a, b))
        prev = fb
print("f(a)=0 crossings:", len(zeros_a))
print("f(b)=0 crossings:", len(zeros_b))
# intersections: zeros_a near zeros_b
inter = []
for (a,b) in zeros_a:
    for (a2,b2) in zeros_b:
        if abs(a-a2) < 0.03 and abs(b-b2) < 0.03:
            inter.append((round(a,3), round(b,3)))
print("candidate intersections:", sorted(set(inter)))
