import json, io, os, re, hashlib
root = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A"
# 1. manifest JSON validity + ASCII-only
mp = os.path.join(root, "run-manifest.json")
raw = io.open(mp, encoding="utf-8-sig").read()
d = json.loads(raw)
print("manifest JSON valid; status:", d["upstream_status_verbatim"], "| completed_at:", d["completed_at"], "| ingestion:", d["manager_ingestion_state"])
non = [c for c in raw if ord(c) > 127]
print("manifest non-ASCII:", len(non))
# 2. ASCII-only check on the markdown deliverables (they are English-language artifacts)
for fn in ["candidate_proof.md", "audit_report.md", "problem_contract.md", "obligation_graph.md", "approach_registry.md", "research_ledger.md", "counterexample_log.md", "status_and_literature.md", "repro_manifest.md"]:
    t = io.open(os.path.join(root, fn), encoding="utf-8").read()
    na = sorted({c for c in t if ord(c) > 127})
    print("ASCII check", fn, "->", "OK" if not na else na[:5])
# 3. verify hashes recorded in manifest match current files
for art in d["artifacts"]:
    if art["sha256"]:
        cur = hashlib.sha256(io.open(os.path.join(root, art["path"]), "rb").read()).hexdigest().upper()
        print("hash match" if cur == art["sha256"] else "HASH MISMATCH", art["path"], cur == art["sha256"])
