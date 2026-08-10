# -*- coding: utf-8 -*-
"""n2_node2.py: mhat vs node z relation."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=1500):
    return lams_fast(blocks, 2, npts=npts)

def f_vals(blocks, xs, s=None, npts=1500):
    if s is None:
        s = s_of(blocks, npts)
    lam = s**2
    xs = np.clip(np.asarray(xs, float), 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], xs)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], xs)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, s

def zeros_and_node(blocks, N=4000, s=None):
    xs = np.linspace(1e-9, 1-1e-9, N)
    fv, s = f_vals(blocks, xs, s)
    sg = np.signbit(fv)
    ch = np.nonzero(sg[1:] != sg[:-1])[0]
    zs = []
    for i in ch:
        a, b = xs[i], xs[i+1]
        try:
            z = brentq(lambda t: f_vals(blocks, np.array([t]), s)[0][0], a, b, xtol=1e-13)
        except ValueError:
            continue
        zs.append(z)
    u2v = y_at(blocks, s[1], xs)
    sg2 = np.signbit(u2v)
    ch2 = np.nonzero(sg2[1:] != sg2[:-1])[0]
    node = brentq(lambda t: y_at(blocks, s[1], np.array([t]))[0], xs[ch2[0]], xs[ch2[0]+1], xtol=1e-13)
    return np.array(sorted(zs)), node, s

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

for mode in ("SUP","INF"):
    print(f"-- {mode} R=4 --")
    print(f"{'a':>8} {'b':>8} {'m':>8} {'mhat':>8} {'node z':>8} {'mhat-z':>8}")
    for a in (0.1, 0.28, 0.46, 0.7):
        for b in (0.05, 0.2545, 0.5273):
            if not (0.05 < a+b < 0.95): continue
            bl = make_blocks(mode, 4.0, a, b)
            zs, node, s = zeros_and_node(bl)
            m = a + b/2
            mhat = (zs[0]+zs[1])/2 if len(zs)==2 else float('nan')
            print(f"{a:8.3f} {b:8.4f} {m:8.4f} {mhat:8.4f} {node:8.4f} {mhat-node:+8.4f}")
