# Round10 local Lean author handoff

作者侧局部形式化完成. 指定最终源码与合取根已由实际 Lean 编译, 原版 lean-verify 2.0.1 返回 machine_verification_passed=true 和 exact_root_passed=true. 这不是独立语义验收, 也不是完整 Lean 工程通过.

## Mathematical content

`project/AuditRound10.lean` 从 `Fin (2*n)` 上真实 `Fin.rev` 定义实线性 J, 坐标定理明确其值为 `2*n-1-i`. 两个线性投影严格定义为 `(I-J)/2` 与 `(I+J)/2`. 证明包括线性性, 对合, 两种特征关系, 分解, 幂等, 双向消去, 固定点/特征空间等价, 反转保持 Euclidean 点积及两个投影范围正交. 还证明 `R(x)=1-Jx` 的对合与精确扰动公式, 并识别对称基点处的保持/破缺方向.

相位部分使用实函数在 `[0,∞)` 上的连续性和严格递增性. `phase_root Phi k x` 精确定义为 `0≤x ∧ Phi x=kπ`. IVT 给出有效闭括区中的唯一解; 已知相位根满足 `x<y ↔ j<k`; 严格递增的指标及逐指标有效括区给出位于括区内的严格递增根序列. 存在性使用 classical choice, 不是数值算法.

`AuditRound10.root` 是全部 21 项局部接口的显式合取. 投影定理从实际定义推出, 未将投影性质当作假设; 相位连续性, 严格单调性和有效括区则按任务要求保留为显式前提. `root-contract.json` 与 `root-exact-type.lean.txt` 保存完整预期 Lean 类型; `root-clauses.json` 逐项列出组成声明. 机械匹配也检查 binder kinds 和 universe parameters; informal 合同性仍须后续独立检验.

## Execution and identity

- Lean: Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release).
- Final source SHA-256: `821e19a77ed105f1642cd7dcc660a9992fa05fe0fa40e1021eaca24a178e8bc7`.
- Root contract SHA-256: `8d24a64383e51b5fd859c09c3a77febd4218092de5bd7daebdeee01ed0325d40`.
- Exact-root durable job: `exact-root-02-durable`, actual terminal state `SUCCEEDED`.
- Root dependency axioms: `propext, Classical.choice, Quot.sound`. No sorryAx or additional axioms were found in the actual selected root closure.
- Full imported-module inventory, dependency closure, expected-type comparison, source/tool/runtime/environment hashes and Lean job logs: `evidence/exact-root-02/run-manifest.json` and its immutable per-run directory. The verifier checks the minimal frozen `root-project/`, whose core source is byte-identical to `project/AuditRound10.lean`. Loaded environment inventory contains 4162 modules; this is an evidence inventory count, not a count of new mathematical results.
- `commands/*/command.json` saves actual argv, cwd, relevant environment, process ID, start/end, exit code, input hashes and log hashes. Each command directory contains full stdout/stderr and input snapshots. `REPLAY.md` gives non-overwriting replay commands.

| Command label | Actual exit | Seconds |
| --- | --- | --- |
| runtime-version | 0 | 1.460 |
| development-01 | 1 | 148.962 |
| development-02 | 0 | 9.863 |
| development-03 | 1 | 10.125 |
| final-source-01 | 0 | 9.591 |
| positive-refutations-01 | 1 | 11.558 |
| positive-refutations-02 | 0 | 9.123 |
| negative-flip-01 | 1 | 9.352 |
| negative-reflection-01 | 1 | 9.154 |
| negative-index-01 | 1 | 9.828 |
| print-main-01 | 0 | 18.476 |
| print-controls-01 | 0 | 12.409 |
| explicit-export-01 | 0 | 16.385 |
| explicit-export-full-01 | 0 | 14.886 |
| blind-source-01 | 0 | 10.415 |
| exact-root-01 | 1 | 584.210 |
| exact-root-02 | 0 | 819.057 |

## Preserved failures and negative controls

- development-01: true exit 1. Fin.rev subtraction was propositionally but not definitionally equal; a distributive coordinate identity needed ring; an ordered-multiplication lemma requested an unsuitable generic instance. Corrected with Fin.ext/omega, ring, and real arithmetic.
- development-03: true exit 1. A style cleanup ran ring after simp had already closed one constructor branch. Split branches explicitly.
- positive-refutations-01: true exit 1. norm_num had already closed the off-by-one contradiction before later tactics. Removed only those unreachable tactics; positive-refutations-02 returned 0.
- exact-root-01: true exit 1, evidence status stale. All Lean jobs returned 0 and the exact type matched, but the verifier's project-wide source snapshot detected the repaired Counterexamples.lean and newly added ReadbackExportFull.lean. This first root run is not a pass. The successful successor checks a separate minimal frozen root-project and leaves the first result intact.
- NegativeFlip: F=-J on v=(1,1) was falsely asserted idempotent. Lean rejected the false equality with an unresolved False goal.
- NegativeReflection: a plus sign was falsely used in the reflection perturbation, for x=0,v=(1,1). Lean rejected it with an unresolved False goal.
- NegativeIndex: Phi(x)=x at x=2π was falsely assigned level 1π. Lean rejected it, with False remaining under the true premise 0<π.
- `Counterexamples.lean` proves all three exact negations. `PrintCounterexamples.lean` and corresponding logs export their statements/proofs and axioms. Negative compiler failures therefore have mathematical witnesses, not just failed tactics.
- The first structured export had pretty-print truncation in large explicit types. It remains saved. `formal-declarations-full.json` and its exporter were regenerated under higher printing limits; all named `type_explicit` and definition bodies have no ellipses. Ordinary readable types may suppress proof terms.

## Files for the coordinator

1. `formal-only/packet.json`: hashed blind packet with comment-free real source, actual declarations, explicit types/definitions, #print/#print axioms output, toolchain, package pinning and runtime search paths. It contains no author-intent prose or audit verdict. The transformed source itself compiled as blind-source-01. `blind-transform.json` records the sole removed comment and both hashes.
2. `HUMAN-CONTRACT.md`: separate per-target intended statements, domains, assumptions, boundary cases and exclusions. Do not give it to the first blind reader. Give it to the separate semantic comparison reviewer afterward.
3. `per-declaration-axioms.json`, `export-coverage.json`: coverage and axiom extraction for every named main declaration and positive counterexample.
4. `author-result.json`, `execution-summary.json`: compact author-side results. These do not manufacture an independent review.

## Exact remaining scope

Fresh isolated blind readback and a separate intended-versus-formal semantic check remain for the coordinator. No Sturm-Liouville theory, infinite-dimensional operator, Prüfer phase differential equation or lift, spectral/phase index identification, comparison bound, floating-point/interval enclosure, executable root enumerator or its termination is formalized here. Strictly increasing indices may skip levels; full coverage requires choosing the desired consecutive indices. Unboundedness is not assumed or derived, so all-level root existence remains conditional on the supplied brackets. Vector algebra does not certify feasible ordered interfaces, clipping, normalization, Hessian sectors or global extremizers.

All task-created files are under the authorized formal-author directory. No project, old evidence, plugin or Git write was performed. `external-input-postcheck.json` covers only the explicitly recorded read inputs, not a full-project protection audit; concurrent project maintenance by the coordinator is outside this author's evidence scope. AGENTS.md records the method and actual dialogue/task constraints.
