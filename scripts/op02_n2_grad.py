# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import brentq

def detfun(s, jumps, vals):
    xs = [0.0] + list(jumps) + [1.0]
    M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2; n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2; n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def lams_precise(jumps, vals, k=5):
    A = max(vals)
    s = np.linspace(1e-8, np.sqrt(A*1200), 120000)
    d = np.array([detfun(x, jumps, vals) for x in s])
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        root = brentq(detfun, slo, shi, args=(jumps, vals), xtol=1e-15, rtol=1e-15)
        out.append(root**2)
        if len(out) >= k: break
    return np.sort(out)[:k]

R = 4.0; s = np.sqrt(R); t = 1.0/(3*s+2)
x0 = np.array([s*t, t, s*t])
def ratio_abc(a, b, c, R=4.0):
    jumps = [a, a+b, a+b+c, a+b+c+b]
    lams = lams_precise(jumps, [1,R,1,R,1])
    return lams[2]/lams[1]

print("ratio at conjectured:", repr(ratio_abc(*x0)))
def ratio_ab(ab):
    a, b = ab
    c = 1-2*b-a
    return ratio_abc(a, b, c)
for hh in (3e-5, 1e-4, 3e-4):
    ga = (ratio_ab([x0[0]+hh, x0[1]]) - ratio_ab([x0[0]-hh, x0[1]]))/(2*hh)
    gb = (ratio_ab([x0[0], x0[1]+hh]) - ratio_ab([x0[0], x0[1]-hh]))/(2*hh)
    print(f"  h={hh}: d/da={ga:+.4e}  d/db={gb:+.4e}")
