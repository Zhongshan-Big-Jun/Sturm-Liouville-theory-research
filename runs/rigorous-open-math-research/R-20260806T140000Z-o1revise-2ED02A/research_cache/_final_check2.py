import json, io, os, hashlib
root = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A"
mp = os.path.join(root, "run-manifest.json")
raw = io.open(mp, encoding="utf-8").read()
d = json.loads(raw)
print("JSON valid; status:", d["upstream_status_verbatim"], "| completed:", d["completed_at"], "| ingestion:", d["manager_ingestion_state"])
print("non-ASCII in manifest:", sum(1 for c in raw if ord(c) > 127))
allok = True
for art in d["artifacts"]:
    if art["sha256"] and art["sha256"] != "REFRESHED-AT-CLOSURE":
        cur = hashlib.sha256(open(os.path.join(root, art["path"]), "rb").read()).hexdigest().upper()
        ok = cur == art["sha256"]
        allok = allok and ok
        print(("OK " if ok else "MISMATCH "), art["path"])
print("ALL HASHES MATCH:", allok)
# BOM scan across run root
bom = []
for dp, dn, fns in os.walk(root):
    for fn in fns:
        p = os.path.join(dp, fn)
        if open(p, "rb").read(3) == b"\xef\xbb\xbf":
            bom.append(os.path.relpath(p, root))
print("files with BOM:", bom)
# non-ASCII scan on the ASCII-intended markdown files
for fn in ["candidate_proof.md", "audit_report.md", "problem_contract.md", "obligation_graph.md", "approach_registry.md", "research_ledger.md", "counterexample_log.md", "status_and_literature.md", "repro_manifest.md"]:
    t = io.open(os.path.join(root, fn), encoding="utf-8").read()
    na = sorted({c for c in t if ord(c) > 127})
    if na:
        print("NON-ASCII in", fn, na[:5])
print("ASCII scan done")
