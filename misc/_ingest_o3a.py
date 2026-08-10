# -*- coding: utf-8 -*-
import io, os, json, hashlib, glob

ROOT = r"F:\LaTeX\BVE research"
RUN = "R-20260806T011500Z-o3abranch-E8E56F"
TASK = "Q-20260806-o3a-branch-E8E56F"
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

art = {}
for p in sorted(glob.glob(os.path.join(RUNROOT, "**", "*"), recursive=True)):
    if os.path.isfile(p):
        rel = os.path.relpath(p, RUNROOT).replace("\\", "/")
        if rel.startswith("reproducibility/__pycache__"):
            continue
        art[rel] = sha16(p)
print("artifacts:", len(art))

# index/runs.json
p = os.path.join(ROOT, "index", "runs.json")
runs = json.loads(read_utf8(p))
runs["items"].append({
    "run_id": RUN, "task_id": TASK, "problem_id": "O-2026-SL-GAP-3B7A2C",
    "run_root": "runs/rigorous-open-math-research/" + RUN,
    "started_at": "2026-08-06T01:15:00Z", "completed_at": "2026-08-06T06:10:00Z",
    "manager_ingestion_state": "ingested",
    "upstream_status_verbatim": "RIGOROUS_PARTIAL_RESULT (Lemma A STRICTLY FALSIFIED by interval certificate at R=1500/1e4; O3a itself NOT refuted; P1-P4 PROVED; corrected conjecture C1 open)",
    "artifacts": art,
    "deliverables": ["candidate_proof.md (P1-P4 + C1 猜想)", "counterexample_log.md (CE-1 严格证书)", "audit_report.md (G1 closed, G2-G4 open)", "reproducibility/cert_ce1.py + output"],
    "exact_remaining_gaps": [
        "G2: 证明 C1 (h=g1-g2 单零点), 即 O3a",
        "G3: Lemma B/C 按修正陈述 (单图分支 + 覆盖, 排除多片 Gamma_2)",
        "G4: 大 R 时 h(b0) 与负 h' 凹陷间距恒正 (h(b0) ~ 0.38/sqrt(R), |min h'| 有界 ~4e-3)",
        "关键负结果: Lemma A (g1'>g2' R 一致下界) 为假, 阈值 R* ~1350; T4 路线对 R>=~1400 失效"
    ]
})
runs["updated_at"] = "2026-08-06T06:10:00Z"
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
arts["updated_at"] = "2026-08-06T06:10:00Z"
write_utf8(p, json.dumps(arts, ensure_ascii=False, indent=2) + "\n")

# index/task-packets.json
p = os.path.join(ROOT, "index", "task-packets.json")
tp = json.loads(read_utf8(p))
for it in tp["items"]:
    if it["task_id"] == TASK:
        it["state"] = "INGESTED"
tp["updated_at"] = "2026-08-06T06:10:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")

# index/open-problems.json
p = os.path.join(ROOT, "index", "open-problems.json")
ops = json.loads(read_utf8(p))
for it in ops["items"]:
    if it["problem_id"] == "O-2026-SL-GAP-3B7A2C":
        it["state"] = "DELEGATED"
        it["last_run_id"] = RUN
        it["note"] = "O3a run ingested: Lemma A FALSIFIED (R>=~1350); O3a itself NOT refuted; corrected conjecture C1 (h single zero) is the new target"
ops["updated_at"] = "2026-08-06T06:10:00Z"
write_utf8(p, json.dumps(ops, ensure_ascii=False, indent=2) + "\n")

# activity.jsonl
act = {"activity_id": "ACT-20260806-011",
    "started_at": "2026-08-06T06:10:00Z", "ended_at": "2026-08-06T06:20:00Z",
    "effective_minutes": 10, "category": "ingestion",
    "related_ids": [TASK, RUN, "O-2026-SL-GAP-3B7A2C"],
    "artifacts_created_or_updated": ["index/runs.json", "index/artifacts.json",
        "index/task-packets.json", "index/open-problems.json", "state/activity.jsonl"],
    "summary": "Ingested O3a run: Lemma A strictly falsified by interval certificate (R=1500/1e4, "
        "h'(a*)<0); P1-P4 PROVED; O3a not refuted; corrected conjecture C1 (h single zero) is new "
        "target; multi-sheet Gamma_2 structure discovered.",
    "evidence": ["candidate_proof.md", "counterexample_log.md CE-1", "audit_report.md G1-G4", "cert_ce1.py"],
    "recorded_by": "coordinator", "notes": "estimate"}
p = os.path.join(ROOT, "state", "activity.jsonl")
with io.open(p, "a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(act, ensure_ascii=False) + "\n")

print("INGESTED")