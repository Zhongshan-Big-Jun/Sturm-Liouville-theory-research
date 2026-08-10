import json, io
p = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility\shape_v6.json"
d = json.load(io.open(p, encoding="utf-8-sig"))
keys = ["1.02","1.05","1.1","1.2","1.5","2.0","3.0","4.0","10.0","100.0","1000.0","1500.0","1e4","1e5","1e6"]
for k in keys:
    if k in d:
        v = d[k]
        print(k, "fp=",round(v.get("fp",float("nan")),6), "a_max1=",round(v.get("a_max1",float("nan")),6), "beta=",round(v.get("beta",float("nan")),6), "h_a0=",round(v.get("h_a0",float("nan")),6), "h_b0=",round(v.get("h_b0",float("nan")),6), "min_h_fp_beta=",round(v.get("min_h_fp_beta",float("nan")),6))