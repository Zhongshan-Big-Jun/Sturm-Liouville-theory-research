# -*- coding: utf-8 -*-
"""dbg_endpoint_h.py v2 - compute the fp-component sheet and h endpoints at small eps.
Sheet a = A(b): Newton solve R1(a,b,1+eps)=0 continued from a0 at b=a0.  [EVIDENCE]."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2

a0 = float(np.arccos(0.25)/np.pi)

def sheet(eps, bgrid):
    out = []
    a_prev = a0
    for b in bgrid:
        a = a_prev
        ok = True
        for _ in range(80):
            fa = R1R2(a, b, 1+eps)[0]
            if abs(fa) < 1e-13: break
            h = 1e-6
            d = (R1R2(a+h, b, 1+eps)[0]-R1R2(a-h, b, 1+eps)[0])/(2*h)
            if abs(d) < 1e-9: ok = False; break
            an = a - fa/d
            if not (0 < an < b): ok = False; break
            a = an
        out.append((b, a, R1R2(a, b, 1+eps)[0] if ok else np.nan))
        a_prev = a
    return out

for eps in (0.02, 0.05, 0.1):
    bgrid = np.linspace(a0, 0.99, 400)
    br = sheet(eps, bgrid)
    good = [(b, a, r) for (b, a, r) in br if np.isfinite(r) and abs(r) < 1e-6 and 0 < a < b]
    bs = np.array([x[0] for x in good]); as_ = np.array([x[1] for x in good])
    b_top, a_max1 = bs[-1], as_[-1]
    def A(x): return np.interp(x, bs, as_)
    print("eps=%.2f: b_top=%.4f  a_max1=A(b_top)=%.6f" % (eps, b_top, a_max1))
    # h(a) = g1(a) - 1 + u(a),  g1 = A^{-1},  u(a) = A(1-a)
    def g1(a): return np.interp(a, as_, bs)
    def u(a): return A(1-a)
    # domain of h: a in [a0, beta], beta = min(a_max1, 1-a0)
    beta = min(a_max1, 1-a0)
    aa = np.linspace(as_[0], beta, 300)
    hh = np.array([g1(x) - 1 + u(x) for x in aa])
    ia0 = np.argmin(np.abs(aa-a0))
    print("  beta=%.6f  h(a0)=%.6f (pred %.6f)  h(beta)=%.6f  u(beta)=%.6f  g1(beta)=%.6f"
          % (beta, hh[ia0], 2*a0-1+eps*0.0260216806655324, hh[-1], u(beta), g1(beta)))
    # phi2(b0): A(b0) - a0 - eps*phi(b0)
    dA = A(1-a0) - a0
    print("  A(b0)-a0 = %.6f  eps*phi(b0)=%.6f  diff/eps^2 = %.4f" % (dA, eps*0.0260216806655324, (dA-eps*0.0260216806655324)/eps**2))
