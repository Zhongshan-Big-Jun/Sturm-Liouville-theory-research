# -*- coding: utf-8 -*-
"""gap_n1_grad2.py: debug INF gradient."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def D_of(blocks, npts=60000, smax=None):
    s = lams_fast(blocks, 2, npts=npts, smax=smax)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

def f_vals(blocks, x_pts):
    s = lams_fast(blocks, 2)
    lam = s**2
    out = []
    for x in x_pts:
        u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
        u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
        out.append(lam[0]*u1**2 - lam[1]*u2**2)
    return np.array(out)

R = 4.0
a, b = 0.3, 0.4
for mode in ("SUP","INF"):
    bl = make_blocks(mode, R, a, b)
    f = f_vals(bl, [a, a+b])
    print(mode, "f(a)=%.6f f(a+b)=%.6f" % (f[0], f[1]))
    # high-precision D with large npts and check stencil
    for h in (1e-4, 1e-5, 1e-6):
        D0 = D_of(bl, npts=120000)
        Da = D_of(make_blocks(mode,R,a+h,b), npts=120000)
        Db = D_of(make_blocks(mode,R,a,b+h), npts=120000)
        print(f"  h={h}: (Da-D0)/h={ (Da-D0)/h:+.6f}  (Db-D0)/h={ (Db-D0)/h:+.6f}   D0={D0:.8f}")
