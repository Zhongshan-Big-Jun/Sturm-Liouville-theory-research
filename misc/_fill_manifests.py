# -*- coding: utf-8 -*-
import io, os, json, hashlib

ROOT = r"F:\LaTeX\BVE research"

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

def sha256(path):
    h = hashlib.sha256()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

runs = {
    "R-20260806T011500Z-keylemma-E58FB1": "Q-20260806-keylemma-E58FB1",
    "R-20260806T011500Z-o3abranch-E8E56F": "Q-20260806-o3a-branch-E8E56F",
    "R-20260806T011500Z-o1audit-422A69": "Q-20260806-o1-audit-422A69",
}

# fill run manifests with packet sha256
for run_id, task_id in runs.items():
    mp = os.path.join(ROOT, "runs", "rigorous-open-math-research", run_id, "run-manifest.json")
    m = json.loads(read_utf8(mp))
    pp = os.path.join(ROOT, "agenda", "task-packets", task_id + ".md")
    m["task_packet_sha256"] = sha256(pp)
    write_utf8(mp, json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    print(run_id, "packet sha256:", m["task_packet_sha256"][:16])

# state/current.json add third run
p = os.path.join(ROOT, "state", "current.json")
cur = json.loads(read_utf8(p))
cur["active_run_ids"] = list(runs.keys())
cur["active_task_ids"] = list(runs.values())
cur["latest_checkpoint"] = "state/checkpoints/2026-08-06T012500Z--gapn1-dispatch3.md"
cur["last_updated"] = "2026-08-06T01:25:00Z"
write_utf8(p, json.dumps(cur, ensure_ascii=False, indent=2) + "\n")

# checkpoint update (dispatch3)
cp = """# Checkpoint: gap-n1 dispatch v3 (2026-08-06T01:25Z)

## Run status (verbatim)
RIGOROUS_PARTIAL_RESULT (unchanged; three runs in progress)

## Completed this stage
- Dispatched three parallel rigorous-open-math-research runs:
  * KEY LEMMA closure (Jason, R-20260806T011500Z-keylemma-E58FB1)
  * O3a Lemmas A-C (Pascal, R-20260806T011500Z-o3abranch-E8E56F)
  * O1 draft independent audit (Copernicus, R-20260806T011500Z-o1audit-422A69)
- Task packets contain project context only (no theorem contract, no route prescription).
- Run manifests filled with task-packet sha256.

## Active items
- KEY LEMMA open (delegated); O3a Lemmas A-C open (delegated); O1 audit (delegated).
- INF R->inf limit proof open (D*R -> 24.943866).

## Blockers
- None.

## Next commands / files
- Wait for agents; then ingest (preserve upstream status verbatim; index artifacts).
- Revalidate: python C:\\Users\\HuangZY\\.codex\\skills\\manage-math-research-program\\scripts\\validate_project.py F:\\LaTeX\\BVE research
- Resume: read state/RESUME.md
"""
write_utf8(os.path.join(ROOT, "state", "checkpoints", "2026-08-06T012500Z--gapn1-dispatch3.md"), cp)
print("done")