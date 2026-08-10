import json, io
p = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A\research_cache\sun2022_openalex.json"
d = json.loads(io.open(p, encoding="utf-8-sig").read())
idx = d.get("abstract_inverted_index")
print("has abstract_inverted_index:", idx is not None)
if idx:
    pos = {}
    for w, ps in idx.items():
        for pp in ps:
            pos[pp] = w
    words = [pos[k] for k in sorted(pos)]
    print(" ".join(words))
print("cited_by_count:", d.get("cited_by_count"))
print("topics:", [t.get("display_name") for t in d.get("topics", [])])
