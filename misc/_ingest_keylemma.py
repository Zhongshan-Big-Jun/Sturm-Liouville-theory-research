# -*- coding: utf-8 -*-
import io, os, json, hashlib, glob

ROOT = r"F:\LaTeX\BVE research"
RUN = "R-20260806T011500Z-keylemma-E58FB1"
TASK = "Q-20260806-keylemma-E58FB1"
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
    "started_at": "2026-08-06T01:15:00Z", "completed_at": "2026-08-06T04:40:00Z",
    "manager_ingestion_state": "ingested",
    "upstream_status_verbatim": "RIGOROUS_PARTIAL_RESULT (KEY LEMMA reduced to four explicit inequalities R1, R2, L4box, L5box; bases B1-B5, B7 PROVED; audit REPAIRABLE_GAP)",
    "artifacts": art,
    "deliverables": ["candidate_proof.md (归约 + 基座证明)", "audit_report.md (缺口 G1-G4)", "reproducibility/keylemma_lib.py, verify_premises.py, final_check.py"],
    "exact_remaining_gaps": [
        "R1: G2 >= 0 for q >= 2, c in (0,1/2); tight at (2,1/2), slack 0.069",
        "R2: G2 >= 0 for q > 1, c in (0,0.4]; slack 0.415",
        "L4box: H' < 0 on (1,2]x[0.4,0.5]; slack 7.7",
        "L5box: F~'' > 0 on (1,2]x[0.4,0.5]; slack 14.2",
        "关键开放核心 Q1: dG2/dq >= 0 (全域数值成立) 可把 R1/R2 归约到一维边界 B6/B7"
    ],
    "corrections": ["C1: (LOG) 形式与 (FP) 形式并非逻辑等价; T4 只消费 (FP); 本 run 分别证明两者"]
})
runs["updated_at"] = "2026-08-06T04:45:00Z"
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
arts["updated_at"] = "2026-08-06T04:45:00Z"
write_utf8(p, json.dumps(arts, ensure_ascii=False, indent=2) + "\n")

# index/task-packets.json
p = os.path.join(ROOT, "index", "task-packets.json")
tp = json.loads(read_utf8(p))
for it in tp["items"]:
    if it["task_id"] == TASK:
        it["state"] = "INGESTED"
tp["updated_at"] = "2026-08-06T04:45:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")

# index/open-problems.json
p = os.path.join(ROOT, "index", "open-problems.json")
ops = json.loads(read_utf8(p))
for it in ops["items"]:
    if it["problem_id"] == "O-2026-SL-GAP-3B7A2C":
        it["state"] = "DELEGATED"
        it["last_run_id"] = RUN
        it["note"] = "KEY LEMMA run ingested: reduced to R1/R2/L4box/L5box (all numerically verified, margins 0.069/0.415/7.7/14.2); bases B1-B5,B7 PROVED; C1: LOG != FP forms"
ops["updated_at"] = "2026-08-06T04:45:00Z"
write_utf8(p, json.dumps(ops, ensure_ascii=False, indent=2) + "\n")

# activity.jsonl
act = {"activity_id": "ACT-20260806-010",
    "started_at": "2026-08-06T04:40:00Z", "ended_at": "2026-08-06T04:50:00Z",
    "effective_minutes": 10, "category": "ingestion",
    "related_ids": [TASK, RUN, "O-2026-SL-GAP-3B7A2C"],
    "artifacts_created_or_updated": ["index/runs.json", "index/artifacts.json",
        "index/task-packets.json", "index/open-problems.json", "state/activity.jsonl"],
    "summary": "Ingested KEY LEMMA run: RIGOROUS_PARTIAL_RESULT preserved; KEY LEMMA reduced to "
        "four explicit inequalities (R1/R2/L4box/L5box) with quantified margins; bases B1-B5, B7 "
        "PROVED; audit finding C1 (LOG and FP forms not logically equivalent; T4 consumes FP).",
    "evidence": ["candidate_proof.md", "audit_report.md", "artifact hashes"],
    "recorded_by": "coordinator", "notes": "estimate"}
p = os.path.join(ROOT, "state", "activity.jsonl")
with io.open(p, "a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(act, ensure_ascii=False) + "\n")

# tools: append KEY LEMMA reduction to key-lemma-decomposition.md
p = os.path.join(ROOT, "tools", "key-lemma-decomposition.md")
txt = read_utf8(p)
addition = """

## 2026-08-06 更新: KEY LEMMA 归约到四引理 (run R-20260806T011500Z-keylemma-E58FB1)
独立 run 把 KEY LEMMA 归约到四个显式局部不等式, 全部数值验证带量化余量, 但解析证明开放:
- R1: G2 >= 0 for q >= 2, c in (0,1/2); 紧点 (2,1/2), 余量 0.069181 (精确角值).
- R2: G2 >= 0 for q > 1, c in (0,0.4]; 余量 0.415004.
- L4box: H' = G2'-G1' < 0 on (1,2]x[0.4,0.5]; 余量 7.7317.
- L5box: F~'' = M~1 J1 - M~2 J2 > 0 on (1,2]x[0.4,0.5]; 余量 14.167.
基座引理已证: L1 (G1<0 全域), L2 (G2>=0 => 两形式成立), B1-B3 (q=1 族), B4
(F~'(q,1/2)=2 pi (cos x-1)^3 P(x)/sin^3 x < 0, P(x)>(pi-3x)^2), B5 (H(q,1/2)=
2 pi q(q+1)/(2q+1)^{3/2} 严格递增, min 4 pi/(3 sqrt3)), B7 (G2(c;1)>0 for c<=0.4).
关键开放核心 Q1: dG2/dq >= 0 (全域数值成立, 衰减到 0) 可把 R1/R2 归约到一维边界 B6/B7.
审计发现 C1 (重要更正): (LOG) 形式 (d/dc)log(M1/M2)<0 与 (FP) 形式 F'(c)<0 并非逻辑等价;
源报告 T4 只消费 (FP) (F 在 (0,1/2) 严格递减); 两形式须分别证明.
四引理闭合后: R1^R2^L4box^L5box^B1-B5^B7 => (LOG)^(FP) => T1-T4 关闭 O2.
"""
write_utf8(p, txt + addition)
print("tools/key-lemma-decomposition.md updated")

# tools/README.md: append log line
p = os.path.join(ROOT, "tools", "README.md")
txt = read_utf8(p)
addition = """
- 2026-08-06: key-lemma-decomposition 追加 KEY LEMMA 归约到四引理 (R1/R2/L4box/L5box),
  基座 B1-B5/B7 已证, 审计发现 C1 (LOG 与 FP 形式非等价; 见 run R-20260806T011500Z-keylemma-E58FB1).
"""
write_utf8(p, txt + addition)
print("tools/README.md updated")
print("INGESTED")