# -*- coding: utf-8 -*-
"""agentB_goodbranch.py: continuation trace of good branches a=x_- and b=x_+."""
import sys, time
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3')
import numpy as np
from agentB_lib import *

def R1(a, b, R):
    if not (1e-9 < a and a < b and b < 1-1e-9): return 1e9
    return float(f_at(a,b,R,a,config(a,b,R)))
def R2(a, b, R):
    if not (1e-9 < a and a < b and b < 1-1e-9): return 1e9
    return float(f_at(a,b,R,b,config(a,b,R)))
def goodL(a, b, R, tol=1e-7):
    z = zeros_f(a, b, R)
    if z is None: return False
    return abs(a-z[0]) < tol
def goodR(a, b, R, tol=1e-7):
    z = zeros_f(a, b, R)
    if z is None: return False
    return abs(b-z[1]) < tol

def bisect_r1(a, blo, bhi, R):
    """b in (blo,bhi) with R1(a,b)=0; assume sign change."""
    for _ in range(55):
        m = 0.5*(blo+bhi)
        if R1(a,m,R)*R1(a,blo,R) < 0: bhi = m
        else: blo = m
    return 0.5*(blo+bhi)

def bisect_r2(b, alo, ahi, R):
    for _ in range(55):
        m = 0.5*(alo+ahi)
        if R2(m,b,R)*R2(alo,b,R) < 0: ahi = m
        else: alo = m
    return 0.5*(alo+ahi)

def trace_good1(R, fp, n=240, da=0.001):
    """Continuation: good branch of Gamma_1 starting at fp, a increasing/decreasing."""
    pts = {}
    # forward in a
    a = fp[0]; b = fp[1]
    for step in range(n):
        a2 = a + da
        if a2 > 0.999: break
        if a2 >= b: break
        # scan b in a small window around previous b
        r = R1(a2, b, R)
        bb = np.linspace(max(b-0.05, a2+1e-6), b+0.05, 41)
        vals = [R1(a2, x, R) for x in bb]
        found = False
        for i in range(len(bb)-1):
            if vals[i]*vals[i+1] < 0:
                b2 = bisect_r1(a2, bb[i], bb[i+1], R)
                if goodL(a2, b2, R, tol=1e-5):
                    pts[round(a2,5)] = b2
                    a, b = a2, b2; found = True
                    break
        if not found: break
    a = fp[0]; b = fp[1]
    for step in range(n):
        a2 = a - da
        if a2 < 1e-4: break
        r = R1(a2, b, R)
        bb = np.linspace(max(b-0.05, a2+1e-6), b+0.05, 41)
        vals = [R1(a2, x, R) for x in bb]
        found = False
        for i in range(len(bb)-1):
            if vals[i]*vals[i+1] < 0:
                b2 = bisect_r1(a2, bb[i], bb[i+1], R)
                if goodL(a2, b2, R, tol=1e-5):
                    pts[round(a2,5)] = b2
                    a, b = a2, b2; found = True
                    break
        if not found: break
    return pts

def trace_good2(R, fp, n=240, db=0.001):
    """Continuation: good branch of Gamma_2 (b=x_+) parametrized by b; return dict b->a."""
    pts = {}
    b = fp[1]; a = fp[0]
    for step in range(n):
        b2 = b + db
        if b2 > 0.999: break
        aa = np.linspace(max(a-0.05, 1e-6), min(a+0.05, b2-1e-6), 41)
        vals = [R2(x, b2, R) for x in aa]
        found = False
        for i in range(len(aa)-1):
            if vals[i]*vals[i+1] < 0:
                a2 = bisect_r2(b2, aa[i], aa[i+1], R)
                if goodR(a2, b2, R, tol=1e-5):
                    pts[round(b2,5)] = a2
                    a, b = a2, b2; found=True
                    break
        if not found: break
    b = fp[1]; a = fp[0]
    for step in range(n):
        b2 = b - db
        if b2 < 1e-4: break
        aa = np.linspace(max(a-0.05, 1e-6), min(a+0.05, b2-1e-6), 41)
        vals = [R2(x, b2, R) for x in aa]
        found = False
        for i in range(len(aa)-1):
            if vals[i]*vals[i+1] < 0:
                a2 = bisect_r2(b2, aa[i], aa[i+1], R)
                if goodR(a2, b2, R, tol=1e-5):
                    pts[round(b2,5)] = a2
                    a, b = a2, b2; found=True
                    break
        if not found: break
    return pts

if __name__ == '__main__':
    R = float(sys.argv[1]) if len(sys.argv)>1 else 4.0
    fp = tuple(map(float, sys.argv[2].split(','))) if len(sys.argv)>2 else (0.4515,0.5485)
    t0=time.time()
    g1 = trace_good1(R, fp)
    print(f"Gamma_1 good branch: {len(g1)} pts, a in [{min(g1):.4f},{max(g1):.4f}], t={time.time()-t0:.0f}s")
    t0=time.time()
    g2 = trace_good2(R, fp)
    print(f"Gamma_2 good branch: {len(g2)} pts, b in [{min(g2):.4f},{max(g2):.4f}], t={time.time()-t0:.0f}s")
    # sample the branches
    print("Gamma_1 samples (a,b):")
    for a in sorted(g1)[::15]:
        print(f"  {a:.4f} {g1[a]:.4f}")
    print("Gamma_2 samples (b,a):")
    for b in sorted(g2)[::15]:
        print(f"  {b:.4f} {g2[b]:.4f}")
    # monotonicity checks
    g1a = sorted(g1); g1b = [g1[a] for a in g1a]
    inc = all(g1b[i+1] > g1b[i] for i in range(len(g1b)-1))
    g2b = sorted(g2); g2a = [g2[b] for b in g2b]
    inc2 = all(g2a[i+1] > g2a[i] for i in range(len(g2a)-1))
    print(f"Gamma_1 monotone increasing in b: {inc}; Gamma_2 monotone increasing in a: {inc2}")
