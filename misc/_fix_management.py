# -*- coding: utf-8 -*-
import json, os, io

ROOT = r"F:\LaTeX\BVE research"

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", path)

# 1. state/current.json: add project_id
p = os.path.join(ROOT, "state", "current.json")
with io.open(p, "r", encoding="utf-8-sig") as f:
    cur = json.load(f)
cur["project_id"] = "MRP-20260731-BVE-SL"
cur["last_updated"] = "2026-08-06T01:15:00Z"
write_utf8(p, json.dumps(cur, ensure_ascii=False, indent=2) + "\n")

# 2. index/open-problems.json: add problem_id to each item
p = os.path.join(ROOT, "index", "open-problems.json")
with io.open(p, "r", encoding="utf-8-sig") as f:
    ops = json.load(f)
for it in ops["items"]:
    it["problem_id"] = it["id"]
ops["updated_at"] = "2026-08-06T01:15:00Z"
write_utf8(p, json.dumps(ops, ensure_ascii=False, indent=2) + "\n")

# 3. index/tools.json: add canonical_key to the 3 items
p = os.path.join(ROOT, "index", "tools.json")
with io.open(p, "r", encoding="utf-8-sig") as f:
    tools = json.load(f)
keys = {
    "gap-n1-reduction": "gap extremal reduction to two-parameter barrier/well families (Dirichlet string, box class 1<=rho<=R)",
    "two-block-gap-bounds": "two-block gap bounds 3*pi^2/R < D < 3*pi^2 (Dirichlet string box class)",
    "key-lemma-decomposition": "key lemma decomposition G2-G1=(A-C)+(B-D) with exact corner limit 4*pi/(3*sqrt3)",
}
for it in tools["items"]:
    if it["tool_id"] in keys:
        it["canonical_key"] = keys[it["tool_id"]]
tools["updated_at"] = "2026-08-06T01:15:00Z"
write_utf8(p, json.dumps(tools, ensure_ascii=False, indent=2) + "\n")

# 4. state/activity.jsonl: strip BOM
p = os.path.join(ROOT, "state", "activity.jsonl")
with io.open(p, "r", encoding="utf-8-sig") as f:
    lines = f.read()
write_utf8(p, lines)

# 5. tool frontmatter canonical_key
for slug, key in keys.items():
    p = os.path.join(ROOT, "tools", slug + ".md")
    with io.open(p, "r", encoding="utf-8-sig") as f:
        txt = f.read()
    if "canonical_key:" not in txt.split("---")[1]:
        txt = txt.replace("---\n", "---\ncanonical_key: " + key + "\n", 1)
        write_utf8(p, txt)

print("DONE")