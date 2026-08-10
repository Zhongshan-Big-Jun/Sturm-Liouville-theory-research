# -*- coding: utf-8 -*-
import json, hashlib, os

root = r"F:\LaTeX\BVE research"
def sha16(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

run_root = os.path.join(root, r"runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3")
now = "2026-08-06T00:30:00Z"

# ---------- index/tools.json ----------
tools = {
    "schema_version": 1,
    "updated_at": now,
    "note": "全量工具库位于 tools/ (README 索引, 29 项); 本索引登记新技能结构要求的登记项 (增量).",
    "items": [
        {
            "tool_id": "gap-n1-reduction",
            "title": "两块族归约定理 (gap-n1 reduction)",
            "kind": "reduction_pattern",
            "location": "tools/gap-n1-reduction.md",
            "provenance_maturity": "UPSTREAM_AUDITED",
            "source_run": "R-20260805T000000Z-gapn1-a1b2c3",
            "artifact": "O1_reduction_draft.md (sha256:16=c647297430348618)",
            "upstream_status_verbatim": "PROVED (draft; 独立审计待补)",
            "last_reviewed": "2026-08-06"
        },
        {
            "tool_id": "two-block-gap-bounds",
            "title": "两块相位间距界 3pi^2/R < D < 3pi^2",
            "kind": "estimate",
            "location": "tools/two-block-gap-bounds.md",
            "provenance_maturity": "UPSTREAM_AUDITED",
            "source_run": "R-20260805T000000Z-gapn1-a1b2c3",
            "artifact": "agentC_O3b_boundary.md (sha256:16=1ba8b1c4863950aa)",
            "upstream_status_verbatim": "PROVED (4000 点零违例; 相位恒等式 1e-13)",
            "last_reviewed": "2026-08-06"
        },
        {
            "tool_id": "key-lemma-decomposition",
            "title": "KEY LEMMA 分解与逐项 q-单调性否证",
            "kind": "obstruction",
            "location": "tools/key-lemma-decomposition.md",
            "provenance_maturity": "UPSTREAM_AUDITED",
            "source_run": "R-20260805T000000Z-gapn1-a1b2c3",
            "artifact": "agentA_O2_single_crossing.md (sha256:16=dc88d7a750a3acef) + research_ledger R-006",
            "upstream_status_verbatim": "分解+角点极限 PROVED; B-D q-单调性 REFUTED (反例已复现)",
            "last_reviewed": "2026-08-06"
        }
    ]
}
with open(os.path.join(root, "index", "tools.json"), "w", encoding="utf-8") as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)

# ---------- index/runs.json ----------
runs = {
    "schema_version": 1,
    "updated_at": now,
    "items": [
        {
            "run_id": "R-20260805T000000Z-gapn1-a1b2c3",
            "task_id": "Q-20260805-gapn1-proof-9F31D0",
            "problem_id": "O-2026-SL-GAP-3B7A2C",
            "run_root": "runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3",
            "started_at": "2026-08-05T00:00:00Z",
            "manager_ingestion_state": "ingested",
            "upstream_status_verbatim": "RIGOROUS_PARTIAL_RESULT (O1 PROVED draft, O3b(1) PROVED, O2/O3a PARTIAL)",
            "artifacts": {
                "problem_contract.md": "sha256:16=0fcd9f94293c7847",
                "O1_reduction_draft.md": "sha256:16=c647297430348618",
                "agentA_O2_single_crossing.md": "sha256:16=dc88d7a750a3acef",
                "agentB_O3a_fixed_point.md": "sha256:16=01fbf95dd6b7afd5",
                "agentC_O3b_boundary.md": "sha256:16=1ba8b1c4863950aa",
                "research_ledger.md": "sha256:16=23a2d882e93a4b23"
            },
            "deliverables": [
                "docs/SL_gap_n1_research_summary.pdf (8 页, 零警告)",
                "tools/gap-n1-reduction.md, tools/two-block-gap-bounds.md, tools/key-lemma-decomposition.md"
            ],
            "exact_remaining_gaps": [
                "KEY LEMMA: (d/dc) log(M1/M2) < 0 on (0,1/2); 分解+角点极限已证, 逐项 q-单调闭环已否证 (B-D 非单调)",
                "O3a 引理 A/B/C: g1'-g2' 的 R 一致正下界, h 端点符号, 好分支覆盖"
            ]
        }
    ]
}
with open(os.path.join(root, "index", "runs.json"), "w", encoding="utf-8") as f:
    json.dump(runs, f, ensure_ascii=False, indent=2)

