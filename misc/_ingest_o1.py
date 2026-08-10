# -*- coding: utf-8 -*-
import io, os, json, hashlib, glob

ROOT = r"F:\LaTeX\BVE research"
RUN = "R-20260806T011500Z-o1audit-422A69"
TASK = "Q-20260806-o1-audit-422A69"
RUNROOT = os.path.join(ROOT, "runs", "rigorous-open-math-research", RUN)

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

def sha16(path):
    h = hashlib.sha256()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:16=" + h.hexdigest()[:16]

# artifact hashes
art = {}
for p in sorted(glob.glob(os.path.join(RUNROOT, "**", "*"), recursive=True)):
    if os.path.isfile(p):
        rel = os.path.relpath(p, RUNROOT).replace("\\", "/")
        if rel.startswith("reproducibility/__pycache__"):
            continue
        art[rel] = sha16(p)
print(json.dumps(art, ensure_ascii=False, indent=1))

# index/runs.json
p = os.path.join(ROOT, "index", "runs.json")
runs = json.loads(read_utf8(p))
runs["items"].append({
    "run_id": RUN, "task_id": TASK, "problem_id": "O-2026-SL-GAP-3B7A2C",
    "run_root": "runs/rigorous-open-math-research/" + RUN,
    "started_at": "2026-08-06T01:20:00Z", "completed_at": "2026-08-06T03:05:00Z",
    "manager_ingestion_state": "ingested",
    "upstream_status_verbatim": "RIGOROUS_PARTIAL_RESULT (O1 audit: statement TRUE, draft REPAIRABLE_GAP; O1a PARTIAL, O1b FAILED-as-stated, O1c/O1d/O1e/O1f PROVED)",
    "artifacts": art,
    "deliverables": ["audit_report.md (逐条裁决 O1a-O1f)", "candidate_proof.md (修复清单 R1-R4)", "reproducibility/verify_o1_audit*.py + _out.json"],
    "exact_remaining_gaps": ["O1a: 用 S_rho=rho^(1/2) T_rho rho^(1/2) 修复自伴性论证", "O1b: FH 跳点导数符号修正为 dD/deps = -(c_+-c_-)f(x_j)", "草稿修订 + 复审"]
})
runs["updated_at"] = "2026-08-06T03:05:00Z"
write_utf8(p, json.dumps(runs, ensure_ascii=False, indent=2) + "\n")

# index/artifacts.json
p = os.path.join(ROOT, "index", "artifacts.json")
arts = json.loads(read_utf8(p))
for rel, h in art.items():
    arts["items"].append({
        "artifact_id": "A-" + RUN + "-" + hashlib.sha256(rel.encode()).hexdigest()[:6].upper(),
        "run_id": RUN, "path": "runs/rigorous-open-math-research/" + RUN + "/" + rel,
        "sha256_16": h, "created_at": "2026-08-06", "kind": "upstream_artifact"
    })
arts["updated_at"] = "2026-08-06T03:05:00Z"
write_utf8(p, json.dumps(arts, ensure_ascii=False, indent=2) + "\n")

# index/task-packets.json
p = os.path.join(ROOT, "index", "task-packets.json")
tp = json.loads(read_utf8(p))
for it in tp["items"]:
    if it["task_id"] == TASK:
        it["state"] = "INGESTED"
tp["updated_at"] = "2026-08-06T03:05:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")

# index/open-problems.json: note audit result on the portfolio record
p = os.path.join(ROOT, "index", "open-problems.json")
ops = json.loads(read_utf8(p))
for it in ops["items"]:
    if it["problem_id"] == "O-2026-SL-GAP-3B7A2C":
        it["state"] = "DELEGATED"
        it["last_run_id"] = RUN
        it["note"] = "O1 audit ingested: statement TRUE, draft REPAIRABLE_GAP (O1a operator repair, O1b FH sign)"
ops["updated_at"] = "2026-08-06T03:05:00Z"
write_utf8(p, json.dumps(ops, ensure_ascii=False, indent=2) + "\n")

# state/current.json: next actions updated
p = os.path.join(ROOT, "state", "current.json")
cur = json.loads(read_utf8(p))
cur["next_actions"] = [
    "1. O1 草稿按审计 R1-R4 修订 (S_rho 算子修正 + FH 符号), 之后复审 (O4)",
    "2. ingest KEY LEMMA run (Jason) 与 O3a run (Pascal); 保留上游状态 verbatim",
    "3. 若 KEY LEMMA PROVED: 合流 O1+O2+O3a+O3b 撰写 docs/SL_gap_n1_proof.tex",
    "4. INF R->inf 极限严格证明 (D*R -> 24.943866)"
]
cur["last_updated"] = "2026-08-06T03:05:00Z"
write_utf8(p, json.dumps(cur, ensure_ascii=False, indent=2) + "\n")

# activity.jsonl
act = {"activity_id": "ACT-20260806-009",
    "started_at": "2026-08-06T03:05:00Z", "ended_at": "2026-08-06T03:20:00Z",
    "effective_minutes": 15, "category": "ingestion",
    "related_ids": [TASK, RUN, "O-2026-SL-GAP-3B7A2C"],
    "artifacts_created_or_updated": ["index/runs.json", "index/artifacts.json",
        "index/task-packets.json", "index/open-problems.json", "state/current.json",
        "state/activity.jsonl", "AGENTS.md"],
    "summary": "Ingested O1 audit run: status RIGOROUS_PARTIAL_RESULT preserved verbatim; "
        "O1a PARTIAL (operator repair S_rho), O1b FAILED-as-stated (FH sign), O1c-e PROVED; "
        "draft unchanged; repair list R1-R4 recorded.",
    "evidence": ["audit_report.md", "candidate_proof.md", "artifact hashes"],
    "recorded_by": "coordinator", "notes": "estimate"}
p = os.path.join(ROOT, "state", "activity.jsonl")
with io.open(p, "a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(act, ensure_ascii=False) + "\n")

print("INGESTED")