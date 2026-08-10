# -*- coding: utf-8 -*-
"""agentB_crossing.py: direct sampling of g1(a), g2(a) (all good roots) and h=g1-g2."""
import sys, time
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3')
import numpy as np
from agentB_lib import *

def R1(a, b, R): return float(f_at(a,b,R,a,config(a,b,R)))
def R2(a, b, R): return float(f_at(a,b,R,b,config(a,b,R)))

def all_roots_r1(a, R, nb=160):
    """all b in (a,1) with R1(a,b)=0 that are left-good (a=x_-)."""
    bs = np.linspace(a+1e-5, 1-1e-5, nb)
    vals = np.array([R1(a,b,R) for b in bs])
    out = []
    for i in range(len(bs)-1):
        if vals[i]*vals[i+1] < 0:
            lo, hi = bs[i], bs[i+1]
            for _ in range(50):
                m = 0.5*(lo+hi)
                if R1(a,m,R)*R1(a,lo,R) < 0: hi = m
                else: lo = m
            b2 = 0.5*(lo+hi)
            z = zeros_f(a, b2, R)
            if z is not None and abs(a-z[0]) < 1e-5:
                out.append(b2)
    return out

def all_roots_r2(a, R, nb=160):
    """all b in (a,1) with R2(a,b)=0 that are right-good (b=x_+)."""
    bs = np.linspace(a+1e-5, 1-1e-5, nb)
    vals = np.array([R2(a,b,R) for b in bs])
    out = []
    for i in range(len(bs)-1):
        if vals[i]*vals[i+1] < 0:
            lo, hi = bs[i], bs[i+1]
            for _ in range(50):
                m = 0.5*(lo+hi)
                if R2(a,m,R)*R2(a,lo,R) < 0: hi = m
                else: lo = m
            b2 = 0.5*(lo+hi)
            z = zeros_f(a, b2, R)
            if z is not None and abs(b2-z[1]) < 1e-5:
                out.append(b2)
    return out

if __name__ == '__main__':
    R = float(sys.argv[1])
    a0 = float(sys.argv[2]); a1 = float(sys.argv[3]); na = int(sys.argv[4]) if len(sys.argv)>4 else 30
    t0=time.time()
    rows = []
    for a in np.linspace(a0, a1, na):
        g1 = all_roots_r1(a, R)
        g2 = all_roots_r2(a, R)
        for b1 in g1:
            for b2 in g2:
                rows.append((a, b1, b2, b1-b2))
    print(f"R={R} a in [{a0},{a1}]: {len(rows)} (a,g1,g2) triples, t={time.time()-t0:.0f}s")
    # print rows where both branches exist
    prev_sign = None
    for (a,b1,b2,h) in rows:
        print(f"  a={a:.4f}: g1={b1:.4f} g2={b2:.4f} h={h:+.4f}")