# ---------- index/artifacts.json ----------
artifacts = {
    "schema_version": 1,
    "updated_at": now,
    "items": [
        {"artifact_id": "ART-GAPN1-SUMMARY-20260805", "kind": "research_summary_doc", "path": "docs/SL_gap_n1_research_summary.pdf", "hash16": "3e303203e83bcb70", "produced_by_run": "R-20260805T000000Z-gapn1-a1b2c3"},
        {"artifact_id": "ART-GAPN1-SUMMARY-TEX", "kind": "research_summary_tex", "path": "docs/SL_gap_n1_research_summary.tex", "hash16": "3703fa5040626599", "produced_by_run": "R-20260805T000000Z-gapn1-a1b2c3"},
        {"artifact_id": "ART-TOOL-GAPN1-REDUCTION", "kind": "tool_entry", "path": "tools/gap-n1-reduction.md", "hash16": "2f92c467098c3d7d", "produced_by_run": "R-20260805T000000Z-gapn1-a1b2c3"},
        {"artifact_id": "ART-TOOL-TWOBLOCK-BOUNDS", "kind": "tool_entry", "path": "tools/two-block-gap-bounds.md", "hash16": "777be5b6cca7e058", "produced_by_run": "R-20260805T000000Z-gapn1-a1b2c3"},
        {"artifact_id": "ART-TOOL-KEYLEMMA-DECOMP", "kind": "tool_entry", "path": "tools/key-lemma-decomposition.md", "hash16": "80f0601d418341f8", "produced_by_run": "R-20260805T000000Z-gapn1-a1b2c3"}
    ]
}
with open(os.path.join(root, "index", "artifacts.json"), "w", encoding="utf-8") as f:
    json.dump(artifacts, f, ensure_ascii=False, indent=2)

# ---------- index/task-packets.json ----------
pk = {
    "schema_version": 1,
    "updated_at": now,
    "items": [
        {
            "task_id": "Q-20260805-gapn1-proof-9F31D0",
            "path": "agenda/task-packets/Q-20260805-gapn1-proof-9F31D0.md",
            "problem_id": "O-2026-SL-GAP-3B7A2C",
            "state": "INGESTED",
            "run_id": "R-20260805T000000Z-gapn1-a1b2c3",
            "dispatched_at": "2026-08-05T00:00:00Z"
        }
    ]
}
with open(os.path.join(root, "index", "task-packets.json"), "w", encoding="utf-8") as f:
    json.dump(pk, f, ensure_ascii=False, indent=2)

