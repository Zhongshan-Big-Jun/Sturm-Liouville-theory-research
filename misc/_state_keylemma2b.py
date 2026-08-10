# -*- coding: utf-8 -*-
import io, os, json

ROOT = r"F:\LaTeX\BVE research"

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

# index/task-packets.json: mark interrupted keylemma2 task
p = os.path.join(ROOT, "index", "task-packets.json")
tp = json.loads(read_utf8(p))
for it in tp["items"]:
    if it["task_id"] == "Q-20260806-keylemma2-5A35E5":
        it["state"] = "CANCELLED"
        it["note"] = "run interrupted (agent lost); partial artifacts in run root; resumed by Q-20260806-keylemma2b-0A6D8F"
tp["updated_at"] = "2026-08-06T07:00:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")

# index/runs.json: note the interrupted run
p = os.path.join(ROOT, "index", "runs.json")
runs = json.loads(read_utf8(p))
for it in runs["items"]:
    if it["run_id"] == "R-20260806T050000Z-keylemma2-5A35E5":
        it["manager_ingestion_state"] = "interrupted_no_verdict"
        it["notes"] = "agent lost mid-write-up; certificates computed (unverified), ledger entries 1-6; resumed by R-20260806T070000Z-keylemma2b-0A6D8F"
runs["updated_at"] = "2026-08-06T07:00:00Z"
write_utf8(p, json.dumps(runs, ensure_ascii=False, indent=2) + "\n")

# state/current.json
p = os.path.join(ROOT, "state", "current.json")
cur = json.loads(read_utf8(p))
cur["current_stage"] = "gap-extremals-n1-keylemma-resume"
cur["active_run_id"] = "R-20260806T070000Z-keylemma2b-0A6D8F"
cur["active_run_ids"] = [
    "R-20260806T070000Z-keylemma2b-0A6D8F",
    "R-20260806T050000Z-keylemma2-5A35E5",
    "R-20260806T011500Z-keylemma-E58FB1",
    "R-20260806T011500Z-o3abranch-E8E56F",
    "R-20260806T011500Z-o1audit-422A69"
]
cur["active_task_ids"] = [
    "Q-20260806-keylemma2b-0A6D8F",
    "Q-20260806-keylemma2-5A35E5",
    "Q-20260806-keylemma-E58FB1",
    "Q-20260806-o3a-branch-E8E56F",
    "Q-20260806-o1-audit-422A69"
]
cur["latest_checkpoint"] = "state/checkpoints/2026-08-06T070500Z--keylemma2b-dispatch.md"
cur["next_actions"] = [
    "1. ingest KEYLEMMA2b run (Plato): 验证四个区间证书 + 完成 M2/CORNER/C4/L4box/L5box 解析证明 + 组装 candidate_proof/audit",
    "2. 若 KEY LEMMA 两形式 (LOG)^(FP) 闭合: 合流 O1(修订后)+O2+O3a+O3b 撰写 docs/SL_gap_n1_proof.tex",
    "3. O3a 修正猜想 C1 (h 单零点) 下一轮派发",
    "4. O1 修订 (R1-R4) + 复审 (O4)",
    "5. INF R->inf 极限严格证明 (D*R -> 24.943866)"
]
cur["run_status_verbatim"] = "RIGOROUS_PARTIAL_RESULT (KEY LEMMA residual nearly closed; four interval certificates computed, verification pending)"
cur["last_updated"] = "2026-08-06T07:05:00Z"
write_utf8(p, json.dumps(cur, ensure_ascii=False, indent=2) + "\n")

# checkpoint
cp = """# Checkpoint: gap-n1 KEYLEMMA2b dispatched (2026-08-06T07:05Z)

## Run status (verbatim)
- KEYLEMMA2b (R-20260806T070000Z-keylemma2b-0A6D8F): in progress (resume of interrupted run)
- KEY LEMMA (R-20260806T011500Z-keylemma-E58FB1): RIGOROUS_PARTIAL_RESULT (four inequalities)
- O3a (R-20260806T011500Z-o3abranch-E8E56F): RIGOROUS_PARTIAL_RESULT (Lemma A FALSIFIED; C1 open)
- O1 audit (R-20260806T011500Z-o1audit-422A69): RIGOROUS_PARTIAL_RESULT
- KEYLEMMA2 (R-20260806T050000Z-keylemma2-5A35E5): interrupted, no verdict; certificates unverified

## Completed this stage
- O3a run ingested (P1-P4 PROVED; Lemma A strictly falsified by interval certificate;
  corrected conjecture C1 = h single zero is the new O3a target).
- Interrupted KEYLEMMA2 run audited at manager level: ledger entries 1-6 recorded the
  (q,u) reformulation (IN >= 0 iff G2 >= 0), the M2 route (dIN/du < 0), CORNER and C4
  reductions, and four computed interval certificates (dM2dq worst -0.1902; L4box
  worst -4.6569; L5box worst +6.2429; C4 worst +2.4218). None independently verified.
- KEYLEMMA2b resume task dispatched (Plato) to verify certificates + complete proofs +
  assemble candidate_proof.md / audit_report.md.

## Active items
- KEY LEMMA residual closure (Plato in progress).
- O3a corrected conjecture C1 (next delegation).
- O1 revision (R1-R4) then re-audit.
- INF R->inf limit proof open.

## Blockers
- None.

## Next commands / files
- Wait for Plato; ingest with status verbatim.
- Resume: read state/RESUME.md
"""
write_utf8(os.path.join(ROOT, "state", "checkpoints", "2026-08-06T070500Z--keylemma2b-dispatch.md"), cp)

# activity.jsonl
act = {"activity_id": "ACT-20260806-012",
    "started_at": "2026-08-06T06:50:00Z", "ended_at": "2026-08-06T07:05:00Z",
    "effective_minutes": 15, "category": "task_packaging",
    "related_ids": ["Q-20260806-keylemma2b-0A6D8F", "R-20260806T070000Z-keylemma2b-0A6D8F",
        "R-20260806T050000Z-keylemma2-5A35E5", "O-2026-SL-GAP-3B7A2C"],
    "artifacts_created_or_updated": ["agenda/task-packets/Q-20260806-keylemma2b-0A6D8F.md",
        "runs/rigorous-open-math-research/R-20260806T070000Z-keylemma2b-0A6D8F/run-manifest.json",
        "index/task-packets.json", "index/runs.json", "state/current.json",
        "state/checkpoints/2026-08-06T070500Z--keylemma2b-dispatch.md"],
    "summary": "Audited interrupted KEYLEMMA2 run (certificates computed, unverified; ledger 1-6); "
        "dispatched resume run KEYLEMMA2b (Plato) to verify four interval certificates, complete "
        "M2/CORNER/C4/L4box/L5box proofs, assemble candidate_proof + audit; marked interrupted task "
        "CANCELLED in index.",
    "evidence": ["research_ledger.md", "certificate JSON summaries", "spawn result"],
    "recorded_by": "coordinator", "notes": "estimate"}
p = os.path.join(ROOT, "state", "activity.jsonl")
with io.open(p, "a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(act, ensure_ascii=False) + "\n")
print("done")