# -*- coding: utf-8 -*-
import numpy as np
R = 4.0; s = np.sqrt(R); t = 1.0/(3*s+2)
a, b, c = s*t, t, s*t
jumps = [a, a+b, a+b+c, a+b+c+b]
vals = [1, R, 1, R, 1]

def full01(w):
    xs = [0.0] + jumps + [1.0]
    M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; cc = vals[i]
        ww = w*np.sqrt(cc); wL = ww*L
        cw = np.cos(wL); sw = np.sin(wL)/ww; sw2 = -ww*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return M01

def half_mixed(w):
    # half [1,R,1] widths (a,b,c/2), mixed BC: M11 = 0
    Ls = [a, b, c/2.0]; cs = [1.0, R, 1.0]
    M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
    for L, cc in zip(Ls, cs):
        ww = w*np.sqrt(cc); wL = ww*L
        cw = np.cos(wL); sw = np.sin(wL)/ww; sw2 = -ww*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return M11

for w in (np.sqrt(4.795347), np.sqrt(6.463037), np.sqrt(71.79196), np.sqrt(46.74785)):
    print(f"w={w:.6f} (lambda={w*w:.4f}): full M01 = {full01(w):+.6e}   half-mixed M11 = {half_mixed(w):+.6e}")
