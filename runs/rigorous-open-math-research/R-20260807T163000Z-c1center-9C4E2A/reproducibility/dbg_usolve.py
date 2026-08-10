import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
import importlib
import e15_authoritative as e15
importlib.reload(e15)
from c1trace_lib import R1R2, a_fp, A0, B0, partials

R = 1000.0
fp = a_fp(R)
a_min, a_max = e15.trace_extent(R)
print("extent: a_min=%.6f a_max=%.6f" % (a_min, a_max))
# rebuild a profile-like table: rows on [A_left, A_right]
A_left = max(A0, a_min); A_right = min(a_max, B0)
agrid = np.linspace(A_left, A_right, 21)
rows = []
bprev = None
for a in agrid:
    if bprev is None:
        lo, hi = A_left - 0.02, 1.0
    else:
        lo, hi = max(0.0, bprev - 0.05), min(1.0, bprev + 0.05)
    b = e15.max_root_col(float(a), R, lo, hi)
    rows.append((float(a), b))
    if b is not None: bprev = b
pts = [(r[0], r[1]) for r in rows if r[1] is not None]
aa = np.array([p[0] for p in pts]); bb = np.array([p[1] for p in pts])
print("bb monotone:", np.all(np.diff(bb) > 0), "aa range [%.4f, %.4f], bb range [%.4f, %.4f]" % (aa.min(), aa.max(), bb.min(), bb.max()))
y = 1.0 - A0
print("y=%.6f  bb.min=%.6f bb.max=%.6f" % (y, bb.min(), bb.max()))
u = float(np.interp(y, bb, aa))
print("u0=%.6f" % u)
dbb = np.gradient(bb, aa)
for _ in range(25):
    bu = float(np.interp(u, aa, bb)); sl = float(np.interp(u, aa, dbb))
    du = (y - bu)/sl
    u = u + du
    if abs(du) < 1e-12: break
print("u after table-newton: %.8f" % u)
print("check b(u)=%.6f vs y=%.6f" % (float(np.interp(u, aa, bb)), y))
