import io, os, json, hashlib
root = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o1revise-2ED02A"
mp = os.path.join(root, "run-manifest.json")
d = json.loads(io.open(mp, encoding="utf-8").read())
fix = {
    "problem_contract.md": "F37D3D692C736FDB1B5D848F938227E4E1BE65B1A73439D8370842E393DB7FBC",
    "obligation_graph.md": "14F33F80EF9DA8EB3B641E9E45AFC061279C57E1B8CD51A2A315419903E153A8",
    "approach_registry.md": "34E26E68D95DE385B188AA34D0B87121D56483738E2B7E519EFC2B02F201188B",
    "counterexample_log.md": "FF29A92D45558EE309C0E02F923A8A35A5713B759BBAE5B7DB748292EDD53366",
}
for art in d["artifacts"]:
    if art["path"] in fix:
        art["sha256"] = fix[art["path"]]
io.open(mp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
# strip BOMs from scratch scripts in research_cache
for fn in os.listdir(os.path.join(root, "research_cache")):
    p = os.path.join(root, "research_cache", fn)
    if os.path.isfile(p):
        b = open(p, "rb").read()
        if b.startswith(b"\xef\xbb\xbf"):
            open(p, "wb").write(b[3:])
# verify all recorded hashes
ok = True
for art in d["artifacts"]:
    if art["sha256"] and not art["sha256"].startswith("REFRESH"):
        cur = hashlib.sha256(open(os.path.join(root, art["path"]), "rb").read()).hexdigest().upper()
        if cur != art["sha256"]:
            ok = False
            print("MISMATCH", art["path"], cur)
print("ALL HASHES MATCH:", ok)
print("run-manifest final hash:", hashlib.sha256(open(mp, "rb").read()).hexdigest().upper())
