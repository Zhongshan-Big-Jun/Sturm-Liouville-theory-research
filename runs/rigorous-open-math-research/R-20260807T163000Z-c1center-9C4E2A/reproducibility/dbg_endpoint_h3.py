# -*- coding: utf-8 -*-
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
a0 = float(np.arccos(0.25)/np.pi)
eps = 0.02
bgrid = np.linspace(a0, 0.99, 400)
out = []
a_prev = a0
for b in bgrid:
    a = a_prev
    for _ in range(80):
        fa = R1R2(a, b, 1+eps)[0]
        if abs(fa) < 1e-13: break
        h = 1e-6
        d = (R1R2(a+h, b, 1+eps)[0]-R1R2(a-h, b, 1+eps)[0])/(2*h)
        if abs(d) < 1e-9: break
        an = a - fa/d
        if not (0 < an < b): break
        a = an
    out.append((b, a, R1R2(a, b, 1+eps)[0]))
    a_prev = a
good = [(b, a, r) for (b, a, r) in out if abs(r) < 1e-6 and 0 < a < b]
bs = np.array([x[0] for x in good]); as_ = np.array([x[1] for x in good])
print("monotone as_:", np.all(np.diff(as_) > 0), " monotone bs:", np.all(np.diff(bs) > 0))
print("first 3 (b,a):", good[:3])
print("last 3 (b,a):", good[-3:])
def A(x): return np.interp(x, bs, as_)
b0 = 1 - a0
print("A(a0)   = %.10f (expect a0 %.10f)" % (A(a0), a0))
print("A(b0)   = %.10f" % A(b0))
print("h(a0)   = %.10f  (formula 2a0-1+eps*phi(b0) = %.10f)" % (a0 - 1 + A(b0), 2*a0-1+eps*0.0260216806655324))
# u(a0) = A(1-a0); check via direct solve too
def A_direct(x):
    # solve A(b)=x
    lo, hi = a0, 0.99
    for _ in range(80):
        md = 0.5*(lo+hi)
        if A(md) < x: lo = md
        else: hi = md
    return 0.5*(lo+hi)
print("A_direct check: A(0.5)=%.8f vs interp %.8f" % (A_direct(0.5), A(0.5)))
print("u(beta): beta=%.6f, A(1-beta)=%.8f" % (as_[-1], A(1-as_[-1])))
