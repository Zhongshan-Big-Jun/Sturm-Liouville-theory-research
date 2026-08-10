# -*- coding: utf-8 -*-
"""u2_shape.py: output u1, u2 shapes at the fp for R=1e6 and R=1e4."""
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, y_at, norm_n
from c1trace_lib import a_fp

def roots2(a, b, R):
    s = np.linspace(1e-9, 2*np.pi+0.6, 4001)
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0][:2]
    out = []
    for i in idx:
        lo, hi = s[i], s[i+1]; flo = M[i]
        for _ in range(60):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        out.append(0.5*(lo+hi))
    return out

for R in [1e4, 1e6]:
    fp = a_fp(R); a, b = fp, 1-fp
    s1, s2 = roots2(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    print("R=%.0e fp=%.8f a=%.8f b=%.8f s1=%.8f s2=%.8f" % (R, fp, a, b, s1, s2))
    print("  l1=%.8f l2=%.8f" % (s1**2, s2**2))
    xs = np.linspace(0, 1, 201)
    u1 = np.array([y_at(s1, a, b, R, x)/np.sqrt(n1) for x in xs])
    u2 = np.array([y_at(s2, a, b, R, x)/np.sqrt(n2) for x in xs])
    ref2 = np.sqrt(2)*np.sin(2*np.pi*xs)
    ref1 = np.ones_like(xs)
    # check parity: u2(x) vs -u2(1-x)
    parity2 = np.max(np.abs(u2 + np.flip(u2)))
    parity1 = np.max(np.abs(u1 - np.flip(u1)))
    print("  u1 even to %.2e, u2 odd to %.2e" % (parity1, parity2))
    # sample u2 at a few points
    for x in [0.25, 0.45, 0.499, 0.5, 0.5+0.00012, 0.55, 0.75]:
        i = np.argmin(np.abs(xs - x))
        print("    x=%.6f: u1=%.6f u2=%.6f (ref2=%.6f)" % (x, u1[i], u2[i], np.sqrt(2)*np.sin(2*np.pi*x)))
