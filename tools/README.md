# 数学工具库

[按数学问题阅读](../docs/research-guide.md) | [问题地图](../research_map.md) | [数值与证书接口](../scripts/README.md)

工具卡服务于检索和复用. 读取具体范围, 原证明和精确版本证据后再使用; 卡片保存, 检索可用, 独立审查与自动接收是不同状态.

## 三个位置的职责与消费者

| 位置 | 实际内容 | 使用者 |
| --- | --- | --- |
| [tools/](./) | 当前可读数学卡片和本索引; 当前 index 的 tool_roots=['tools'] | 人类读者, 插件 research_library.py 的卡片读取/保存/检索 |
| `knowledge/tools/` | 原管理布局的保留位置, 当前为空 | 旧 init_project.py/validate_project.py 仍要求此目录; 当前卡片索引不从这里取卡 |
| [research/library/](../research/library/) | sources, annotations, card-versions/card-bindings, index-history, reviews 与 corrections | 现行库插件的版本绑定, 原文读取, 批注, 审查/纠错门禁 |

[index/tools.json](../index/tools.json) 是派生检索指针. 下方 generated 区块来自它的既有生成流程; 本次只编辑人工说明, 保留该区块原字节, 不重建索引或改动卡片/接收记录. Blueprint 的 canonical 图与 inventory 位于 blueprint/, 与工具库职责分开.

## 按用途查卡

| 主题 | 当前入口及使用限制 |
| --- | --- |
| 空间和算子域 | [真实谱域](spectral-domain-checks.md), [幂域障碍](krein-power-domain-polynomial-obstruction.md), [域字典](krein-fractional-trace-dictionary.md), [奇偶桥](krein-parity-unitary.md); 固定模型的真实域与代数传输分开 |
| 原族/删项/有限约束 | [余有限全窗口](krein-cofinite-closure-all-orders.md), [任意保留集](krein-infinite-deletion-subclasses.md), [有限约束筛选](krein-finite-constraint-filtering.md); 固定 c>0, 0<=s<7/2, 收敛侧全部元素仍开放 |
| 稳定替代系 | [整数 Hermite-Legendre](krein-integrated-legendre-riesz.md), [有限 TSVD](finite-synthesis-tsvd.md); 原族非基结论保留, 速率另有条件 |
| 一般稠密/矩递推 | [修后投影准则](constrained-denseness-runs.md), [左定矩](left-definite-moment-recurrence.md), [矩跳跃](moment-jump-completeness.md), [三阶递推](third-order-recurrence.md); 一般 A3/A4 与非齐次推广仍开放 |
| 比值与谱隙 | [首对变分](ratio-first-pair-variational.md), [MW 零点接口](mw-zero-truncation.md), [FH](feynman-hellmann.md), [谱隙](gap-band-extremals.md); 卡片可读不等于门禁允许复用 |
| 模态与 Green | [DD 频率枚举](indexed-dd-frequency-enumeration.md), [半问题核](half-problem-regularized-green.md), [惯性](green-half-inertia.md); omega/omega², raw K/SKS 和一基身份分开 |
| 变分与证书 | [有界方向及谱尾](second-variation-weighted-eigenvalues.md), [有限界面](finite-interface-second-derivative.md), [精确 Taylor](exact-taylor-sign-boundary.md); 有界方向与 delta 路径不同, 浮点误差不作认证包络 |

数学范围和原生审查分别见 [R14](../reports/proof-audit-round14-20261004/REPORT.md), [R15](../reports/proof-audit-round15-20261005/REPORT.md), [R16](../reports/proof-audit-round16-20261006/REPORT.md). 旧自动适配器拒收 task_name/fork_turns 原生身份的缺口仍保留, 不伪造旧 UUID 或放行隔离. R16 的 60 可检索/34 阻断是当时快照, 当前检索需现场查询.

## 使用与纠错

