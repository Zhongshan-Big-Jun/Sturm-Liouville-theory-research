import json, numpy as np
d = json.load(open("runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility/e14c_1000.json"))
rows = d["rows"]
valid = [r for r in rows if np.isfinite(r[1])]
print("nrows=%d nvalid=%d A=[%.6f,%.6f]" % (len(rows), len(valid), d["A_left"], d["A_right"]))
print("first 6 valid rows:")
for r in valid[:6]:
    print("  ", ["%.6f" % x if np.isfinite(x) else "NaN" for x in r])
print("rows 0..14 (raw):")
for r in rows[:15]:
    print("  ", ["%.6f" % x if np.isfinite(x) else "NaN" for x in r])
g = [(r[0], r[2]) for r in valid if np.isfinite(r[2])]
im = min(range(len(g)), key=lambda i: g[i][1])
print("g1p min: a=%.6f g1p=%.6f" % g[im])
hv = [r for r in valid if np.isfinite(r[5])]
print("h endpoints: h(first)=%.6f at a=%.6f ; h(last)=%.6f at a=%.6f" % (hv[0][5], hv[0][0], hv[-1][5], hv[-1][0]))
