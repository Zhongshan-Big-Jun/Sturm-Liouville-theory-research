# -*- coding: utf-8 -*-
import io, os

ROOT = r"F:\LaTeX\BVE research"

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

# AGENTS.md session 25
p = os.path.join(ROOT, "AGENTS.md")
txt = read_utf8(p)
s25 = """
### 2026-08-06 会话 25 (KEYLEMMA2 中断审计 + KEYLEMMA2b 续作派发, coordinator)
- 背景: KEYLEMMA2 run (R-20260806T050000Z-keylemma2-5A35E5, subagent Carson) 在最后组装阶段
  被中断 (代理对象丢失); 管理层审计其 run 目录, 判定无最终判定, 但保留大量可用进展.
- 中断 run 已产出 (未独立验证):
  - (q,u) 参数化: u = q tan(pi-alpha2), G2 >= 0 等价于 IN(q,u) >= 0, Sign(IN)=Sign(G2).
  - M2 路线: dIN/du < 0 on D = {(q,u): q>1, 0<u<sqrt(2q+1)}; M2(1,u)=pi*(4u(pi-atan u)-5-9u^2)
    精确, h(u) 凹且 h(u*) <= -1.35 < 0 (解析); dM2/dq < 0 对 q>=20 由初等界 B(q) 成立.
  - 归约改进: R1 <= M2 ^ CORNER; R2 <= M2 ^ C4; M1 不再需要.
  - CORNER: G2(1/2;q)>=0 (q>=2) 等价于 pi > arccos(2/3)+sqrt(5), 初等证书进行中.
  - C4: c=0.4 曲线上 K(v) 递增, min K=2.615 > 0 at v=2pi/7.
  - 四个区间证书已计算: dM2dq (84 盒, 最坏上界 -0.1902), L4box (128 盒, -4.6569),
    L5box (128 盒, +6.2429), C4 (200 盒, +2.4218).
- 已做: 更新 index (中断 run 标记 interrupted_no_verdict, 任务 CANCELLED); 派发续作
  KEYLEMMA2b (Q-20260806-keylemma2b-0A6D8F, run R-20260806T070000Z-keylemma2b-0A6D8F,
  subagent Plato) - 任务: 独立运行 verify_certificates.py 验证四个证书, 完成
  M2/CORNER/C4/L4box/L5box 解析证明, 组装 candidate_proof.md 与 audit_report.md.
- 状态: RIGOROUS_PARTIAL_RESULT; KEY LEMMA 残余缺口接近闭合但证书未验证, 不得升级.
- 待办: 等 Plato 返回后摄取; 若 (LOG)^(FP) 闭合则合流写 SL_gap_n1_proof.tex.
"""
write_utf8(p, txt + s25)
print("AGENTS.md updated")

resume = """# RESUME

## Current objective
Prove (n=1): over 1<=rho<=R, SUP(lambda_2-lambda_1) attained by symmetric 3-block [1,R,1] at u*(R);
INF by symmetric [R,1,R]. Run status: RIGOROUS_PARTIAL_RESULT
(O1 audited REPAIRABLE_GAP; O3b(1) PROVED; KEY LEMMA reduced to four inequalities, residual
near-closed with four unverified interval certificates; O3a Lemma A FALSIFIED, C1 open).

## Read these files first
1. `docs/SL_gap_n1_research_summary.pdf` (8 pages; status + gaps)
2. `runs/rigorous-open-math-research/R-20260806T050000Z-keylemma2-5A35E5/research_ledger.md`
   (KEY LEMMA residual: (q,u) reformulation, M2 route, CORNER, C4; TO DO list)
3. `runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/candidate_proof.md`
4. `runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/candidate_proof.md`
   (P1-P4 + C1 conjecture; Lemma A falsified)
5. `runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/audit_report.md`
6. `tools/key-lemma-decomposition.md`

## Last completed action
2026-08-06: O1 audit + KEY LEMMA + O3a runs ingested. KEYLEMMA2 run interrupted
(certificates computed but unverified). KEYLEMMA2b resume run dispatched (Plato).

## Active tasks and runs
- Task: Q-20260806-keylemma2b-0A6D8F, run R-20260806T070000Z-keylemma2b-0A6D8F (DISPATCHED, in progress)
- Task: Q-20260806-keylemma2-5A35E5, run R-20260806T050000Z-keylemma2-5A35E5 (CANCELLED/interrupted)
- Task: Q-20260806-keylemma-E58FB1, run R-20260806T011500Z-keylemma-E58FB1 (INGESTED)
- Task: Q-20260806-o3a-branch-E8E56F, run R-20260806T011500Z-o3abranch-E8E56F (INGESTED)
- Task: Q-20260806-o1-audit-422A69, run R-20260806T011500Z-o1audit-422A69 (INGESTED)

## Exact next action
1. Ingest KEYLEMMA2b (Plato) when it returns; verify certificates + analytic proofs status.
2. If KEY LEMMA (LOG)^(FP) closes: merge O1(revised)+O2+O3a+O3b into docs/SL_gap_n1_proof.tex.
3. O3a corrected conjecture C1 (h single zero) - next delegation.
4. O1 revision (R1-R4) then re-audit.
5. INF R->inf limit proof (D*R -> 24.943866).

## Blockers or missing inputs
- None blocking. Note: O3a T4 route void for R >= ~1400 (Lemma A false); replacement = C1.

## Budget remaining
8.0 h target, evidence-backed; consumed 4.8 h (ACT-001..006) + ACT-007..012 (estimates);
combined subagent effort this session far exceeds 8 h effective; final accounting on stage close.

## Validation command
- `python C:\\Users\\HuangZY\\.codex\\skills\\manage-math-research-program\\scripts\\validate_project.py F:\\LaTeX\\BVE research`
"""
write_utf8(os.path.join(ROOT, "state", "RESUME.md"), resume)
print("RESUME.md updated")