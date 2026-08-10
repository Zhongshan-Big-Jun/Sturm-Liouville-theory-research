# -*- coding: utf-8 -*-
import io, os, json, hashlib

ROOT = r"F:\LaTeX\BVE research"

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

def h6(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:6].upper()

t1_run = "R-20260806T011500Z-keylemma-E58FB1"
t2_run = "R-20260806T011500Z-o3abranch-E8E56F"
t1_task = "Q-20260806-keylemma-E58FB1"
t2_task = "Q-20260806-o3a-branch-E8E56F"

# --- 1. AGENTS.md session 19 ---
agents = read_utf8(os.path.join(ROOT, "AGENTS.md"))
session19 = """

### 2026-08-06 会话 19 (技能升级适配 + 项目校验修复 + 派发 KEY LEMMA / O3a 两个并行 run)
- 任务: 用户升级了 manage-math-research-program 与 rigorous-open-math-research 两个 skill, 按新协议
  调整研究; 继续推进 n=1 相邻间距极端值严格证明 (前序预算 consumed 4.8h / 8h).
- 完成:
  - 读取两个升级后 skill 全文与 references (delegation-and-ingestion, boundary-checklist,
    project-repository-spec, state-checkpoints-and-reports); 确认单向依赖 管理->求解,
    管理层不复制/不重写上游标准工件, 不建定理契约/义务图/路线组合/候选证明.
  - 运行 skill 自带校验脚本 validate_project.py: 初始 INVALID, 修复后 VALID (零错误零警告).
    修复项: state/current.json 补 project_id; index/open-problems.json 补 problem_id;
    state/activity.jsonl 去 BOM; index/tools.json 与 tools/*.md 补 canonical_key (3 项);
    新建 6 个必需文档: agenda/DIRECTIONS.md, agenda/PRIORITIES.md,
    literature/maps/PAPER_MAP.md, literature/maps/FRONTIER.md,
    knowledge/GLOSSARY.md, knowledge/FAILURE_PATTERNS.md.
  - 按新协议建立两个 task packet (只含上下文/文献线索, 不含定理契约):
    agenda/task-packets/Q-20260806-keylemma-E58FB1.md (KEY LEMMA 闭包, 授权任一等价形式
    (d/dc)log(M1/M2)<0 / G(alpha2)>G(alpha1) / F'(c)<0, 或连续型 (C) 无切零), 与
    agenda/task-packets/Q-20260806-o3a-branch-E8E56F.md (O3a 引理 A/B/C).
  - 并行派发两个 rigorous-open-math-research run (subagent Jason 负责 KEY LEMMA,
    Pascal 负责 O3a): runs/rigorous-open-math-research/{R-20260806T011500Z-keylemma-E58FB1,
    R-20260806T011500Z-o3abranch-E8E56F}/; 每个 run 目录仅含 run-manifest.json 与
    task-packet-link.txt (manager-owned), 上游工件由求解层写入.
  - 索引/状态更新: index/task-packets.json (2 条 READY->DISPATCHED), state/current.json,
    state/RESUME.md, state/activity.jsonl (ACT-007/008, estimate), checkpoint 派发记录.
- 状态: RIGOROUS_PARTIAL_RESULT (不变; 两个 run in progress). 开放项: KEY LEMMA, O3a 引理
  A/B/C, O1 独立审计 (O4), INF R->inf 极限证明.
- 待办: 代理返回后 ingest (保留上游状态标签 verbatim); KEY LEMMA 或 O3a 若 PROVED 则合流撰写
  docs/SL_gap_n1_proof.tex; 预算余额如实记账.
"""
write_utf8(os.path.join(ROOT, "AGENTS.md"), agents + session19)
print("AGENTS.md updated")

