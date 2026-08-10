# -*- coding: utf-8 -*-
"""agentB_goodbranch2.py: predictor-corrector trace of good branches."""
import sys, time
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3')
import numpy as np
from agentB_lib import *

def R1(a, b, R):
    if not (1e-9 < a and a < b and b < 1-1e-9): return None
    return float(f_at(a,b,R,a,config(a,b,R)))
def R2(a, b, R):
    if not (1e-9 < a and a < b and b < 1-1e-9): return None
    return float(f_at(a,b,R,b,config(a,b,R)))

def dR1(a, b, R, h=1e-6):
    return ((R1(a+h,b,R)-R1(a-h,b,R))/(2*h), (R1(a,b+h,R)-R1(a,b-h,R))/(2*h))
def dR2(a, b, R, h=1e-6):
    return ((R2(a+h,b,R)-R2(a-h,b,R))/(2*h), (R2(a,b+h,R)-R2(a,b-h,R))/(2*h))

def goodL(a, b, R, tol=1e-6):
    z = zeros_f(a, b, R)
    return z is not None and abs(a-z[0]) < tol
def goodR(a, b, R, tol=1e-6):
    z = zeros_f(a, b, R)
    return z is not None and abs(b-z[1]) < tol

def correct_r1(a, b_guess, R, win=0.08, n=41):
    """find b near b_guess with R1(a,b)=0; bisection; None if no sign change."""
    bb = np.linspace(max(b_guess-win, a+1e-6), min(b_guess+win, 1-1e-6), n)
    vals = [R1(a, x, R) for x in bb]
    for i in range(len(bb)-1):
        if vals[i] is not None and vals[i+1] is not None and vals[i]*vals[i+1] < 0:
            lo, hi = bb[i], bb[i+1]
            for _ in range(55):
                m = 0.5*(lo+hi)
                if R1(a,m,R)*R1(a,lo,R) < 0: hi = m
                else: lo = m
            return 0.5*(lo+hi)
    return None

def correct_r2(b, a_guess, R, win=0.08, n=41):
    aa = np.linspace(max(a_guess-win, 1e-6), min(a_guess+win, b-1e-6), n)
    vals = [R2(x, b, R) for x in aa]
    for i in range(len(aa)-1):
        if vals[i] is not None and vals[i+1] is not None and vals[i]*vals[i+1] < 0:
            lo, hi = aa[i], aa[i+1]
            for _ in range(55):
                m = 0.5*(lo+hi)
                if R2(m,b,R)*R2(lo,b,R) < 0: hi = m
                else: lo = m
            return 0.5*(lo+hi)
    return None

def trace_good1(R, fp, n=600, ds=0.001, which='L'):
    """Continuation in arc-length-like steps; returns dict a->b along Gamma_1 good (a=x_-)."""
    pts = {}
    for direction in [1, -1]:
        a, b = fp
        # initial slope via FD
        ra, rb = dR1(a, b, R)
        slope = -ra/rb if rb != 0 else 0.0
        for step in range(n):
            # predictor: move in tangent direction (1, slope), scaled
            norm = np.hypot(1, slope)
            a2 = a + direction*ds/norm
            b_pred = b + direction*ds*slope/norm
            if not (1e-6 < a2 < 0.999) or a2 >= 0.999: break
            b2 = correct_r1(a2, b_pred, R, win=0.10)
            if b2 is None or not (a2 < b2 < 1-1e-6): break
            if not goodL(a2, b2, R): break
            pts[round(a2,5)] = b2
            # update slope
            ra, rb = dR1(a2, b2, R)
            if abs(rb) < 1e-9: break
            slope = -ra/rb
            a, b = a2, b2
    return pts

def trace_good2(R, fp, n=600, ds=0.001):
    pts = {}
    for direction in [1, -1]:
        b, a = fp[1], fp[0]
        ra, rb = dR2(a, b, R)
        slope_a = -rb/ra if ra != 0 else 0.0   # da/db
        for step in range(n):
            norm = np.hypot(1, slope_a)
            b2 = b + direction*ds/norm
            a_pred = a + direction*ds*slope_a/norm
            if not (1e-6 < b2 < 0.999): break
            a2 = correct_r2(b2, a_pred, R, win=0.10)
            if a2 is None or not (1e-6 < a2 < b2): break
            if not goodR(a2, b2, R): break
            pts[round(b2,5)] = a2
            ra, rb = dR2(a2, b2, R)
            if abs(ra) < 1e-9: break
            slope_a = -rb/ra
            b, a = b2, a2
    return pts

if __name__ == '__main__':
    R = float(sys.argv[1]) if len(sys.argv)>1 else 4.0
    fp = tuple(map(float, sys.argv[2].split(','))) if len(sys.argv)>2 else (0.4515,0.5485)
    t0=time.time()
    g1 = trace_good1(R, fp)
    print(f"Gamma_1 good: {len(g1)} pts, a in [{min(g1):.4f},{max(g1):.4f}], t={time.time()-t0:.0f}s")
    t0=time.time()
    g2 = trace_good2(R, fp)
    print(f"Gamma_2 good: {len(g2)} pts, b in [{min(g2):.4f},{max(g2):.4f}], t={time.time()-t0:.0f}s")
    g1a = sorted(g1); g1b = [g1[a] for a in g1a]
    inc = all(g1b[i+1] > g1b[i] for i in range(len(g1b)-1))
    g2b = sorted(g2); g2a = [g2[b] for b in g2b]
    inc2 = all(g2a[i+1] > g2a[i] for i in range(len(g2a)-1))
    print(f"Gamma_1 increasing: {inc}; Gamma_2 increasing: {inc2}")
    a1arr = np.array(sorted(g1)); b1arr = np.array([g1[a] for a in a1arr])
    b2arr = np.array(sorted(g2)); a2arr = np.array([g2[b] for b in b2arr])
    from numpy import interp
    def g1of(a): return interp(a, a1arr, b1arr)
    def g2of(a): return interp(a, a2arr, b2arr)
    amin = max(a1arr.min(), a2arr.min()); amax = min(a1arr.max(), a2arr.max())
    print(f"common a-range: [{amin:.4f},{amax:.4f}]")
    if amin < amax:
        aa = np.linspace(amin, amax, 200)
        h = g1of(aa) - g2of(aa)
        signs = np.sign(h)
        ch = int(np.sum(signs[1:] != signs[:-1]))
        zc = aa[:-1][signs[1:] != signs[:-1]]
        print(f"sign changes of g1-g2: {ch} at a ~ {np.round(zc,4)}")
        # exact crossing via bisection
        for i in range(len(signs)-1):
            if signs[i] != signs[i+1]:
                lo, hi = aa[i], aa[i+1]
                for _ in range(55):
                    m = 0.5*(lo+hi)
                    if (g1of(m)-g2of(m))*(g1of(lo)-g2of(lo)) < 0: hi = m
                    else: lo = m
                print(f"  crossing at a={0.5*(lo+hi):.8f}, g1={g1of(0.5*(lo+hi)):.8f}")
    # save
    import json
    out = dict(R=R, g1=[[float(a), float(g1[a])] for a in a1arr], g2=[[float(a2arr[i]), float(b2arr[i])] for i in range(len(b2arr))])
    out_path = "F:/LaTeX/BVE research/runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentB_goodbranches.json"
    with open(out_path, "a") as f:
        f.write(json.dumps(out) + "\n")
