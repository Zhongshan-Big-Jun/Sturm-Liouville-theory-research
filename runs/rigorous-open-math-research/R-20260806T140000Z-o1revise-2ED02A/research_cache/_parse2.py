import json, io, glob, os
base = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A\research_cache"
for fn in ["qi2020.json", "sun_subelliptic.json"]:
    p = os.path.join(base, fn)
    d = json.loads(io.open(p, encoding="utf-8-sig").read())
    print("="*90)
    print("FILE:", fn)
    for doc in d.get("result", []):
        print("id:", doc.get("id"))
        t = doc.get("title") or {}
        print("title:", t.get("title"))
        auths = doc.get("contributors", {}).get("authors", [])
        print("authors:", [a.get("name") for a in auths])
        print("year:", doc.get("year"))
        print("msc:", doc.get("msc"))
        print("-- review text --")
        for ec in doc.get("editorial_contributions", []):
            print(ec.get("text", ""))
        print("-- references (zbmath ids) --")
        for r_ in doc.get("references", []):
            zb = r_.get("zbmath") or {}
            print("  year=%s codes=%s docid=%s msc=%s" % (zb.get("year"), zb.get("author_codes"), zb.get("document_id"), zb.get("msc")))