1. 先查下方指针, 读取卡片的条件/原证明. 正式查询使用**当前安装插件**的 research_library.py query --project <root> --query <terms>, 它会重新检查纠错门禁. 旧手工索引不覆盖隔离.
2. 需要历史隔离条目时显式 --include-affected, 结果只供溯源. RETRIEVAL_ONLY 不等于数学自动接收.
3. 发现实质错误按原版 research_corrections.py issue 绑定出错版本与下游. 受影响事项修后需独立新会话审查, 再按原机制处理精确版本的释放. 修改说明或索引不释放任何事项.
4. annotate 的批注绑定卡片版本. 本次编辑的导航有历史整文件输入绑定, 旧批准仅覆盖原快照, 不转给新说明; 具体影响记在 [会话日志](../state/AGENTS_SESSION_LOG.md#2026-10-08-仓库入口与续接整理).

文献来源与原文读取位置见 [SOURCE_TABLE](../literature/absorption-20260923/SOURCE_TABLE.md); L13 仍为元数据/不完整预览, 不支持已证步骤. [人的理解和批注](../docs/PROJECT_UNDERSTANDING.md) 保留自由分析职责.

## 历史

[本页整理前全文](../docs/history/tools-README.pre-organization-20261008.txt) 保留逐轮范围与 generated 指针原文, 路径按原 tools/README.md 解释. [更早索引](../docs/history/tools-index-before-round2-20260920.md), 各报告, 原失败及 [会话日志](../state/AGENTS_SESSION_LOG.md) 保留当时语境; 当前主题入口不覆盖原证据.

<!-- research-tool-pointers:v1:start -->

## Generated retrieval pointers

Cards and notes are retrieval leads. Check their scope and evidence before reuse.

| Tool | Card | Annotations |
| --- | --- | --- |
| banded-shift-toeplitz-density | [card](<banded-shift-toeplitz-density.md>) | 0 |
| cell-merging | [card](<cell-merging.md>) | 0 |
| endpoint-collapse-reduction | [card](<endpoint-collapse-reduction.md>) | 0 |
| exact-taylor-sign-boundary | [card](<exact-taylor-sign-boundary.md>) | 0 |
| fh-hessian-branch-reduction | [card](<fh-hessian-branch-reduction.md>) | 0 |
| finite-interface-second-derivative | [card](<finite-interface-second-derivative.md>) | 1 |
| finite-synthesis-tsvd | [card](<finite-synthesis-tsvd.md>) | 1 |
| fixed-operator-boundary-extension-check | [card](<fixed-operator-boundary-extension-check.md>) | 1 |
| fp-arm-max-root | [card](<fp-arm-max-root.md>) | 0 |
| full-muntz-krein-moment-interface | [card](<full-muntz-krein-moment-interface.md>) | 1 |
| gap-n1-reduction | [card](<gap-n1-reduction.md>) | 0 |
| general-alternating-secular-chebyshev | [card](<general-alternating-secular-chebyshev.md>) | 0 |
| good-root-global-lemma | [card](<good-root-global-lemma.md>) | 0 |
| indexed-dd-frequency-enumeration | [card](<indexed-dd-frequency-enumeration.md>) | 0 |
| interval-ad-certificate | [card](<interval-ad-certificate.md>) | 0 |
| keller-variational | [card](<keller-variational.md>) | 0 |
| key-lemma-decomposition | [card](<key-lemma-decomposition.md>) | 0 |
| kp-odd-firstzero-reduction | [card](<kp-odd-firstzero-reduction.md>) | 0 |
| kpdet-common-beta-sign | [card](<kpdet-common-beta-sign.md>) | 0 |
| krein-boundary-right-inverses | [card](<krein-boundary-right-inverses.md>) | 1 |
| krein-cofinite-closure-all-orders | [card](<krein-cofinite-closure-all-orders.md>) | 1 |
| krein-finite-constraint-filtering | [card](<krein-finite-constraint-filtering.md>) | 0 |
| krein-fractional-trace-dictionary | [card](<krein-fractional-trace-dictionary.md>) | 2 |
| krein-infinite-deletion-subclasses | [card](<krein-infinite-deletion-subclasses.md>) | 1 |
| krein-integrated-legendre-riesz | [card](<krein-integrated-legendre-riesz.md>) | 1 |
| krein-parity-unitary | [card](<krein-parity-unitary.md>) | 1 |
| krein-power-domain-polynomial-obstruction | [card](<krein-power-domain-polynomial-obstruction.md>) | 0 |
| krein-s3-cofinite-three-traces | [card](<krein-s3-cofinite-three-traces.md>) | 2 |
| lamplighter-range-translation-tv | [card](<lamplighter-range-translation-tv.md>) | 0 |
| largeR-level-cascade | [card](<largeR-level-cascade.md>) | 0 |
| liouville-transform | [card](<liouville-transform.md>) | 0 |
| m3-largeR-closure | [card](<m3-largeR-closure.md>) | 0 |
| m3-log-correction | [card](<m3-log-correction.md>) | 0 |
| mde-extremal | [card](<mde-extremal.md>) | 0 |
| measure-weight-atoms-and-concentration | [card](<measure-weight-atoms-and-concentration.md>) | 1 |
| morales-ramis-kovacic | [card](<morales-ramis-kovacic.md>) | 0 |
| phase-param-2d-certificate | [card](<phase-param-2d-certificate.md>) | 0 |
| phase-ratio-rigidity | [card](<phase-ratio-rigidity.md>) | 0 |
| prufer-phase | [card](<prufer-phase.md>) | 0 |
| r1plus-perturbation-sheet | [card](<r1plus-perturbation-sheet.md>) | 0 |
| ratio-energy-invariant | [card](<ratio-energy-invariant.md>) | 0 |
| ratio-first-pair-variational | [card](<ratio-first-pair-variational.md>) | 2 |
| reflection-branch-reduction | [card](<reflection-branch-reduction.md>) | 0 |
| residual-exactness | [card](<residual-exactness.md>) | 0 |
| single-well-intersection | [card](<single-well-intersection.md>) | 0 |
| sturm-oscillation | [card](<sturm-oscillation.md>) | 0 |
| symline-n1-monotonicity | [card](<symline-n1-monotonicity.md>) | 0 |
| tension-ratio-chain | [card](<tension-ratio-chain.md>) | 0 |
| transfer-matrix-secular | [card](<transfer-matrix-secular.md>) | 0 |
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