# ---------- state/current.json ----------
cur = {
    "schema_version": 1,
    "project_lifecycle_state": "ACTIVE",
    "current_stage": "gap-extremals-n1-ingest",
    "objective": "Prove SUP/INF of lambda_2-lambda_1 over 1<=rho<=R box class attained by symmetric 3-block [1,R,1] / [R,1,R]",
    "active_direction": "SL-gap-extremals",
    "active_problem_id": "O-2026-SL-GAP-3B7A2C",
    "active_task_id": "Q-20260805-gapn1-proof-9F31D0",
    "active_run_id": "R-20260805T000000Z-gapn1-a1b2c3",
    "latest_checkpoint": "state/checkpoints/2026-08-06T0030Z--gapn1-ingest.md",
    "run_status_verbatim": "RIGOROUS_PARTIAL_RESULT",
    "next_actions": [
        "1. KEY LEMMA: 证明 A-C 的 q-单调性 (数值全通过) 并找到 B-D 递减区的互补下界, 或对和 G2-G1 建立解析下界",
        "2. O3a 引理 A: g1'-g2' 的 R 一致正下界 (数值 42.78 (R=1.05) 到 0.287 (R=100))",
        "3. O1 草稿安排独立 verifier 审计 (义务 O4)",
        "4. INF 极限: 严格证明 R->inf 时 D*R -> 24.943866",
        "5. 合流后撰写 SL_gap_n1_proof.tex"
    ],
    "blockers": [],
    "budget": {
        "mode": "effective_time",
        "target_hours": 8.0,
        "consumed_hours": 4.8,
        "note": "如实记账; 证据见 state/activity.jsonl ACT-001..006; 缺口未闭合, 预算结余用于后续会话"
    },
    "last_literature_cutoff": "2026-08-05",
    "last_updated": now
}
with open(os.path.join(root, "state", "current.json"), "w", encoding="utf-8") as f:
    json.dump(cur, f, ensure_ascii=False, indent=2)

# ---------- state/RESUME.md ----------
resume = """# RESUME

## Current objective
Prove (n=1): over 1<=rho<=R, SUP(lambda_2-lambda_1) attained by symmetric 3-block [1,R,1] at u*(R); INF by symmetric [R,1,R].
Run status: RIGOROUS_PARTIAL_RESULT (O1 reduction PROVED draft; O3b(1) two-block bounds PROVED; O2 single-crossing and O3a uniqueness PARTIAL).

## Read these files first
1. `docs/SL_gap_n1_research_summary.pdf` (8 pages, zero warnings; definitive status + gaps)
2. `runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/problem_contract.md`
3. `runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/research_ledger.md` (R-001..R-006)
4. `docs/SL_gap_extremals.tex` (numerics; tab:rscan SUP u-column already fixed)
5. `tools/key-lemma-decomposition.md` (decomposition + falsified q-monotonicity)

## Last completed action
2026-08-05/06: rebuilt the corrupted summary tex in full Chinese (8 pages, zero warnings); independent re-verification
confirmed R=4 SUP/INF D* to 3.9e-11 and two-block bounds (phase solver, 0 violations); KEY LEMMA decomposition with
exact corner limit 4pi/(3 sqrt3); FALSIFIED the handoff claim d/dq(B-D) >= 0 (counterexample c=0.01, q 5000->20000,
B-D 199.79->193.99); tools gap-n1-reduction / two-block-gap-bounds / key-lemma-decomposition added; indexes/state updated.

## Active tasks and runs
- Task: Q-20260805-gapn1-proof-9F31D0 (task state: INGESTED)
- Run: R-20260805T000000Z-gapn1-a1b2c3 (status: RIGOROUS_PARTIAL_RESULT)

## Exact next action
1. KEY LEMMA: prove A-C q-monotonicity (numerics all pass) and find a complementary lower bound for B-D on its
   decreasing region (c <= 0.1), or a direct analytic lower bound for the sum G2-G1 (min 2.4184 at the corner).
2. O3a Lemma A: R-uniform positive lower bound for g1'-g2'.
3. Independent verifier audit of O1 draft (obligation O4).

## Blockers or missing inputs
- None blocking. Full texts of Sun 2022 (JMAA 126513) unavailable (literature audit done; no published result for box class).

## Budget remaining
8.0 h target, evidence-backed effective time; consumed 4.8 h (state/activity.jsonl ACT-001..006; estimates labeled).

## Validation command
- `python scripts/gap_lib.py` sanity check (lams_fast)
- Recompile docs: xelatex in docs/ with -output-directory=build (SL_gap_n1_research_summary.tex -> 8 pages, zero warnings)
"""
with open(os.path.join(root, "state", "RESUME.md"), "w", encoding="utf-8") as f:
    f.write(resume)

print("state/index files written")