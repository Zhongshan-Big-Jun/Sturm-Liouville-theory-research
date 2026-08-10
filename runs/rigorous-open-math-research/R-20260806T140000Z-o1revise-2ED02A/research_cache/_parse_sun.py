import json, io
p = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A\research_cache\sun2022_zbmath.json"
out = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A\research_cache\sun2022_zbmath_parsed.txt"
d = json.loads(io.open(p, encoding="utf-8-sig").read())
res = d.get("result", [])
buf = []
buf.append("num results: %d" % len(res))
for doc in res:
    buf.append("="*80)
    buf.append("id: %s | title: %s" % (doc.get("id"), doc.get("title")))
    buf.append("authors: %s" % (doc.get("contributors", {}).get("authors")))
    pub = doc.get("publication") or {}
    buf.append("publication: %s" % pub)
    buf.append("year: %s | document_url: %s" % (doc.get("year"), doc.get("document_url")))
    buf.append("-- review --")
    for ec in doc.get("editorial_contributions", []):
        buf.append("reviewer: %s | sign: %s" % (ec.get("reviewer"), ec.get("sign")))
        buf.append(ec.get("text", ""))
    buf.append("-- abstract --")
    buf.append(doc.get("abstract") or "(no abstract)")
    buf.append("-- references --")
    for r_ in doc.get("references", []):
        buf.append(json.dumps(r_, ensure_ascii=False))
    buf.append("-- class/msc --")
    buf.append("msc: %s" % (doc.get("msc") or doc.get("classification") or "?"))
    buf.append("keywords: %s" % (doc.get("keywords") or "?"))
    # any field that might mention S1/S2
    for k, v in doc.items():
        s = json.dumps(v, ensure_ascii=False)
        if "S1" in s or "S2" in s:
            buf.append("FIELD %s mentions S1/S2: %s" % (k, s[:800]))
io.open(out, "w", encoding="utf-8").write("\n".join(buf))
print("done; chars:", sum(len(b) for b in buf))
