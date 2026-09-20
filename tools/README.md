# 数学工具库

工具库保存可复用的数学方法、适用条件、来源、批注及成功或失败路线.
它服务于研究, 每次使用仍要核对当前问题是否满足工具的假设.

## 怎样使用

1. 先查下方生成指针, 再读取卡片的适用范围与原证明.
2. 正式复用使用插件 `research_library.py query`; 程序会重新检查纠错状态.
   手工索引的旧副本或 `status: 已证` 不能覆盖当前隔离状态.
3. 发现错误时保留报告, 用 `research_corrections.py issue` 绑定出错版本;
   下游待复核. 修订后经新会话隔离检验, 才能恢复特定版本的复用.
4. 批注由 `research_library.py annotate` 绑定卡片版本. 旧批注和失败路线保留,
   不把旧版的认可自动转给新版. 历史隔离条目需显式 `--include-affected` 查看.

命令入口随已加载插件版本确定; 本轮开发实现位于插件源码仓库 `_xsoc1_work/`,
是否已发布和安装见对应版本报告, 不从目录存在推断安装成功.

## 第四轮修订 (2026-09-21)

[三阶递推](third-order-recurrence.md)给出指定双奇偶系数族的正项尾解、一般c常数和全部有理比值分类; [K1锚点](third-order-minimal-K1.md)保留独立有限终端约定. [Krein-Sobolev](krein-sobolev-polynomials.md)区分普通函数代表与商类极限. [稳定性](jump-stability.md)及四张未改正文的卡片完成精确审计绑定续接. 原错误版本、退回记录和批注仍可溯源, 默认检索只按当前纠错状态复用. 证明、程序与局部Lean的不同范围见 [第四轮报告](../reports/proof-audit-round4-20260921/REPORT.md).

## 本轮修订入口

| 主题 | 工具 |
| --- | --- |
| 完整谱系、归一化、负阶完备化、成员性 | [谱系与幂域检查](spectral-domain-checks.md) |
| 增长条件、矩跳跃与精确适用阶数 | [左定矩递推](left-definite-moment-recurrence.md), [矩跳跃](moment-jump-completeness.md), [稠密性准则](denseness-criteria.md) |
| 全局首对极值与候选计算的分工 | [变分证明](ratio-first-pair-variational.md), [平衡相位](balanced-phase.md) |
| 有符号延拓、共同零点与谱指标 | [MW 胞延拓](mw-periodic-extension.md), [零点截断](mw-zero-truncation.md), [单调性归约](spectral-monotonicity-reduction.md) |
| K1 终端条件、归一化与极限 | [最小解 K1](third-order-minimal-K1.md) |

本轮精确结论: `x² in Ht iff t<3/2`, `p4 in Hs iff s<7/2` (非负阶).
原稀疏族在 `s>=7/2` 时不全属于相应幂域; `3<s<7/2` 的同族稠密性仍开放.
原“全阶算子域多项式基”解释已经撤回, 见 [幂域障碍](krein-power-domain-polynomial-obstruction.md).
首对全局最优性需要变分证明; 全序列相邻比值下确界为 1, 与固定指标问题分开.
详细检验、纠错回执及 Lean 范围见 [第二轮报告](../reports/proof-audit-round2-20260920/REPORT.md).

## 历史与证据边界

[原索引与逐次维护记录](../docs/history/tools-index-before-round2-20260920.md) 按原字节归档,
其中的旧状态和高阶推广不能作为当前结论. 历史文件中的相对路径基准是原 `tools/README.md`.
冻结证明、审计和 checkpoint 保持原身份. 错误清除意味着停止默认复用并修订活动内容,
而不是删除用于解释错误成因的证据.

下表是可再生的检索指针, 数学认证范围仍以各次精确声明的独立检验为准.

<!-- research-tool-pointers:v1:start -->

## Generated retrieval pointers

Cards and notes are retrieval leads. Check their scope and evidence before reuse.

