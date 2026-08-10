# -*- coding: utf-8 -*-
import io, os, json, hashlib, glob

ROOT = r"F:\LaTeX\BVE research"
RUN = "R-20260806T070000Z-keylemma2b-0A6D8F"
TASK = "Q-20260806-keylemma2b-0A6D8F"
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
        if rel.startswith("reproducibility/__pycache__") or rel.startswith("reproducibility/cert_reeval_output/__pycache__"):
            continue
        art[rel] = sha16(p)
print("artifacts:", len(art))

# index/runs.json
p = os.path.join(ROOT, "index", "runs.json")
runs = json.loads(read_utf8(p))
runs["items"].append({
    "run_id": RUN, "task_id": TASK, "problem_id": "O-2026-SL-GAP-3B7A2C",
    "run_root": "runs/rigorous-open-math-research/" + RUN,
    "started_at": "2026-08-06T07:00:00Z", "completed_at": "2026-08-06T13:00:00Z",
    "manager_ingestion_state": "ingested",
    "upstream_status_verbatim": "CANDIDATE_COMPLETE_PROOF (KEY LEMMA (LOG)^(FP) proven; R1/R2/L4box/L5box closed; four interval certificates independently re-verified; upgrade to INDEPENDENTLY_AUDITED_PROOF needs second independent audit or formalization)",
    "artifacts": art,
    "deliverables": ["candidate_proof.md (KEY LEMMA 完整证明)", "audit_report.md", "reproducibility/ 15 脚本 + 独立引擎复验", "cert_reeval_output/ fresh 捕获"],
    "exact_remaining_gaps": [
        "KEY LEMMA 证明无缺口 (run 自审)",
        "升级为 INDEPENDENTLY_AUDITED_PROOF 需第二独立实体审计或形式化",
        "非承重注意: riarith.iv_sqrt 非严格外舍入 (符号结论由 mpmath.iv 独立重导, 不承重); C4 曲线恒等式 IN=A*K(v) 未完全符号归零; 区间引擎未形式化"
    ],
    "resumes": "R-20260806T050000Z-keylemma2-5A35E5"
})
runs["updated_at"] = "2026-08-06T13:05:00Z"
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
arts["updated_at"] = "2026-08-06T13:05:00Z"
write_utf8(p, json.dumps(arts, ensure_ascii=False, indent=2) + "\n")

# index/task-packets.json
p = os.path.join(ROOT, "index", "task-packets.json")
tp = json.loads(read_utf8(p))
for it in tp["items"]:
    if it["task_id"] == TASK:
        it["state"] = "INGESTED"
tp["updated_at"] = "2026-08-06T13:05:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")

# index/open-problems.json
p = os.path.join(ROOT, "index", "open-problems.json")
ops = json.loads(read_utf8(p))
for it in ops["items"]:
    if it["problem_id"] == "O-2026-SL-GAP-3B7A2C":
        it["state"] = "DELEGATED"
        it["last_run_id"] = RUN
        it["note"] = "KEY LEMMA candidate complete proof ingested (CANDIDATE_COMPLETE_PROOF); O2 closes pending independent audit; O3a C1 open; O1 revision pending"
ops["updated_at"] = "2026-08-06T13:05:00Z"
write_utf8(p, json.dumps(ops, ensure_ascii=False, indent=2) + "\n")

# activity.jsonl
act = {"activity_id": "ACT-20260806-013",
    "started_at": "2026-08-06T13:00:00Z", "ended_at": "2026-08-06T13:10:00Z",
    "effective_minutes": 10, "category": "ingestion",
    "related_ids": [TASK, RUN, "O-2026-SL-GAP-3B7A2C"],
    "artifacts_created_or_updated": ["index/runs.json", "index/artifacts.json",
        "index/task-packets.json", "index/open-problems.json", "state/activity.jsonl"],
    "summary": "Ingested KEYLEMMA2b run: CANDIDATE_COMPLETE_PROOF verbatim; KEY LEMMA (LOG)^(FP) "
        "proven, R1/R2/L4box/L5box closed; certificates independently re-verified by second engine; "
        "upgrade to INDEPENDENTLY_AUDITED_PROOF requires second independent audit.",
    "evidence": ["candidate_proof.md", "audit_report.md", "cert_reeval_output/*_rerun.txt"],
    "recorded_by": "coordinator", "notes": "estimate"}
p = os.path.join(ROOT, "state", "activity.jsonl")
with io.open(p, "a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(act, ensure_ascii=False) + "\n")

print("INGESTED")