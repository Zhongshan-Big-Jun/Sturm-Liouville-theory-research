# -*- coding: utf-8 -*-
"""analyze_3.py: g1(a)-a on branch; x_+/- monotonicity in a,b; R1(a,a+) sign."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fast_lib as F

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_branch_full.json")) as fh:
    data = json.load(fh)

def band_ends(a, b, R):
    """x_-, x_+ = zeros of f with v = +/-q; find via v(x) = +/- q."""
    s1, s2 = F.roots2_fast(a, b, R)
    n1, n2 = F.norm_n(s1,a,b,R), F.norm_n(s2,a,b,R)
    q = (s1/s2)*np.sqrt(n2/n1)
    # v(x) = y2/y1; find x with v = q and v = -q by bisection
    def v(x):
        if x <= 1e-9: return 1.0
        if x >= 1-1e-9:
            # v(1-) = y2'(1)/y1'(1): compute via y_at near 1
            return None
        y1 = F.y_at(s1, a, b, R, x); y2 = F.y_at(s2, a, b, R, x)
        return y2/y1
    # sample v on grid
    xs = np.linspace(1e-7, 1-1e-7, 2001)
    vs = np.array([F.y_at(s2,a,b,R,x)/F.y_at(s1,a,b,R,x) for x in xs])
    xm, xp = None, None
    ch = np.signbit(vs[1:]-q) != np.signbit(vs[:-1]-q)
    for i in np.nonzero(ch)[0]:
        # refine
        lo, hi = xs[i], xs[i+1]
        for _ in range(40):
            md = 0.5*(lo+hi)
            vm = F.y_at(s2,a,b,R,md)/F.y_at(s1,a,b,R,md)
            if (vm - q)*(F.y_at(s2,a,b,R,lo)/F.y_at(s1,a,b,R,lo) - q) < 0: hi = md
            else: lo = md
        xm = 0.5*(lo+hi)
        break
    ch2 = np.signbit(vs[1:]+q) != np.signbit(vs[:-1]+q)
    for i in np.nonzero(ch2)[0]:
        lo, hi = xs[i], xs[i+1]
        for _ in range(40):
            md = 0.5*(lo+hi)
            vm = F.y_at(s2,a,b,R,md)/F.y_at(s1,a,b,R,md)
            if (vm + q)*(F.y_at(s2,a,b,R,lo)/F.y_at(s1,a,b,R,lo) + q) < 0: hi = md
            else: lo = md
        xp = 0.5*(lo+hi)
        break
    return xm, xp

print("band endpoint monotonicity (R=4):")
for (a,b) in [(0.43,0.55),(0.45,0.55),(0.44,0.56),(0.42,0.58)]:
    h = 2e-4
    xm0, xp0 = band_ends(a, b, 4.0)
    xm_a, xp_a = band_ends(a+h, b, 4.0)
    xm_b, xp_b = band_ends(a, b+h, 4.0)
    print(f"  (a,b)=({a},{b}): x_-={xm0:.5f} x_+={xp0:.5f} | dx-/da={ (xm_a-xm0)/h:+.3f} "
          f"dx+/da={(xp_a-xp0)/h:+.3f} dx-/db={(xm_b-xm0)/h:+.3f} dx+/db={(xp_b-xp0)/h:+.3f}")

print()
print("g1(a)-a along branch:")
for Rstr in ["R=1.05","R=2","R=4","R=10","R=100","R=1000"]:
    rec = data[Rstr]
    aa = np.array(rec["agrid"]); gg = np.array(rec["g1"])
    diffs = gg - aa
    print(f"  {Rstr}: min(g1-a)={diffs.min():+.4e} max(g1-a)={diffs.max():+.4e} at a={aa[np.argmin(diffs)]:.4f}")

print()
print("R1(a, a+) sign along diagonal:")
for R in [1.05, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4]:
    h = 1e-5
    row = []
    for a in [0.43, 0.45, 0.48, 0.5, 0.55]:
        if a >= 0.5: continue
        r1 = F.R1R2(a, a+h, R)[0]
        row.append(f"a={a}:{r1:+.2e}")
    print(f"  R={R:7g}: " + " ".join(row))
