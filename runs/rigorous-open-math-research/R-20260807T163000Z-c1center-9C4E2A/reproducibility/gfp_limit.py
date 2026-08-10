# -*- coding: utf-8 -*-
"""gfp_limit.py: G at the fp for very large R; check -> sqrt(2)."""
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fast_lib import sec, norm_n
from c1trace_lib import a_fp, partials

def roots2(a, b, R, ns=20001):
    s = np.linspace(1e-9, 2*np.pi+0.6, ns)
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0][:2]
    out = []
    for i in idx:
        lo, hi = s[i], s[i+1]; flo = M[i]
        for _ in range(70):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        out.append(0.5*(lo+hi))
    return out

for R in [1e6, 1e7, 1e8]:
    fp = a_fp(R)
    a, b = fp, 1-fp
    # for 1e8 the barrier width ~ 1.3e-5; finite-difference h must be smaller
    h = 1e-7 if R < 1e8 else 1e-8
    s1, s2 = roots2(a, b, R)
    print("R=%.0e fp=%.10f w=%.3e" % (R, fp, 1-2*fp))
    R1a, R1b, R2a, R2b = partials(a, b, R)
    G = -R1a/R1b
    print("  G(fp)=%.8f  sqrt2=%.8f  Phi(fp)=G^2=%.8f" % (G, np.sqrt(2), G**2))
