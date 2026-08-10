# -*- coding: utf-8 -*-
import io, os

ROOT = r"F:\LaTeX\BVE research"

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

# AGENTS.md: renumber the agent-appended duplicate "会话 15 (O1 独立审计)" to 会话 20
p = os.path.join(ROOT, "AGENTS.md")
txt = read_utf8(p)
old = "### 2026-08-06 会话 15 (O1 独立审计, Q-20260806-o1-audit-422A69)"
new = "### 2026-08-06 会话 20 (O1 独立审计 run, 由 subagent Copernicus 撰写; 会话编号由 coordinator 修正避免与 2026-08-05 会话 15 重复)"
assert old in txt
txt = txt.replace(old, new)
# append ingestion note
note = """
### 2026-08-06 会话 21 (O1 审计 run 摄取, coordinator)
- run R-20260806T011500Z-o1audit-422A69 已摄取; 上游状态 verbatim:
  RIGOROUS_PARTIAL_RESULT (O1 audit: statement TRUE, draft REPAIRABLE_GAP).
- 逐条裁决: O1a PARTIAL (T_rho 非自伴, 修复用 S_rho=rho^(1/2) T_rho rho^(1/2),
  ||S_rho-S_sigma||_HS -> 0); O1b FAILED 如陈述 (正确: dD/deps = -(c_+-c_-)f(x_j),
  草稿符号相反; 下游零条件 f(x_j)=0 不受影响); O1c/O1d/O1e/O1f PROVED.
- 修复清单 R1-R4 见 run root candidate_proof.md; 草稿未修改 (只读审计).
- 索引: index/runs.json + artifacts.json + task-packets.json (INGESTED) +
  open-problems.json 已更新; activity.jsonl 记 ACT-009; 审计前四份输入哈希复核未变.
- 待办: O1 修订 (revising 角色) 与复审 (O4); 同时等 KEY LEMMA (Jason) 与 O3a (Pascal).
"""
write_utf8(p, txt + note)
print("AGENTS.md updated")

# RESUME.md refresh
resume = """# RESUME

## Current objective
Prove (n=1): over 1<=rho<=R, SUP(lambda_2-lambda_1) attained by symmetric 3-block [1,R,1] at u*(R);
INF by symmetric [R,1,R]. Run status: RIGOROUS_PARTIAL_RESULT
(O1 reduction audited: statement TRUE, draft REPAIRABLE_GAP; O3b(1) two-block bounds PROVED;
O2 single-crossing and O3a uniqueness PARTIAL).

## Read these files first
1. `docs/SL_gap_n1_research_summary.pdf` (8 pages, zero warnings; status + gaps)
2. `runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/problem_contract.md`
3. `runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/audit_report.md` (O1 audit)
4. `tools/key-lemma-decomposition.md` (decomposition + falsified q-monotonicity)
5. Task packets: `agenda/task-packets/Q-20260806-keylemma-E58FB1.md`,
   `agenda/task-packets/Q-20260806-o3a-branch-E8E56F.md`

## Last completed action
2026-08-06: skill-upgrade adaptation + integrity fixes (validate_project.py VALID);
dispatched three runs (KEY LEMMA, O3a, O1 audit); O1 audit ingested
(RIGOROUS_PARTIAL_RESULT; O1a operator repair, O1b FH sign, O1c-f PROVED).

## Active tasks and runs
- Task: Q-20260806-keylemma-E58FB1, run R-20260806T011500Z-keylemma-E58FB1 (DISPATCHED, in progress)
- Task: Q-20260806-o3a-branch-E8E56F, run R-20260806T011500Z-o3abranch-E8E56F (DISPATCHED, in progress)
- Task: Q-20260806-o1-audit-422A69, run R-20260806T011500Z-o1audit-422A69 (INGESTED)
- Prior: Q-20260805-gapn1-proof-9F31D0, run R-20260805T000000Z-gapn1-a1b2c3 (INGESTED)

## Exact next action
1. Ingest KEY LEMMA (Jason) and O3a (Pascal) when they return.
2. O1 revision (R1-R4) then re-audit (O4).
3. If KEY LEMMA PROVED: merge O1+O2+O3a+O3b into docs/SL_gap_n1_proof.tex.

## Blockers or missing inputs
- None blocking. Paywalled literature (Sun 2022 etc.) logged as unavailable.

## Budget remaining
8.0 h target, evidence-backed effective time; consumed 4.8 h (ACT-001..006) plus ACT-007/008/009
(estimates) this session; subagent effective time to be recorded on ingestion.

## Validation command
- `python C:\\Users\\HuangZY\\.codex\\skills\\manage-math-research-program\\scripts\\validate_project.py F:\\LaTeX\\BVE research`
- Recompile docs: xelatex in docs/ with -output-directory=build
"""
write_utf8(os.path.join(ROOT, "state", "RESUME.md"), resume)
print("RESUME.md updated")

# checkpoint
cp = """# Checkpoint: gap-n1 O1 audit ingested (2026-08-06T03:20Z)

## Run status (verbatim)
- O1 audit (R-20260806T011500Z-o1audit-422A69): RIGOROUS_PARTIAL_RESULT
- Overall program: RIGOROUS_PARTIAL_RESULT (KEY LEMMA and O3a runs in progress)

## Completed this stage
- O1 reduction theorem audited line by line: statement TRUE; draft REPAIRABLE_GAP.
  O1a PARTIAL (repair: S_rho = rho^(1/2) T_rho rho^(1/2), HS-norm continuity);
  O1b FAILED-as-stated (correct sign dD/deps = -(c_+-c_-)f(x_j); consequence valid);
  O1c/O1d/O1e/O1f PROVED (O1c matches AEH Lemma 2.2 (1),(4),(5)).
- Artifacts indexed with sha256 (audit_report.md, candidate_proof.md R1-R4, repro scripts).
- tools/gap-n1-reduction.md synced by auditor (status REPAIRABLE_GAP, FH sign corrected).

## Active items
- KEY LEMMA open (delegated, Jason); O3a Lemmas A-C open (delegated, Pascal).
- O1 revision (R1-R4) then re-audit.
- INF R->inf limit proof open (D*R -> 24.943866).

## Blockers
- None.

## Next commands / files
- Wait for Jason/Pascal; ingest with status verbatim.
- Resume: read state/RESUME.md
"""
write_utf8(os.path.join(ROOT, "state", "checkpoints", "2026-08-06T032000Z--o1-audit-ingest.md"), cp)
print("checkpoint written")