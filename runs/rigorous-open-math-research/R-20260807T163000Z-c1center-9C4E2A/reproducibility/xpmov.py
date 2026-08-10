# -*- coding: utf-8 -*-
"""xpmov.py: along the fp-branch, compute dx+/da, dx+/db, dx-/da, dx-/db and check signs."""
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n, y_at
from c1trace_lib import R1R2, a_fp, A0, B0
from trace_w import trace_w

def zeros_f(a, b, R, s1, s2, n1, n2):
    # zeros of f = lambda1 u1^2 - lambda2 u2^2 via v^2 = q^2
    q2 = (s1**2*n2)/(s2**2*n1)
    # v = y2/y1, find crossings of v^2 = q^2 in (0,1)
    xs = np.linspace(1e-6, 1-1e-6, 4001)
    def v(x): return (np.sin(s2*x)/s2)/(np.sin(s1*x)/s1) if x <= a else y_at(s2,a,b,R,x)/y_at(s1,a,b,R,x)
    vals = np.array([v(x)**2 - q2 for x in xs])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    idx = np.nonzero(ch)[0]
    # x_- : on (0, z), v decreasing from s2/s1 to 0 -> v^2=q^2 once; x_+ once on (z,1)
    # pick the two with v>0 and v<0 sides: just take first and last crossings
    return xs[idx[0]], xs[idx[-1]]

def cfg(a, b, R):
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
    return out[0], out[1], norm_n(out[0], a, b, R), norm_n(out[1], a, b, R)

for R in [4.0, 100.0, 1000.0, 10000.0]:
    pts = trace_w(R, A0, B0, nstep=400)
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
    keep = [0]
    for i in range(1, len(aa)):
        if aa[i] > aa[keep[-1]]+1e-12: keep.append(i)
    aa = aa[keep]; bb = bb[keep]
    h = 1e-6
    rows = []
    for i in range(0, len(aa), 7):
        a, b = aa[i], bb[i]
        s1, s2, n1, n2 = cfg(a, b, R)
        xm, xp = zeros_f(a, b, R, s1, s2, n1, n2)
        # finite-difference partials of x_+ and x_-
        dxp_da = (zeros_f(a+h, b, R, *cfg(a+h,b,R))[1] - xp)/h
        dxp_db = (zeros_f(a, b+h, R, *cfg(a,b+h,R))[1] - xp)/h
        dxm_da = (zeros_f(a+h, b, R, *cfg(a+h,b,R))[0] - xm)/h
        dxm_db = (zeros_f(a, b+h, R, *cfg(a,b+h,R))[0] - xm)/h
        rows.append((a, b, xm, xp, dxp_da, dxp_db, dxm_da, dxm_db))
    rows = np.array(rows)
    print("R=%g: dxp/da: min=%.4f max=%.4f all>0=%s ; dxp/db: min=%.4f max=%.4f all<0=%s ; 1+dxp/db: min=%.4f" % (
        R, rows[:,4].min(), rows[:,4].max(), (rows[:,4]>0).all(), rows[:,5].min(), rows[:,5].max(), (rows[:,5]<0).all(), (1+rows[:,5]).min()))
    print("      dxm/da: min=%.4f max=%.4f ; dxm/db: min=%.4f max=%.4f ; twist dxp/da + dxm/db: max|.|=%.2e" % (
        rows[:,6].min(), rows[:,6].max(), rows[:,7].min(), rows[:,7].max(), np.abs(rows[:,4]+rows[:,7]).max()))
