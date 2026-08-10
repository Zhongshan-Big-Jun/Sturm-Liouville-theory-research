# -*- coding: utf-8 -*-
import io, os, glob

ROOT = r"F:\LaTeX\BVE research"
bad = []
count = 0
for d in ["state", "index", "tools", "agenda", "literature", "knowledge", "runs", "docs"]:
    base = os.path.join(ROOT, d)
    if not os.path.isdir(base):
        continue
    for p in glob.glob(os.path.join(base, "**", "*"), recursive=True):
        if not os.path.isfile(p) or not p.endswith((".md", ".json", ".jsonl")) or "__pycache__" in p:
            continue
        count += 1
        try:
            with io.open(p, "r", encoding="utf-8") as f:
                f.read()
        except UnicodeDecodeError as e:
            bad.append((os.path.relpath(p, ROOT), str(e)[:60]))
print("scanned:", count, "bad:", len(bad))
for rel, err in bad[:20]:
    print("  BAD:", rel, "|", err)