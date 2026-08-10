import json, numpy as np
d = json.load(open("runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility/e15_t1000.json"))
rows = d["rows"]
valid = [r for r in rows if np.isfinite(r[1])]
print("nvalid=%d (of %d)" % (len(valid), len(rows)))
for r in valid[:6]:
    print("  a=%.6f b=%.6f g1p=%.6f u=%.6f Phi=%.6f h=%.6f hp=%.6f" % tuple(r))
print("a_min=%.6f a_max=%.6f A=[%.6f,%.6f]" % (d["a_min"], d["a_max"], d["A_left"], d["A_right"]))
# check rows where u NaN (invalid h)
bad = [r for r in rows if not np.isfinite(r[5]) and np.isfinite(r[1])]
print("rows with b but no h: %d, e.g." % len(bad))
for r in bad[:5]:
    print("  a=%.6f b=%.6f" % (r[0], r[1]))