# --- 2. state/current.json ---
p = os.path.join(ROOT, "state", "current.json")
cur = json.loads(read_utf8(p))
cur["current_stage"] = "gap-extremals-n1-dispatch"
cur["active_run_id"] = t1_run
cur["active_run_ids"] = [t1_run, t2_run]
cur["active_task_ids"] = [t1_task, t2_task]
cur["latest_checkpoint"] = "state/checkpoints/2026-08-06T011800Z--gapn1-dispatch.md"
cur["next_actions"] = [
    "1. ingest KEY LEMMA run (Jason) 与 O3a run (Pascal); 保留上游状态 verbatim",
    "2. 若 KEY LEMMA PROVED: 合流 O1+O2+O3a+O3b 撰写 docs/SL_gap_n1_proof.tex",
    "3. O1 草稿独立 verifier 审计 (义务 O4)",
    "4. INF R->inf 极限严格证明 (D*R -> 24.943866)"
]
cur["last_updated"] = "2026-08-06T01:18:00Z"
write_utf8(p, json.dumps(cur, ensure_ascii=False, indent=2) + "\n")
print("current.json updated")

# --- 3. state/RESUME.md (rewrite) ---
resume = """# RESUME

## Current objective
Prove (n=1): over 1<=rho<=R, SUP(lambda_2-lambda_1) attained by symmetric 3-block [1,R,1] at u*(R);
INF by symmetric [R,1,R]. Run status: RIGOROUS_PARTIAL_RESULT
(O1 reduction PROVED draft; O3b(1) two-block bounds PROVED; O2 single-crossing and O3a uniqueness PARTIAL).

## Read these files first
1. `docs/SL_gap_n1_research_summary.pdf` (8 pages, zero warnings; definitive status + gaps)
2. `runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/problem_contract.md`
3. `runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/research_ledger.md`
4. `tools/key-lemma-decomposition.md` (decomposition + falsified q-monotonicity)
5. Task packets: `agenda/task-packets/Q-20260806-keylemma-E58FB1.md` and
   `agenda/task-packets/Q-20260806-o3a-branch-E8E56F.md`

## Last completed action
2026-08-06: skill-upgrade adaptation. Ran validate_project.py (INVALID -> VALID; fixed project_id,
problem_id, activity BOM, tool canonical_key, created 6 required management docs). Dispatched two
parallel rigorous-open-math-research runs: KEY LEMMA closure (Jason) and O3a Lemmas A-C (Pascal),
run roots listed below.

## Active tasks and runs
- Task: Q-20260806-keylemma-E58FB1, run R-20260806T011500Z-keylemma-E58FB1 (DISPATCHED, in progress)
- Task: Q-20260806-o3a-branch-E8E56F, run R-20260806T011500Z-o3abranch-E8E56F (DISPATCHED, in progress)
- Prior: Q-20260805-gapn1-proof-9F31D0, run R-20260805T000000Z-gapn1-a1b2c3 (INGESTED)

## Exact next action
1. Wait for both agents; ingest upstream status verbatim and index artifacts.
2. If KEY LEMMA PROVED: merge O1+O2+O3a+O3b into docs/SL_gap_n1_proof.tex.
3. O1 draft independent verifier audit (obligation O4).

## Blockers or missing inputs
- None blocking. Paywalled literature (Sun 2022 etc.) logged as unavailable.

## Budget remaining
8.0 h target, evidence-backed effective time; consumed 4.8 h before this session
(state/activity.jsonl ACT-001..006). This session records ACT-007/008 as estimates; update after
agent returns.

## Validation command
- `python scripts/gap_lib.py` sanity check
- `python C:\\Users\\HuangZY\\.codex\\skills\\manage-math-research-program\\scripts\\validate_project.py F:\\LaTeX\\BVE research`
- Recompile docs: xelatex in docs/ with -output-directory=build
"""
write_utf8(os.path.join(ROOT, "state", "RESUME.md"), resume)
print("RESUME.md updated")

