# 数学工具库

## 文献吸收 (2026-09-23)

[来源指针表](../literature/absorption-20260923/SOURCE_TABLE.md)区分原文与项目适配。新卡以实际审查版本接入：

| 用途 | 当前工具 |
| --- | --- |
| 含域的奇偶分解与临界条件 | [幺正分解](krein-parity-unitary.md)、[分数域字典](krein-fractional-trace-dictionary.md) |
| 余有限闭包与边界代数 | [s=3三迹](krein-s3-cofinite-three-traces.md)、[右逆与GKN范围](krein-boundary-right-inverses.md) |
| 稳定近似 | [有限TSVD](finite-synthesis-tsvd.md)、[Legendre相容Riesz系](krein-integrated-legendre-riesz.md) |
| 无限删项 | [真实矩/Müntz接口](full-muntz-krein-moment-interface.md)、[两个子类](krein-infinite-deletion-subclasses.md) |
| 移动界面 | [二阶公式](finite-interface-second-derivative.md)、[固定算子适用性](fixed-operator-boundary-extension-check.md)、[测度与集中](measure-weight-atoms-and-concentration.md) |

原作者稿的待审标签保留提交时状态；当前回执在卡片review_status/evidence中。使用前仍核对条件。L13只作待获取完整原文的批注，不支持任何已证步骤。第五轮段落中s=3当时开放的状态已由本批限定的余有限分类更新；无限删项一般情形仍开放。

## 第九轮修订 (2026-09-23)

[二阶变分](second-variation-weighted-eigenvalues.md)补齐归一化核项、真实块积分切向和带符号集中脉冲的质量收敛条件; Green核有限及移动界面加速度分别处理. [世俗根计数](secular-chebyshev-jacobi-rootcount.md)区分物理F与omega*F, [平衡候选极限](bloch-band.md)用嵌套Jacobi矩阵证明候选c_n的严格单调和极限, 保留全局O1/O2开放. 精确版本和默认复用仍由纠错门禁决定, 不能由本段文字替代. [第九轮报告](../reports/proof-audit-round9-20260923/REPORT.md)记录首次退回、修复、局部Lean与实际数值复验.

## 第八轮修订 (2026-09-22)

[INF极限](inf-limit-comparison.md)、[大w比较](lemma-A-doubleprime.md)、[相位括号](delta-bracketing.md)、[余切余项](cot-series-certificate.md)已按当前精确版本修订. 新连续相位覆盖替代旧薄层网格, 固定u误差改为1/R; 根像端点、Laurent幂次、局部一致收敛与arctan极限同步修正. 默认复用须通过当前纠错回执, 旧证据和批注按原版本保留. [第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md)分别列明解析、精确证书和局部Lean范围.


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

第九轮使用已安装的研究插件2.0.1纠错与检验运行时; 本轮未改插件实现或缓存. 命令入口随实际加载版本确定, 源码维护仓库为 `_xsoc1_work/`; 复用时以版本报告和真实运行记录核对.

## 第七轮修订 (2026-09-21)

[FH](feynman-hellmann.md)和[谱隙](gap-band-extremals.md)修正真实归一化与镜像成对导数. [等变性](band-selfconsistency-equivariance.md)、[半问题Green](half-problem-regularized-green.md)、[惯性](green-half-inertia.md)同步修正行列式与定性的逻辑边界、lambda因子和半隙坐标. 五张当前卡均由精确版本纠错回执控制, 原版本与失败路线保留; 历史Green推导没有因此整体重新获证. [第七轮报告](../reports/proof-audit-round7-20260921/REPORT.md)列出统一端点估计、一般SUP极限、软件回归和局部Lean的不同验收范围.

## 第六轮修订 (2026-09-21)

[投影与有限矩准则](constrained-denseness-runs.md)修复三项问题, 采用实际尾部正交障碍上的有限检验; 原F的假设无实例, 一个表示元的非零检测不等于两个矩分别为零. [谱域工具](spectral-domain-checks.md)给出原完整命名族的精确非负稠密范围0<=s<7/2, 由四迹图核心补证. 九张相关卡和继承义务均按当前版本审查并释放; 旧源和批注保留. 第五轮s=2删除分类范围不扩大. [第六轮报告](../reports/proof-audit-round6-20260921/REPORT.md)区分解析验收、局部Lean和首次摘要退回.

## 第五轮修订 (2026-09-21)

