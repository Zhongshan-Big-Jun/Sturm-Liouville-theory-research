# -*- coding: utf-8 -*-
"""agentB_trace.py: trace Gamma_1={R1=0} and Gamma_2={R2=0}, find intersections."""
import sys, time, json
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3')
import numpy as np
from agentB_lib import *

def r1(a, b, R): return float(f_at(a,b,R,a,config(a,b,R)))
def r2(a, b, R): return float(f_at(a,b,R,b,config(a,b,R)))

def trace_gamma1(R, na=50, nb=120):
    """For each a, all b in (a,1) with R1(a,b)=0 (bisection on fine scan)."""
    pts = []
    for a in np.linspace(0.005, 0.995, na):
        bs = np.linspace(a+1e-6, 1-1e-6, nb)
        vals = np.array([r1(a, b, R) for b in bs])
        for i in range(len(bs)-1):
            if vals[i]*vals[i+1] < 0:
                lo, hi = bs[i], bs[i+1]
                for _ in range(50):
                    m = 0.5*(lo+hi)
                    if r1(a, m, R)*r1(a, lo, R) < 0: hi = m
                    else: lo = m
                pts.append((a, 0.5*(lo+hi)))
    return pts

def trace_gamma2(R, nb=50, na=120):
    """For each b, all a in (0,b) with R2(a,b)=0."""
    pts = []
    for b in np.linspace(0.005, 0.995, nb):
        as_ = np.linspace(1e-6, b-1e-6, na)
        vals = np.array([r2(a, b, R) for a in as_])
        for i in range(len(as_)-1):
            if vals[i]*vals[i+1] < 0:
                lo, hi = as_[i], as_[i+1]
                for _ in range(50):
                    m = 0.5*(lo+hi)
                    if r2(m, b, R)*r2(lo, b, R) < 0: hi = m
                    else: lo = m
                pts.append((0.5*(lo+hi), b))
    return pts

if __name__ == '__main__':
    R = float(sys.argv[1]) if len(sys.argv)>1 else 4.0
    t0=time.time()
    g1 = trace_gamma1(R); print(f"Gamma1: {len(g1)} pts, t={time.time()-t0:.0f}s")
    t0=time.time()
    g2 = trace_gamma2(R); print(f"Gamma2: {len(g2)} pts, t={time.time()-t0:.0f}s")
    # print curves (a,b) pairs sorted
    print("Gamma1 (a -> b):")
    for a, b in sorted(g1):
        print(f"  {a:.4f} -> {b:.4f}")
    print("Gamma2 (a -> b):")
    for a, b in sorted(g2):
        print(f"  {a:.4f} -> {b:.4f}")
