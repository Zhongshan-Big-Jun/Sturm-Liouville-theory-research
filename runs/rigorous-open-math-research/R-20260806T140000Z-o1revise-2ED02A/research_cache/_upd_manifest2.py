import io, os, json, hashlib
root = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest().upper()

new_hashes = {
    "candidate_proof.md": "728BD2B8D9F3AA9249B2E2A701006461AABC8154B18F47586A35677417254404",
    "research_ledger.md": "CB3719A9F327E440F5CC4D414084CA07A765D209CFB9F999FE75658B26F1981C",
    "status_and_literature.md": "6A196C64F81489506728B0D535F106B1986FB038F3A6D017672326001F6BEC6C",
    "repro_manifest.md": sha(os.path.join(root, "repro_manifest.md")),
}
print("new repro_manifest hash:", new_hashes["repro_manifest.md"])

mp = os.path.join(root, "run-manifest.json")
d = json.loads(io.open(mp, encoding="utf-8-sig").read())
for art in d["artifacts"]:
    if art["path"] in new_hashes:
        art["sha256"] = new_hashes[art["path"]]
d["notes"] = [n for n in d["notes"] if "completed in continuation" not in n]
d["notes"].append("completed in continuation session 2026-08-06: audit_report.md delivered (lost in the original session, see ledger R-010/R-012); candidate_proof.md corrected per audit finding F-001 and BOM-stripped; Sun 2022 novelty classification finalized in status_and_literature.md N1-N5; reproducibility spot re-runs bit-identical (R-013); all text artifacts BOM-stripped 2026-08-06")
io.open(mp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
print("run-manifest.json updated")
print("final run-manifest hash:", sha(mp))