| Tool | Card | Annotations |
| --- | --- | --- |
| balanced-phase | [card](<balanced-phase.md>) | 0 |
| band-selfconsistency-equivariance | [card](<band-selfconsistency-equivariance.md>) | 0 |
| banded-shift-toeplitz-density | [card](<banded-shift-toeplitz-density.md>) | 0 |
| bang-bang | [card](<bang-bang.md>) | 0 |
| bloch-band | [card](<bloch-band.md>) | 0 |
| cell-merging | [card](<cell-merging.md>) | 0 |
| constrained-denseness-runs | [card](<constrained-denseness-runs.md>) | 0 |
| cot-series-certificate | [card](<cot-series-certificate.md>) | 0 |
| delta-bracketing | [card](<delta-bracketing.md>) | 0 |
| denseness-criteria | [card](<denseness-criteria.md>) | 0 |
| endpoint-collapse-reduction | [card](<endpoint-collapse-reduction.md>) | 0 |
| feynman-hellmann | [card](<feynman-hellmann.md>) | 0 |
| fh-hessian-branch-reduction | [card](<fh-hessian-branch-reduction.md>) | 0 |
| fp-arm-max-root | [card](<fp-arm-max-root.md>) | 0 |
| gap-band-extremals | [card](<gap-band-extremals.md>) | 0 |
| gap-n1-reduction | [card](<gap-n1-reduction.md>) | 0 |
| general-alternating-secular-chebyshev | [card](<general-alternating-secular-chebyshev.md>) | 0 |
| good-root-global-lemma | [card](<good-root-global-lemma.md>) | 0 |
| green-half-inertia | [card](<green-half-inertia.md>) | 0 |
| half-problem-regularized-green | [card](<half-problem-regularized-green.md>) | 0 |
| helly-compactness | [card](<helly-compactness.md>) | 0 |
| inf-limit-comparison | [card](<inf-limit-comparison.md>) | 0 |
| interval-ad-certificate | [card](<interval-ad-certificate.md>) | 0 |
| interval-dec-directed-rounding | [card](<interval-dec-directed-rounding.md>) | 0 |
| jump-stability | [card](<jump-stability.md>) | 1 |
| keller-variational | [card](<keller-variational.md>) | 0 |
| key-lemma-decomposition | [card](<key-lemma-decomposition.md>) | 0 |
| kp-odd-firstzero-reduction | [card](<kp-odd-firstzero-reduction.md>) | 0 |
| kpdet-common-beta-sign | [card](<kpdet-common-beta-sign.md>) | 0 |
| krein-power-domain-polynomial-obstruction | [card](<krein-power-domain-polynomial-obstruction.md>) | 0 |
| krein-sobolev-polynomials | [card](<krein-sobolev-polynomials.md>) | 0 |
| lamplighter-range-translation-tv | [card](<lamplighter-range-translation-tv.md>) | 0 |
| largeR-level-cascade | [card](<largeR-level-cascade.md>) | 0 |
| left-definite-moment-recurrence | [card](<left-definite-moment-recurrence.md>) | 0 |
| left-definite-theory | [card](<left-definite-theory.md>) | 0 |
| leftdef-o1pld-l2-structural | [card](<leftdef-o1pld-l2-structural.md>) | 0 |
| lemma-A-doubleprime | [card](<lemma-A-doubleprime.md>) | 0 |
| liouville-transform | [card](<liouville-transform.md>) | 0 |
| m3-largeR-closure | [card](<m3-largeR-closure.md>) | 0 |
| m3-log-correction | [card](<m3-log-correction.md>) | 0 |
| mde-extremal | [card](<mde-extremal.md>) | 0 |
| moment-jump-completeness | [card](<moment-jump-completeness.md>) | 0 |
| morales-ramis-kovacic | [card](<morales-ramis-kovacic.md>) | 0 |
| mw-periodic-extension | [card](<mw-periodic-extension.md>) | 0 |
| mw-zero-truncation | [card](<mw-zero-truncation.md>) | 0 |
| phase-param-2d-certificate | [card](<phase-param-2d-certificate.md>) | 0 |
| phase-ratio-rigidity | [card](<phase-ratio-rigidity.md>) | 0 |
| prufer-phase | [card](<prufer-phase.md>) | 0 |
| r1plus-perturbation-sheet | [card](<r1plus-perturbation-sheet.md>) | 0 |
| ratio-energy-invariant | [card](<ratio-energy-invariant.md>) | 0 |
| ratio-first-pair-variational | [card](<ratio-first-pair-variational.md>) | 1 |
| rational-envelope-certificates | [card](<rational-envelope-certificates.md>) | 0 |
| reflection-branch-reduction | [card](<reflection-branch-reduction.md>) | 0 |
| residual-exactness | [card](<residual-exactness.md>) | 0 |
| second-variation-weighted-eigenvalues | [card](<second-variation-weighted-eigenvalues.md>) | 0 |
| secular-chebyshev-jacobi-rootcount | [card](<secular-chebyshev-jacobi-rootcount.md>) | 0 |
| single-well-intersection | [card](<single-well-intersection.md>) | 0 |
| spectral-domain-checks | [card](<spectral-domain-checks.md>) | 1 |
| spectral-monotonicity-reduction | [card](<spectral-monotonicity-reduction.md>) | 0 |
| sturm-oscillation | [card](<sturm-oscillation.md>) | 0 |
| switch-saturation-k-invariant | [card](<switch-saturation-k-invariant.md>) | 0 |
| symline-n1-monotonicity | [card](<symline-n1-monotonicity.md>) | 0 |
| tension-ratio-chain | [card](<tension-ratio-chain.md>) | 0 |
| third-order-minimal-K1 | [card](<third-order-minimal-K1.md>) | 1 |
| third-order-recurrence | [card](<third-order-recurrence.md>) | 1 |
| transfer-matrix-secular | [card](<transfer-matrix-secular.md>) | 0 |
| true-curve-region-decomposition | [card](<true-curve-region-decomposition.md>) | 0 |
| two-block-gap-bounds | [card](<two-block-gap-bounds.md>) | 0 |
| weighted-shift-beta-lambda-density | [card](<weighted-shift-beta-lambda-density.md>) | 0 |
| well-family-rigidity | [card](<well-family-rigidity.md>) | 0 |
| workflow-blueprint-dag-ci | [card](<workflow-blueprint-dag-ci.md>) | 0 |
| workflow-divergent-search | [card](<workflow-divergent-search.md>) | 0 |
| workflow-eve-coevolution | [card](<workflow-eve-coevolution.md>) | 0 |
| workflow-first-error-taxonomy | [card](<workflow-first-error-taxonomy.md>) | 0 |
| workflow-hub-spoke-contract | [card](<workflow-hub-spoke-contract.md>) | 0 |
| workflow-kb-hash-wiki | [card](<workflow-kb-hash-wiki.md>) | 0 |
| workflow-sorrifier-decomposition | [card](<workflow-sorrifier-decomposition.md>) | 0 |
| workflow-statement-freeze | [card](<workflow-statement-freeze.md>) | 0 |

<!-- research-tool-pointers:v1:end -->