# --- 4. activity.jsonl append ---
acts = [
    {"activity_id": "ACT-20260806-007",
     "started_at": "2026-08-06T01:00:00Z", "ended_at": "2026-08-06T01:10:00Z",
     "effective_minutes": 10, "category": "administration",
     "related_ids": ["MRP-20260731-BVE-SL"],
     "artifacts_created_or_updated": ["state/current.json", "index/open-problems.json",
        "index/tools.json", "state/activity.jsonl", "agenda/DIRECTIONS.md",
        "agenda/PRIORITIES.md", "literature/maps/PAPER_MAP.md", "literature/maps/FRONTIER.md",
        "knowledge/GLOSSARY.md", "knowledge/FAILURE_PATTERNS.md"],
     "summary": "Skill-upgrade adaptation: read new manage-math-research-program references, ran "
        "validate_project.py (INVALID -> VALID), fixed project_id/problem_id/activity BOM/"
        "canonical_key, created 6 required management documents.",
     "evidence": ["validate_project.py output VALID"], "recorded_by": "coordinator",
     "notes": "estimate"},
    {"activity_id": "ACT-20260806-008",
     "started_at": "2026-08-06T01:10:00Z", "ended_at": "2026-08-06T01:18:00Z",
     "effective_minutes": 8, "category": "task_packaging",
     "related_ids": ["Q-20260806-keylemma-E58FB1", "Q-20260806-o3a-branch-E8E56F",
        "R-20260806T011500Z-keylemma-E58FB1", "R-20260806T011500Z-o3abranch-E8E56F",
        "O-2026-SL-GAP-3B7A2C"],
     "artifacts_created_or_updated": ["agenda/task-packets/Q-20260806-keylemma-E58FB1.md",
        "agenda/task-packets/Q-20260806-o3a-branch-E8E56F.md",
        "runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/run-manifest.json",
        "runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/run-manifest.json",
        "index/task-packets.json", "state/current.json", "state/RESUME.md"],
     "summary": "Created two task packets (KEY LEMMA closure; O3a Lemmas A-C), registered them, "
        "created run roots with manager-owned run-manifest + task-packet-link, dispatched two "
        "rigorous-open-math-research agents (Jason, Pascal) in parallel.",
     "evidence": ["task packets", "run manifests", "spawn_agent results"],
     "recorded_by": "coordinator", "notes": "estimate"},
]
p = os.path.join(ROOT, "state", "activity.jsonl")
with io.open(p, "a", encoding="utf-8", newline="\n") as f:
    for a in acts:
        f.write(json.dumps(a, ensure_ascii=False) + "\n")
print("activity.jsonl appended")

# --- 5. checkpoint ---
cp = """# Checkpoint: gap-n1 dispatch (2026-08-06T01:18Z)

## Run status (verbatim)
RIGOROUS_PARTIAL_RESULT (unchanged; two new runs in progress)

## Completed this stage
- Skill-upgrade adaptation completed; validate_project.py status: VALID (no errors or warnings).
- Fixed: project_id in state/current.json; problem_id in index/open-problems.json;
  activity.jsonl BOM; canonical_key in index/tools.json and tools/*.md;
  created agenda/DIRECTIONS.md, agenda/PRIORITIES.md, literature/maps/PAPER_MAP.md,
  literature/maps/FRONTIER.md, knowledge/GLOSSARY.md, knowledge/FAILURE_PATTERNS.md.
- Dispatched two parallel rigorous-open-math-research runs:
  * KEY LEMMA closure (task Q-20260806-keylemma-E58FB1, agent Jason,
    run R-20260806T011500Z-keylemma-E58FB1)
  * O3a Lemmas A-C (task Q-20260806-o3a-branch-E8E56F, agent Pascal,
    run R-20260806T011500Z-o3abranch-E8E56F)
- Task packets contain project context only (no theorem contract, no route prescription).

## Active items
- KEY LEMMA open (delegated); O3a Lemmas A-C open (delegated).
- O1 draft: independent verifier audit scheduled (obligation O4).
- INF R->inf limit proof open (D*R -> 24.943866).

## Blockers
- None.

## Next commands / files
- Wait for agents; then ingest (preserve upstream status verbatim; index artifacts).
- Revalidate: python C:\\Users\\HuangZY\\.codex\\skills\\manage-math-research-program\\scripts\\validate_project.py F:\\LaTeX\\BVE research
- Resume: read state/RESUME.md
"""
write_utf8(os.path.join(ROOT, "state", "checkpoints", "2026-08-06T011800Z--gapn1-dispatch.md"), cp)
print("checkpoint written")