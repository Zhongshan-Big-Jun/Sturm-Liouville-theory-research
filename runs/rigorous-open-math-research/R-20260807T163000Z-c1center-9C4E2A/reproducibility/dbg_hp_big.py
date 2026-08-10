import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import R1R2, a_fp, A0, B0, partials

def arm_b_at(a, R, b_guess):
    # Newton refine b on R1=0 from guess
    b = b_guess
    for _ in range(30):
        R1a, R1b, R2a, R2b = partials(a, b, R)
        R1 = R1R2(a, b, R)[4]
        if abs(R1b) < 1e-9: return None
        b2 = b - R1/R1b
        if not (a+1e-9 < b2 < 1-1e-9): return None
        b = b2
        if abs(b2-b) < 1e-14: break
    return b if abs(R1R2(a, b, R)[4]) < 1e-9 else None

# compute h, hp, Phi on the arm over the domain for very large R using direct root-following
def profile_big(R, a_left, a_right, n=300):
    cache = {}
    # start from fp, walk up and down in a to build (aa, bb) table
    fp = a_fp(R, cache=cache)
    pts = []
    a, b = fp, 1-fp
    step = (a_right - fp)/n
    for k in range(int((a_right-fp)/step)+1):
        a_new = a + step
        rs = [r for r in np.linspace(b-0.1, min(1-1e-6, b+0.1), 401) if r > a_new+1e-6]
        # scan R1 over this window
        best = None
        for b0 in rs:
            b1 = arm_b_at(a_new, R, b0)
            if b1 is not None and (best is None or abs(b1-b) < abs(best-b)): best = b1
        if best is None: break
        pts.append((a_new, best)); a, b = a_new, best
    a, b = fp, 1-fp
    step = (fp - a_left)/n
    for k in range(int((fp-a_left)/step)+1):
        a_new = a - step
        best = None
        for b0 in np.linspace(max(1e-6, b-0.1), min(1-1e-6, b+0.1), 401):
            if b0 <= a_new: continue
            b1 = arm_b_at(a_new, R, b0)
            if b1 is not None and (best is None or abs(b1-b) < abs(best-b)): best = b1
        if best is None: break
        pts.append((a_new, best)); a, b = a_new, best
    pts.sort()
    aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
    # domain
    A_left = max(A0, aa.min()); A_right = min(aa.max(), B0)
    print("R=%g: arm a-range [%.6f, %.6f]; A=[%.6f, %.6f]" % (R, aa.min(), aa.max(), A_left, A_right))
    # h/Phi/hp on a-grid over J
    rows = []
    for a in np.linspace(A_left, A_right, n+1):
        y = 1-a
        if y < bb.min() or y > bb.max(): continue
        u = float(np.interp(y, bb, aa))
        # Newton refine u: g1(u) = y
        for _ in range(40):
            bu = float(np.interp(u, aa, bb))
            R1a, R1b, R2a, R2b = partials(u, bu, R)
            g1pu = -R1a/R1b
            if abs(g1pu) < 1e-12: break
            du = -(bu - y)/g1pu
            if not (aa.min()-1e-6 < u+du < aa.max()+1e-6): break
            u = u + du
            if abs(du) < 1e-13: break
        bu = float(np.interp(u, aa, bb))
        R1a, R1b, R2a, R2b = partials(u, bu, R)
        g1pu = -R1a/R1b
        b = float(np.interp(a, aa, bb))
        R1a, R1b, R2a, R2b = partials(a, b, R)
        g1p = -R1a/R1b
        Phi = g1p*g1pu; h = b - 1 + u; hp = g1p - 1/g1pu
        rows.append((a, b, g1p, u, Phi, h, hp))
    return rows

for R in [2000.0, 10000.0, 100000.0, 1e6]:
    rows = profile_big(R, 0.41, 0.60, n=200)
    hv = [r for r in rows if np.isfinite(r[5])]
    hps = [r[6] for r in hv]
    print("  h: [%.6f at a=%.5f] .. [%.6f at a=%.5f]; hp min=%.6f max=%.6f; h zeros=%d" %
          (hv[0][5], hv[0][0], hv[-1][5], hv[-1][0], min(hps), max(hps),
           sum(1 for i in range(len(hv)-1) if hv[i][5]*hv[i+1][5] < 0)))
    print("  g1p min=%.6f max=%.6f" % (min(r[2] for r in hv), max(r[2] for r in hv)))
