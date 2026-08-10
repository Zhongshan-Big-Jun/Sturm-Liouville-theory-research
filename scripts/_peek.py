import json, io
p = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility\shape_v6.json"
d = json.load(io.open(p, encoding="utf-8-sig"))
print(type(d))
if isinstance(d, dict):
    print(list(d.keys())[:20])
    for k in list(d.keys())[:2]:
        v = d[k]
        print(k, type(v), (list(v.keys())[:10] if isinstance(v, dict) else str(v)[:200]))