[余有限稀疏族与两条迹](leftdef-o1pld-l2-structural.md)撤回原Claim4/Theorem5/Corollary6的错误候选, 给出s=2的完整余有限闭包、两个Green障碍及实际闭子空间分类. 单项式有限删除引理的换元系数和证明同时修复. 原封存run保持不变, 当前复用以新版精确回执为准; 一般非余有限O1'LD与s=3的对应分类仍开放. [第五轮报告](../reports/proof-audit-round5-20260921/REPORT.md)区分解析证明、37个局部Lean定理、四份隔离审查回执与额外的独立编译检查.

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
原稀疏族在 `s>=7/2` 时不全属于相应幂域; 第二轮当时保留的 `3<s<7/2` 问题已由第六轮四迹图核心补证关闭, 当前原完整族范围为 `0<=s<7/2`.
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
| band-selfconsistency-equivariance | [card](<band-selfconsistency-equivariance.md>) | 2 |
| banded-shift-toeplitz-density | [card](<banded-shift-toeplitz-density.md>) | 0 |
| bang-bang | [card](<bang-bang.md>) | 0 |
| bloch-band | [card](<bloch-band.md>) | 1 |
| cell-merging | [card](<cell-merging.md>) | 0 |
| constrained-denseness-runs | [card](<constrained-denseness-runs.md>) | 1 |
| cot-series-certificate | [card](<cot-series-certificate.md>) | 1 |
| delta-bracketing | [card](<delta-bracketing.md>) | 0 |
| denseness-criteria | [card](<denseness-criteria.md>) | 0 |
| endpoint-collapse-reduction | [card](<endpoint-collapse-reduction.md>) | 0 |
| feynman-hellmann | [card](<feynman-hellmann.md>) | 1 |
| fh-hessian-branch-reduction | [card](<fh-hessian-branch-reduction.md>) | 0 |
| finite-interface-second-derivative | [card](<finite-interface-second-derivative.md>) | 1 |
| finite-synthesis-tsvd | [card](<finite-synthesis-tsvd.md>) | 1 |
| fixed-operator-boundary-extension-check | [card](<fixed-operator-boundary-extension-check.md>) | 1 |
| fp-arm-max-root | [card](<fp-arm-max-root.md>) | 0 |
| full-muntz-krein-moment-interface | [card](<full-muntz-krein-moment-interface.md>) | 1 |
| gap-band-extremals | [card](<gap-band-extremals.md>) | 3 |
| gap-n1-reduction | [card](<gap-n1-reduction.md>) | 0 |
| general-alternating-secular-chebyshev | [card](<general-alternating-secular-chebyshev.md>) | 0 |
| good-root-global-lemma | [card](<good-root-global-lemma.md>) | 0 |
| green-half-inertia | [card](<green-half-inertia.md>) | 2 |
| half-problem-regularized-green | [card](<half-problem-regularized-green.md>) | 2 |
| helly-compactness | [card](<helly-compactness.md>) | 0 |
| inf-limit-comparison | [card](<inf-limit-comparison.md>) | 1 |
| interval-ad-certificate | [card](<interval-ad-certificate.md>) | 0 |
| interval-dec-directed-rounding | [card](<interval-dec-directed-rounding.md>) | 0 |
| jump-stability | [card](<jump-stability.md>) | 1 |
| keller-variational | [card](<keller-variational.md>) | 0 |
| key-lemma-decomposition | [card](<key-lemma-decomposition.md>) | 0 |
| kp-odd-firstzero-reduction | [card](<kp-odd-firstzero-reduction.md>) | 0 |
| kpdet-common-beta-sign | [card](<kpdet-common-beta-sign.md>) | 0 |
| krein-boundary-right-inverses | [card](<krein-boundary-right-inverses.md>) | 1 |
| krein-cofinite-closure-all-orders | [card](<krein-cofinite-closure-all-orders.md>) | 1 |
| krein-fractional-trace-dictionary | [card](<krein-fractional-trace-dictionary.md>) | 2 |
| krein-infinite-deletion-subclasses | [card](<krein-infinite-deletion-subclasses.md>) | 1 |
| krein-integrated-legendre-riesz | [card](<krein-integrated-legendre-riesz.md>) | 1 |
| krein-parity-unitary | [card](<krein-parity-unitary.md>) | 1 |
| krein-power-domain-polynomial-obstruction | [card](<krein-power-domain-polynomial-obstruction.md>) | 0 |
| krein-s3-cofinite-three-traces | [card](<krein-s3-cofinite-three-traces.md>) | 2 |
| krein-sobolev-polynomials | [card](<krein-sobolev-polynomials.md>) | 0 |
| lamplighter-range-translation-tv | [card](<lamplighter-range-translation-tv.md>) | 0 |
| largeR-level-cascade | [card](<largeR-level-cascade.md>) | 0 |
| left-definite-moment-recurrence | [card](<left-definite-moment-recurrence.md>) | 0 |
| left-definite-theory | [card](<left-definite-theory.md>) | 0 |
| leftdef-o1pld-l2-structural | [card](<leftdef-o1pld-l2-structural.md>) | 3 |
| lemma-A-doubleprime | [card](<lemma-A-doubleprime.md>) | 0 |
| liouville-transform | [card](<liouville-transform.md>) | 0 |
| m3-largeR-closure | [card](<m3-largeR-closure.md>) | 0 |
| m3-log-correction | [card](<m3-log-correction.md>) | 0 |
| mde-extremal | [card](<mde-extremal.md>) | 0 |
| measure-weight-atoms-and-concentration | [card](<measure-weight-atoms-and-concentration.md>) | 1 |
| moment-jump-completeness | [card](<moment-jump-completeness.md>) | 0 |
| morales-ramis-kovacic | [card](<morales-ramis-kovacic.md>) | 0 |
| mw-periodic-extension | [card](<mw-periodic-extension.md>) | 0 |
| mw-zero-truncation | [card](<mw-zero-truncation.md>) | 0 |
| phase-param-2d-certificate | [card](<phase-param-2d-certificate.md>) | 0 |
| phase-ratio-rigidity | [card](<phase-ratio-rigidity.md>) | 0 |
| prufer-phase | [card](<prufer-phase.md>) | 0 |
| r1plus-perturbation-sheet | [card](<r1plus-perturbation-sheet.md>) | 0 |
| ratio-energy-invariant | [card](<ratio-energy-invariant.md>) | 0 |
| ratio-first-pair-variational | [card](<ratio-first-pair-variational.md>) | 2 |
| rational-envelope-certificates | [card](<rational-envelope-certificates.md>) | 0 |
| reflection-branch-reduction | [card](<reflection-branch-reduction.md>) | 0 |
| residual-exactness | [card](<residual-exactness.md>) | 0 |
| second-variation-weighted-eigenvalues | [card](<second-variation-weighted-eigenvalues.md>) | 4 |
| secular-chebyshev-jacobi-rootcount | [card](<secular-chebyshev-jacobi-rootcount.md>) | 1 |
| single-well-intersection | [card](<single-well-intersection.md>) | 0 |
| spectral-domain-checks | [card](<spectral-domain-checks.md>) | 3 |
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
