# -*- coding: utf-8 -*-
"""num_gapn1_curves_trace.py: trace Gamma_1={f(a;a,b)=0} and Gamma_2={f(b;a,b)=0}
in the (a,b) plane for the barrier/well families; check monotonicity and unique crossing."""
import numpy as np
from scipy.optimize import brentq
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    if mode == "SUP":
        return [(a,1.0),(b-a,R),(1-b,1.0)]
    return [(a,R),(b-a,1.0),(1-b,R)]

def f_at(blocks, x):
    s = lams_fast(blocks, 2, npts=6000)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1*u1 - lam[1]*u2*u2

def z0_of(blocks):
    """zero of u2 in (0,1)."""
    s = lams_fast(blocks, 2, npts=6000)
    xs = np.linspace(0.001, 0.999, 4001)
    u2 = y_at(blocks, s[1], xs)
    z = np.where(np.diff(np.signbit(u2)) != 0)[0]
    return xs[z[0]] if len(z) else np.nan

def trace_curves(R, mode, N=40):
    aa = np.linspace(0.05, 0.45, N)
    rows = []
    for a in aa:
        def F1(b): return f_at(make_blocks(mode,R,a,b), a)
        def F2(b): return f_at(make_blocks(mode,R,a,b), b)
        h1 = h2 = None
        # Gamma_1: solve F1(b)=0 over b in (a+eps, 1-eps)
        bs = np.linspace(a+0.01, 0.99, 40)
        v1 = np.array([F1(b) for b in bs])
        for i in range(len(bs)-1):
            if v1[i]*v1[i+1] < 0:
                h1 = brentq(F1, bs[i], bs[i+1], xtol=1e-12); break
        v2 = np.array([F2(b) for b in bs])
        for i in range(len(bs)-1):
            if v2[i]*v2[i+1] < 0:
                h2 = brentq(F2, bs[i], bs[i+1], xtol=1e-12); break
        rows.append((a, h1, h2))
    return rows

if __name__ == "__main__":
    for R in (2.0, 4.0, 10.0):
        for mode in ("SUP","INF"):
            rows = trace_curves(R, mode, N=30)
            print(f"===== R={R} {mode} =====")
            print("  a      h1(a) [f(a)=0]   h2(a) [f(b)=0]")
            prev = None
            mono1 = mono2 = True
            for (a, h1, h2) in rows:
                tag1 = ""
                if h1 is not None:
                    if prev is not None and prev[0] is not None and h1 <= prev[0]: tag1 += "  <-- h1 not increasing"
                    prev = (h1, prev[1] if prev else None)
                if h1 is not None and h2 is not None:
                    print(f"  {a:6.3f}   {h1:10.6f}   {h2:10.6f}")
                else:
                    print(f"  {a:6.3f}   {h1}   {h2}")
