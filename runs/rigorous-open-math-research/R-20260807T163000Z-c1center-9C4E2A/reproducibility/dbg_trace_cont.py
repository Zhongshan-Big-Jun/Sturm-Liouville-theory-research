import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import R1R2, a_fp, A0, B0, partials, _newton_b, _bisect_b
from e14_authoritative import b_roots

# continuity trace: start at fp, walk in a with tiny steps, Newton in b, keep R1=0 root closest to previous b
def trace(R, a_lo, a_hi, nstep=600, cache=None):
    fp = a_fp(R, cache=cache)
    pts = [(fp, 1-fp)]
    a, b = fp, 1-fp
    step = (a_hi - fp)/nstep
    for k in range(nstep):
        a_new = a + step
        # all roots at a_new
        rs = [r for r in b_roots(a_new, R) if r > a_new]
        if not rs:
            break
        # pick the root closest to previous b
        b_new = min(rs, key=lambda r: abs(r - b))
        if abs(b_new - b) > 0.2:
            break
        pts.append((a_new, b_new)); a, b = a_new, b_new
    a, b = fp, 1-fp
    step = (fp - a_lo)/nstep
    for k in range(nstep):
        a_new = a - step
        rs = [r for r in b_roots(a_new, R) if r > a_new]
        if not rs:
            break
        b_new = min(rs, key=lambda r: abs(r - b))
        if abs(b_new - b) > 0.2:
            break
        pts.append((a_new, b_new)); a, b = a_new, b_new
    pts.sort()
    return pts

for R in [1000.0, 2000.0, 10000.0, 100000.0]:
    pts = trace(R, 0.0005, 0.9995, nstep=800)
    print("=== R=%g: %d points, a-range [%.6f, %.6f]" % (R, len(pts), pts[0][0], pts[-1][0]))
    for fr in [0.0, 0.2, 0.4, 0.6, 0.8, 0.95, 1.0]:
        i = int(fr*(len(pts)-1))
        a, b = pts[i]
        print("  a=%.5f b=%.5f b-a=%.6f" % (a, b, b-a))
    # check g1p along the traced arm over [a0, b0]
    cache = {}
    vals = []
    for a, b in pts:
        if a < A0 - 1e-9 or a > B0 + 1e-9:
            continue
        R1a, R1b, R2a, R2b = partials(a, b, R, cache=cache)
        vals.append((a, b, -R1a/R1b))
    g1p_arr = np.array([v[2] for v in vals])
    if len(g1p_arr):
        imin = int(np.argmin(g1p_arr))
        print("  g1p over [a0,b0]: min=%.6f at a=%.6f b=%.6f; max=%.6f" % (g1p_arr.min(), vals[imin][0], vals[imin][1], g1p_arr.max()))
    else:
        print("  no points in [a0,b0]")
