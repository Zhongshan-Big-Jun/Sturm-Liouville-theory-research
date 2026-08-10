# -*- coding: utf-8 -*-
"""Debug: M01 zeros for t=0.4, R=4."""
import numpy as np

def M01(s, t=0.4):
    c1, c2 = 1.0, 4.0
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    return (np.sin(w1*t)/q1)*np.cos(w2*(1-t)) + np.cos(w1*t)*np.sin(w2*(1-t))/q2

for s in [0.5, 1.0, 1.5, 1.7, 1.7542, 1.8, 2.0, 2.5, 3.0]:
    print(f"s={s}: M01 = {M01(s):+.6f}")
# first 6 sign changes
s = np.linspace(1e-9, 30, 300000)
M = np.array([M01(ss) for ss in s])
sg = np.signbit(M)
ch = sg[1:] != sg[:-1]
idx = np.nonzero(ch)[0]
print("first 6 sign-change indices at s =", s[idx[:6]], " M01 at those =", M[idx[:6]], M[idx[:6]+1])
