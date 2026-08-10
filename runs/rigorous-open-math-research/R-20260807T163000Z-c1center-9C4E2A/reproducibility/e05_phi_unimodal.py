# -*- coding: utf-8 -*-
"""e05_phi_unimodal.py: verify (U) Phi(a) = g1'(a) g1'(u(a)) unimodal max at fp.
Trace the fp-component b = g1(a) by Newton from the fp; compute Phi on a grid;
report monotonicity violations of Phi on [a0, fp] and [fp, beta]."""
import numpy as np, sys, json, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T200000Z-o3a-c1b-7F3A9B\reproducibility")
from c1_lib import residual, a_fp, cfg

def g1_trace(R, a0=0.4195, da=1e-4, extend=0.16):
    """Trace branch from fp left/right; returns sorted (a, b) lists."""
    fp = a_fp(R)
    b0 = 1 - fp
    # Newton for branch point at given a with initial b
    def solve_b(a, binit):
        b = binit
        for _ in range(60):
            r = residual(a, b, R, at='a')
            h = 1e-6
            rb = (residual(a, b+h, R, at='a') - residual(a, b-h, R, at='a'))/(2*h)
            if abs(rb) < 1e-14:
                break
            db = -r/rb
            b = np.clip(b + db, a+1e-9, 1-1e-9)
            if abs(db) < 1e-13:
                break
        return b
    pts = [(fp, b0)]
    # right side: a from fp to fp+extend
    a = fp
    b = b0
    while a < fp + extend:
        a += da
        if a >= 0.999: break
        b = solve_b(a, b)
        if not (a < b < 1): break
        pts.append((a, b))
    # left side
    a = fp
    b = b0
    while a > fp - extend:
        a -= da
        if a <= 0.001: break
        b = solve_b(a, b)
        if not (a < b < 1): break
        pts.append((a, b))
    pts.sort()
    return pts

def g1p(a, b, R, h=1e-6):
    """g1'(a) by finite difference of the branch (a, b(a)): slope db/da."""
    r = residual(a, b, R, at='a')
    ha = 1e-6
    # slope of branch: implicit -R1_a/R1_b
    def R1(aa, bb): return residual(aa, bb, R, at='a')
    R1a = (R1(a+ha, b) - R1(a-ha, b))/(2*ha)
    R1b = (R1(a, b+ha) - R1(a, b-ha))/(2*ha)
    return -R1a/R1b

def g1inv(target, pts):
    """invert g1 by bisection on the traced (a,b) table: find a with g1(a)=target."""
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
    # bb increasing? assume yes; bisect on a via interp-free search
    if not (np.diff(bb) > 0).all():
        return None, None
    lo, hi = aa[0], aa[-1]
    if not (bb[0] < target < bb[-1]):
        return None, None
    for _ in range(80):
        md = 0.5*(lo+hi)
        bmd = np.interp(md, aa, bb)
        if bmd < target:
            lo = md
        else:
            hi = md
    return 0.5*(lo+hi)

def analyze(R, da=1e-4, extend=0.16):
    pts = g1_trace(R, da=da, extend=extend)
    fp = a_fp(R)
    aa = [p[0] for p in pts]; bb = [p[1] for p in pts]
    # grid of a values
    grid = [aa[0]] + list(np.linspace(aa[0]+1e-4, aa[-1]-1e-4, 120)) + [aa[-1]]
    grid = sorted(set(round(float(x), 12) for x in grid))
    rows = []
    for a in grid:
        b = np.interp(a, aa, bb)
        gp = g1p(a, b, R)
        u = g1inv(1-a, pts)
        if u is None:
            rows.append((a, float(gp), None, None)); continue
        bu = np.interp(u, aa, bb)
        gpu = g1p(u, bu, R)
        Phi = gp*gpu
        rows.append((a, float(gp), float(u), float(Phi)))
    # monotonicity check on left (a < fp) and right (a > fp)
    left = [r for r in rows if r[0] < fp - 1e-9 and r[3] is not None]
    right = [r for r in rows if r[0] > fp + 1e-9 and r[3] is not None]
    viol_left = sum(1 for i in range(1, len(left)) if left[i][3] < left[i-1][3] - 1e-9)
    viol_right = sum(1 for i in range(1, len(right)) if right[i][3] > right[i-1][3] + 1e-9)
    Phi_fp = [r[3] for r in rows if abs(r[0]-fp) < 1e-4]
    return dict(R=R, fp=fp, a0=rows[0][0], beta=rows[-1][0],
                npts=len(rows), viol_left=viol_left, viol_right=viol_right,
                Phi_fp=float(Phi_fp[0]) if Phi_fp else None,
                Phi_a0=rows[0][3], Phi_beta=rows[-1][3],
                g1p_fp=float(rows[min(range(len(rows)), key=lambda i: abs(rows[i][0]-fp))][1]))

Rs = [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e6]
t0 = time.time()
out = {}
for R in Rs:
    try:
        rec = analyze(R)
        out[R] = rec
        print(f"R={R}: fp={rec['fp']:.5f} a0={rec['a0']:.5f} beta={rec['beta']:.5f} "
              f"Phi_fp={rec['Phi_fp']:.4f} Phi_a0={rec['Phi_a0'] if rec['Phi_a0'] is not None else None} "
              f"viol_L={rec['viol_left']} viol_R={rec['viol_right']}")
    except Exception as e:
        print(f"R={R}: FAILED {e}")
print("elapsed", round(time.time()-t0,1))
with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260807T163000Z-c1center-9C4E2A\reproducibility\phi_unimodal.json","w") as f:
    json.dump(out, f, indent=1, default=str)