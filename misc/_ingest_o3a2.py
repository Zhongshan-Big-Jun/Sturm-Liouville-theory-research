# -*- coding: utf-8 -*-
import io, os

ROOT = r"F:\LaTeX\BVE research"

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

p = os.path.join(ROOT, "AGENTS.md")
txt = read_utf8(p)
s24 = """
### 2026-08-06 会话 24 (O3a run 摄取, coordinator)
- run R-20260806T011500Z-o3abranch-E8E56F (subagent Pascal) 已摄取; 上游状态 verbatim:
  RIGOROUS_PARTIAL_RESULT.
- 定理级结果:
  - P1-P4 已证: P1 FH 带特征值因子 (d lambda_k/d eps = -lambda_k int rho_eps u_k^2;
    无因子版本为错误); P2 残差恒等式 dR1/db = -dR2/da (P1 下成立); P3 对称不动点处
    分支斜率恒等式 g1'*g2' = 1 与 Hessian 归约; P4 R=1 基态 (v=cos(pi x), q=1/4,
    端点 a0=arccos(1/4)/pi, b0=arccos(-1/4)/pi).
  - 负结果 (严格证伪): Lemma A 为假. 区间算术证书 (mpmath.iv 外舍入, prec=220) 在
    (R,a*)=(1500,0.57364) 与 (1e4,0.57364) 处 h'(a*) 包络 [-3.4298e-4,-3.4298e-4] 与
    [-3.2030e-3,-3.2030e-3] 严格 < 0; 阈值 R* ~ 1350. T4 路线对 R >= ~1400 失效.
  - O3a 本身未被证伪: h = g1-g2 在公共区间对所有测试 R in {1.02..1e6} 恰有一个零点
    (对称不动点); 数值支持, 未证明. 修正猜想 C1: h 单零点.
  - 新结构: R=1500, a=0.57364 处 R2(a,b)=0 且 v(b)<0 有三解, 仅第三个为主片; 其余片
    v(a)<0 非符号一致不动点; Lemma C 的 "only branch components" 须按主片理解.
- 剩余缺口: G2 (证 C1 = O3a), G3 (Lemma B/C 修正陈述), G4 (大 R 时 h(b0) 与负 h' 凹陷
  间距恒正).
- 工具库: 新增 tools/fh-hessian-branch-reduction.md 与 tools/interval-ad-certificate.md;
  residual-exactness.md 增加 Lemma A 证伪注记 (由 run 内更新).
- 待办: 下一轮 O3a 目标改为 C1 (h 单零点); 等 KEY LEMMA2 run (Carson).
"""
write_utf8(p, txt + s24)
print("AGENTS.md updated")

resume = """# RESUME

## Current objective
Prove (n=1): over 1<=rho<=R, SUP(lambda_2-lambda_1) attained by symmetric 3-block [1,R,1] at u*(R);
INF by symmetric [R,1,R]. Run status: RIGOROUS_PARTIAL_RESULT
(O1 audited REPAIRABLE_GAP; O3b(1) PROVED; KEY LEMMA reduced to R1/R2/L4box/L5box;
O3a Lemma A FALSIFIED, corrected conjecture C1 open).

## Read these files first
1. `docs/SL_gap_n1_research_summary.pdf` (8 pages; status + gaps)
2. `runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/candidate_proof.md`
   (KEY LEMMA reduction + bases)
3. `runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/candidate_proof.md`
   (P1-P4 + C1 conjecture; Lemma A falsified)
4. `runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/audit_report.md`
5. `tools/key-lemma-decomposition.md`

## Last completed action
2026-08-06: O1 audit ingested; KEY LEMMA run ingested (four inequalities R1/R2/L4box/L5box);
O3a run ingested (Lemma A FALSIFIED by interval certificate; O3a NOT refuted; P1-P4 PROVED;
new target C1: h single zero). KEY LEMMA2 run (Carson) in progress.

## Active tasks and runs
- Task: Q-20260806-keylemma2-5A35E5, run R-20260806T050000Z-keylemma2-5A35E5 (DISPATCHED, in progress)
- Task: Q-20260806-keylemma-E58FB1, run R-20260806T011500Z-keylemma-E58FB1 (INGESTED)
- Task: Q-20260806-o3a-branch-E8E56F, run R-20260806T011500Z-o3abranch-E8E56F (INGESTED)
- Task: Q-20260806-o1-audit-422A69, run R-20260806T011500Z-o1audit-422A69 (INGESTED)
- Prior: Q-20260805-gapn1-proof-9F31D0, run R-20260805T000000Z-gapn1-a1b2c3 (INGESTED)

## Exact next action
1. Ingest KEY LEMMA2 (Carson) when it returns.
2. Next delegations: (a) KEY LEMMA residuals R1/Q1/R2/L4box/L5box; (b) O3a corrected
   conjecture C1 (h single zero); (c) O1 revision (R1-R4) + re-audit.
3. If KEY LEMMA closes: merge O1+O2+O3a+O3b into docs/SL_gap_n1_proof.tex.

## Blockers or missing inputs
- None blocking. Note: O3a T4 route is void for R >= ~1400 (Lemma A false); new route needed.

## Budget remaining
8.0 h target, evidence-backed; consumed 4.8 h (ACT-001..006) + ACT-007..011 (estimates);
combined subagent effort this session exceeds 8 h effective; final accounting on stage close.

## Validation command
- `python C:\\Users\\HuangZY\\.codex\\skills\\manage-math-research-program\\scripts\\validate_project.py F:\\LaTeX\\BVE research`
"""
write_utf8(os.path.join(ROOT, "state", "RESUME.md"), resume)
print("RESUME.md updated")

cp = """# Checkpoint: gap-n1 O3a ingested, KEY LEMMA2 in progress (2026-08-06T06:20Z)

## Run status (verbatim)
- O3a (R-20260806T011500Z-o3abranch-E8E56F): RIGOROUS_PARTIAL_RESULT
  (Lemma A FALSIFIED; P1-P4 PROVED; O3a not refuted; C1 open)
- KEY LEMMA (R-20260806T011500Z-keylemma-E58FB1): RIGOROUS_PARTIAL_RESULT (four inequalities open)
- O1 audit (R-20260806T011500Z-o1audit-422A69): RIGOROUS_PARTIAL_RESULT
- KEY LEMMA2 (R-20260806T050000Z-keylemma2-5A35E5): in progress

## Completed this stage
- O3a ingested: Lemma A strictly falsified (interval certificate, R=1500/1e4, h'(a*)<0;
  threshold R* ~1350). P1-P4 proved. Multi-sheet Gamma_2 structure mapped.
- Tools added by run: fh-hessian-branch-reduction.md, interval-ad-certificate.md.

## Active items
- KEY LEMMA residuals R1/R2/L4box/L5box (Carson in progress).
- O3a corrected conjecture C1 (h single zero) - next delegation.
- O1 revision (R1-R4) then re-audit.
- INF R->inf limit proof open.

## Blockers
- None. O3a T4 route void for R >= ~1400 (Lemma A false); replacement route = C1.

## Next commands / files
- Wait for Carson; ingest.
- Resume: read state/RESUME.md
"""
write_utf8(os.path.join(ROOT, "state", "checkpoints", "2026-08-06T062000Z--o3a-ingest.md"), cp)
print("checkpoint written")