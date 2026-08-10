# -*- coding: utf-8 -*-
"""n2_zeromap.py: zero map T(a,b)->(xhat-,xhat+): zeros of f = lam1 u1^2 - lam2 u2^2.
Study center map: m=(a+b/2...) center of jumps vs mhat = center of zeros.
"""
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

def zeros_of_f(blocks, N=4000, s=None):
    xs = np.linspace(1e-9, 1-1e-9, N)
    fv, s = f_vals(blocks, xs, s)
    sg = np.signbit(fv)
    ch = np.nonzero(sg[1:] != sg[:-1])[0]
    zs = []
    for i in ch:
        a, b = xs[i], xs[i+1]
        try:
            z = brentq(lambda t: f_vals(blocks, np.array([t]), s)[0][0], a, b, xtol=1e-14)
        except ValueError:
            continue
        zs.append(z)
    return np.array(sorted(zs)), s

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "SUP"
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    print(f"mode={mode} R={R}: zero map scan (m = center of jumps, mhat = center of f-zeros)")
    print(f"{'a':>8} {'b':>8} {'m':>8} {'xhat-':>10} {'xhat+':>10} {'mhat':>10} {'mhat-m':>10} {'mhat-1/2':>10} {'#zeros':>6}")
    for a in np.linspace(0.10, 0.88, 14):
        for b in np.linspace(0.05, 0.80, 12):
            if not (0.05 < a+b < 0.95):
                continue
            bl = make_blocks(mode, R, a, b)
            zs, s = zeros_of_f(bl)
            if len(zs) < 2:
                print(f"{a:8.4f} {b:8.4f} { (2*a+b)/2:8.4f} {'-':>10} {'-':>10} {'-':>10} {'-':>10} {'-':>10} {len(zs):6d}")
                continue
            m = a + b/2
            mhat = (zs[0]+zs[1])/2
            print(f"{a:8.4f} {b:8.4f} {m:8.4f} {zs[0]:10.5f} {zs[1]:10.5f} {mhat:10.5f} {mhat-m:+10.5f} {mhat-0.5:+10.5f} {len(zs):6d}")
