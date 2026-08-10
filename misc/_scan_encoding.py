# -*- coding: utf-8 -*-
import io, os, glob

ROOT = r"F:\LaTeX\BVE research"
bad = []
count = 0
for p in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
    if not os.path.isfile(p):
        continue
    if not (p.endswith((".md", ".json", ".jsonl", ".tex", ".txt", ".py"))):
        continue
    if "__pycache__" in p or p.endswith((".pyc",)):
        continue
    count += 1
    try:
        with io.open(p, "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError as e:
        bad.append((os.path.relpath(p, ROOT), str(e)))
print("files scanned:", count, "bad:", len(bad))
for rel, err in bad[:40]:
    print("  BAD:", rel, "|", err)