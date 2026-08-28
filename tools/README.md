---
title: 数学工具库索引
tags: [mathtool, index]
created: 2026-08-04
---

# 数学工具库索引

本目录存放项目研究过程中从论文学到的与自研发现的数学工具/方法.
每个工具一个 Markdown 文件, 含**解析** (数学表述) 与**适用范围** (适用条件, 边界情形, 不适用情形), 以及验证状态.

## 更新规则 (实时更新)
1. 从论文学到新方法, 或在研究中发现新工具时, 新建一个 `tools/<slug>.md` 文件.
2. 同步更新本索引 (分类与表格).
3. 在 `AGENTS.md` 的会话记录中登记本次更新.
4. 数值验证过的结论必须写明验证方式与精度; 未验证的必须标注 `未验证` 或 `文献引用`.
5. 只允许使用英文标点.

## 验证状态标注约定 (数值 vs 严格)
速查表 `状态` 列与每个工具文件的 `status` 字段必须区分两类断言, 不得混淆:
- **严格证明/定理已证**: 有完整数学证明的结论 (如 `定理已证`, `已证`,
  `CANDIDATE_COMPLETE_PROOF` 仅当完成独立审计).
- **数值证据/数值验证**: 由计算支持的结论, **不构成证明**; 必须写明精度
  (如 `数值验证 (1e-8)`), 且不得表述为定理.
- **文献引用/评述级**: 依赖外部文献或仅转述, 须注明出处与核验程度.
- **猜想/开放**: 未证明的陈述, 必须明确标注 `猜想` 或 `开放`.
凡一个工具同时含严格部分与数值部分 (如 `gap-band-extremals`), 必须在文件中
分节说明各自状态. 数值检验永远不作为结果呈现.

## 分类索引

### 谱理论 (从论文学到)
- [[transfer-matrix-secular]] - 转移矩阵与 secular 方程
- [[prufer-phase]] - Prüfer 相位
- [[sturm-oscillation]] - Sturm 振荡理论
- [[feynman-hellmann]] - Feynman-Hellmann 公式
- [[liouville-transform]] - Liouville 变换与 normal form
- [[bloch-band]] - Bloch 能带与带边比值

### 极值方法 (从论文学到)
- [[keller-variational]] - Keller 变分条件
- [[mw-periodic-extension]] - MW 周期延拓与倍指标恒等式
- [[mw-zero-truncation]] - 零点截断归纳
- [[bang-bang]] - bang-bang 原理
- [[helly-compactness]] - Helly 紧性与极值存在性
- [[mde-extremal]] - 测度微分方程 (MDE) 极值方法
- [[morales-ramis-kovacic]] - Morales-Ramis 理论与 Kovacic 算法
- [[single-well-intersection]] - 单阱/单垒交点计数法

### 左定理论与正交多项式 (从论文学到)
- [[left-definite-theory]] - 左定理论与 Hilbert 空间尺度
- [[krein-sobolev-polynomials]] - Krein-Sobolev 正交多项式

### 自研方法与技巧
- [[band-selfconsistency-equivariance]] - 带状自洽等变性: F(R,x̄)=PF(R,x) + 反对合 J=-PJP + 拓扑度唯一性框架 (会话 58 续作 4b, 2026-08-12)
- [[balanced-phase]] - 平衡相位方法 (会话 5)
- [[spectral-monotonicity-reduction]] - 谱单调性归约 (会话 5)
- [[cell-merging]] - 胞界合并构造 (会话 5)
- [[moment-jump-completeness]] - 矩跳跃完备性判据 (会话 9)
- [[left-definite-moment-recurrence]] - 左定矩跳跃: H^s 完备性判据 (会话 10)
- [[left-definite-orthogonal-systems]] - 左定传输正交系: H^s 显式完备正交多项式系 (会话 11)
- [[krein-power-domain-polynomial-obstruction]] - Krein 幂算子域中的代数多项式逆障碍, 以及抽象完备化与算子域的精确接口
- [[denseness-criteria]] - 稠密性准则: 矩刻画/一阶/跳变判据与对角临界 3/2 (会话 11)
- [[jump-stability]] - 跳变稳定性: 增长引理定量形式与 omega(log) 门槛 (会话 11)
- [[third-order-recurrence]] - 三阶递推积分解理论: 积分解分类/精确降阶/最小解 (会话 11)
- [[third-order-minimal-K1]] - Strict c=1 even minimal-solution anchor K(1)=e/4 (R-20260824T184147Z-k1-e4-ab, 2026-08-25)
- [[gap-band-extremals]] - 带状自洽极值判据: 相邻间距驻点条件与 FH 对称加倍 (会话 13)
- [[largeR-level-cascade]] - 大 R 层级级联平衡: band 系统整数幂级数层级结构/硬常数机制/分族平移层 (会话 105, R-210/R-211, 审计 R-212)
- [[m3-log-correction]] - M3 对数修正假设: 截断整数幂无根 + 数据拟合 u^2 主导 + log u 匹配渐近下一步 (会话 108, 2026-08-16, EVIDENCE)
- [[constrained-denseness-runs]] - 边界约束子空间多项式稠密性: 矩刻画/游程图/对角完整分类 (会话 106, R-20260814T070000Z-densbc)
- [[banded-shift-toeplitz-density]] - 稳定移位带 Toeplitz 空间 O1' 有限秩判据: 带宽 m>=1 非对角推广 (R-20260823T000000Z-o1p-baseline, 2026-08-23)
- [[weighted-shift-beta-lambda-density]] - 加权移位族 H_{beta,lambda} O1' 判据: beta>3/2 无穷游程可实现门槛 (R-20260823T000000Z-o1p-lightreuse, 2026-08-23)
- [[leftdef-o1pld-l2-structural]] - 左定 O1'LD 的 L^2 降维结构定理 (有限支撑矩刚性/无限游程不可实现/奇偶分解, R-20260823T030000Z-leftdef-o1pld, 2026-08-23)
- [[lamplighter-range-translation-tv]] - Lamplighter 平移 TV: 可见包络精确充分统计量, 改进下界, 对数上界, one-sided 界, killed-kernel 与 coarea 归约 (pilot v5 Arms A/C + v1.7 regression, 2026-08-27)
- [[gap-n1-reduction]] - 两块族归约定理 (O1, 2026-08-05)
- [[two-block-gap-bounds]] - 两块相位间距界 3pi^2/R < D < 3pi^2 (O3b, 2026-08-05)
- [[key-lemma-decomposition]] - KEY LEMMA 分解 + 逐项 q-单调性否证 + (LOG)/(FP) 全解析证明 (O2, 2026-08-05/09)
- [[fh-hessian-branch-reduction]] - FH 带特征值因子 + Hessian/分支斜率归约 (O3a, 2026-08-06)
- [[interval-ad-certificate]] - 区间自动微分证书: 隐式斜率符号的严格判定 (O3a, 2026-08-06)
- [[reflection-branch-reduction]] - 反射分支归约: R1-R6 把 C1 归约到 E1+M (O3a, 2026-08-06)
- [[lemma-A-doubleprime]] - 引理 A'' 下界: 相位坐标差量法 (INF 极限, 会话 30, 2026-08-07)
- [[delta-bracketing]] - 相位括号: 隐式 secular 根的初等夹逼 (会话 30, 2026-08-07)
- [[cot-series-certificate]] - 余切级数余项证书: C_z < 0.337 类显式常数 (会话 30, 2026-08-07)
- [[inf-limit-comparison]] - 极限系统比较法: 大参数极限 T1/T2/T3 框架 (会话 30, 2026-08-07)
- [[r1plus-perturbation-sheet]] - 一阶摄动片层法: R->1+ 片层 a = a0 + eps*phi(b) (会话 33 续, 2026-08-08)
- [[fp-arm-max-root]] - fp 臂最大根列追踪: S3 近竖直分支列根 (会话 33 续, 2026-08-08)
- [[phase-ratio-rigidity]] - 相位比刚性: good root 唯一性/对称性 (O3a, 2026-08-09)
- [[well-family-rigidity]] - 阱族相位比刚性: 一切 R>1 good root 对称性 (INF 侧, 2026-08-10 会话 56, 全 R 已证)
- [[symline-n1-monotonicity]] - 对称线 1D 单调性: KEY LEMMA (F~_e 唯一零点) + 精确降维恒等式 (缺口 (a) 闭合, 会话 52, 2026-08-10)
- [[tension-ratio-chain]] - 张力比链: 比值上界化到退化极限 + 一维单峰不等式 (缺口 (a') 全 R 闭合, 会话 58 续作, 2026-08-12)
- [[good-root-global-lemma]] - good-root 全局引理: Wronskian 比值单调 + f 零点唯一性, 内部临界点自动 sign-consistent (缺口 (d) 闭合, 会话 58 续作 2, 2026-08-12)
- [[endpoint-collapse-reduction]] - 端点塌缩归约: w1->0 必得带匹配约化根且 q0=c (框架约定; 会话 58 续作 7/8, 2026-08-13; 已被 (G2) 直接闭合超越)
- [[phase-param-2d-certificate]] - 二维相位参数化证书: 相位方程显式反解 + 2D 叶盒 (O3a I3, 2026-08-09)
- [[true-curve-region-decomposition]] - 真曲线区域分解: T1/T2 双侧全解析化 (定理 5.8 + 5.14, O3a I3, 会话 40/41)
- [[interval-dec-directed-rounding]] - 十进制定向舍入区间引擎: 单变量符号事实的严格认证 (O3a I3, 会话 40 续, 2026-08-09)
- [[rational-envelope-certificates]] - 有理包络证书: 交错级数包络 + 精确有理区间链 (会话 44, 2026-08-09)
- [[switch-saturation-k-invariant]] - 开关饱和与块能量不变量: FH 完全盒饱和 + 零点=开关 + K=-2D (会话 50, 2026-08-10)
- [[ratio-energy-invariant]] - 比值能量不变量: 固定 n 比值极大子结构, E=0 + q0=1/c + q1=-1/c (R-20260822T220000Z-b3-baseline, 2026-08-22)
- [[secular-chebyshev-jacobi-rootcount]] - 交替平衡世俗多项式 2n 根计数: 转移矩阵递推 + Chebyshev/Jacobi 谱论证 (R-20260822T220000Z-b3-baseline, 2026-08-22)
- [[general-alternating-secular-chebyshev]] - 一般等宽交替世俗 Chebyshev 表示: sin(p)[U_n+delta*U_{n-1}], delta=sin(q)/(s sin(p)) (R-20260823T060000Z-b3-current, 2026-08-23)
- [[green-half-inertia]] - 半问题 Green 惯性: 奇偶性更正 + 全局 ε 交错 + (G1') 的 Green 函数化归 (R-205, 2026-08-13)
- [[second-variation-weighted-eigenvalues]] - 加权特征值二阶变分 lambda'' 公式 + 移动框架与 delta' 边界层两陷阱 (R-206, 2026-08-13)
- [[half-problem-regularized-green]] - 半问题约化 Green 闭式: 无 rho(y) 因子约化预解核 + 精确 A1/A2 原函数 + K 两镜扇区闭式 (R-207, 2026-08-13)

### 研究工作流方法 (AI4Math V2 蒸馏, 2026-08-12)
来源: AI4Math 会议 V2 (2026.07.22-24, 浙大 IASM) 演讲者公开项目, 蒸馏报告见 [[ai4math_v2_workflow_distillation]].
- [[workflow-divergent-search]] - 发散式检索契约: 搜索宽不守门 + 来源诚实 + 分层检索 (MMAT searcher)
- [[workflow-hub-spoke-contract]] - hub-and-spoke 角色契约: orchestrator 只路由 + 草稿/证明/验证分离 (MMAT)
- [[workflow-sorrifier-decomposition]] - sorrifier 分解: 失败块 sorry 化保留骨架 + 子问题递归 (MechMath)
- [[workflow-statement-freeze]] - M2F 陈述冻结: 陈述编译 (允许 sorry) -> 冻结签名 -> 证明修复 (M2F/ReasBook)
- [[workflow-blueprint-dag-ci]] - 蓝图与 DAG 状态追踪: 目标契约 + 引理依赖图 + 新鲜上下文收敛检查 (LeanMarathon/Archon-Horizon)
- [[workflow-first-error-taxonomy]] - 首错定位与错误分类: first-error step + SCI 28 类四能力 (FaithSieve/FormalRx)
- [[workflow-kb-hash-wiki]] - hash 寻址知识库与 wiki 编译: 原始源不可变 + 编译层卡片 (KB-Manager)
- [[workflow-eve-coevolution]] - EvE 双种群进化: 可评分变异的边际收益演化 (EvE)

## 速查表

| 工具 | 来源 | 状态 | 类别 |
|---|---|---|---|
| [[transfer-matrix-secular]] | 经典数值法 | 已验证 (本项目全部数值) | 谱理论 |
| [[prufer-phase]] | 经典 | 文献引用 | 谱理论 |
| [[sturm-oscillation]] | 经典 | 文献引用 | 谱理论 |
| [[feynman-hellmann]] | 量子力学标准 | 文献引用 | 谱理论 |
| [[liouville-transform]] | 经典 | 文献引用 | 谱理论 |
| [[bloch-band]] | 周期介质理论 | 数值验证 (能带极限) | 谱理论 |
| [[keller-variational]] | Keller 1976 | 文献 + 数值 (1e-11) | 极值方法 |
| [[mw-periodic-extension]] | Mahar-Willner 1976 | 数值复现 (1e-8) | 极值方法 |
| [[mw-zero-truncation]] | Mahar-Willner 1976 | 文献引用 (未独立重证) | 极值方法 |
| [[bang-bang]] | 最优控制 | 文献引用 | 极值方法 |
| [[helly-compactness]] | 经典分析 | 文献引用 | 极值方法 |
| [[mde-extremal]] | Meng-Zhang 等 | 评述级 | 极值方法 |
| [[morales-ramis-kovacic]] | 微分 Galois 理论 | 文献引用 | 极值方法 |
| [[single-well-intersection]] | Hedhly 2021, Huang 1999 | 全文核验 | 极值方法 |
| [[left-definite-theory]] | Littlejohn-Wellman | 文献引用 | 左定理论 |
| [[krein-sobolev-polynomials]] | Littlejohn-Quintero-Roba 2025 | 姊妹论文还原 | 左定理论 |
| [[balanced-phase]] | 自研 (会话 5) | 数值验证 (1e-15) | 自研 |
| [[spectral-monotonicity-reduction]] | 自研 (会话 5) | 定理已证 | 自研 |
| [[cell-merging]] | 自研 (会话 5) | 数值验证 (1e-8) | 自研 |
| [[moment-jump-completeness]] | 自研 (会话 9) | 定理已证 + 精确有理数 | 自研 |
| [[left-definite-moment-recurrence]] | 自研 (会话 10) | 定理已证 + 精确有理数 | 自研 |
| [[left-definite-orthogonal-systems]] | 自研 (会话 11) | 定理已证 + 855 项精确有理数 | 自研 |
| [[denseness-criteria]] | 自研 (会话 11) | 定理已证 + 精确有理数 | 自研 |
| [[jump-stability]] | 自研 (会话 11) | 定理已证 + 精确有理数 | 自研 |
| [[third-order-recurrence]] | 自研 (会话 11) | 定理已证 + 符号/高精度 | 自研 |
| [[gap-band-extremals]] | 自研 (会话 13) | 机制严格 + 数值验证 (1e-9..1e-12) | 自研 |
| [[residual-exactness]] | 自研 (O3a, 2026-08-05) | 定理已证 + 数值验证 (~1e-7) | 自研 |
| [[gap-n1-reduction]] | 自研 (O1, 2026-08-05) | CANDIDATE_COMPLETE_PROOF (2026-08-06 修复: S_rho 自伴 + 跳点符号 + 平滑论证; 自审 O1a-O1f 全过, 独立复审待办) | 自研 |
| [[two-block-gap-bounds]] | 自研 (O3b, 2026-08-05) | 定理已证 + 4000 点零违例 | 自研 |
| [[key-lemma-decomposition]] | 自研 (O2, 2026-08-05) | KEY LEMMA 已证 (2026-08-06 独立审计); (LOG) 2026-08-09 全解析化 (thm:LOG) | 自研 |
| [[fh-hessian-branch-reduction]] | 自研 (O3a, 2026-08-06) | 定理已证 (P1-P3) + 数值/区间验证 | 自研 |
| [[interval-ad-certificate]] | 自研 (O3a, 2026-08-06) | 已实现并通过 (CE-1 严格化) | 自研 |
| [[lemma-A-doubleprime]] | 自研 (会话 30, 2026-08-07) | 已证 (解析 + 三常数区间认证; v 参数已更正) | 自研 |
| [[delta-bracketing]] | 自研 (会话 30, 2026-08-07) | 已证 (初等单调夹逼) | 自研 |
| [[cot-series-certificate]] | 自研 (会话 30, 2026-08-07) | 已证 (正系数级数 + 区间值) | 自研 |
| [[inf-limit-comparison]] | 自研 (会话 30, 2026-08-07) | 已证 (定理 A, T1/T2/T3 闭合) | 自研 |
| [[r1plus-perturbation-sheet]] | 自研 (会话 33 续 + 会话 34, 2026-08-08/09) | 闭式已得 (DERIVATION); phi' > 0 CERTIFIED+STRICT; b_top* > b0 STRICT; 余留 Gap 1 | 自研 |
| [[phase-ratio-rigidity]] | 自研 (O3a, 2026-08-09) | 解析 + 两类证书 (2026-08-09: $\partial_qM_2<0$ 与 C4 均全解析) | 自研方法 |
| [[well-family-rigidity]] | 自研 (INF 侧, 2026-08-10 会话 56) | 定理已证 (STRICT, 一切 R>1; all-R 文档 14 页零警告 + 总结 8 页零警告; sympy 约束下精确; 数值为 EVIDENCE) | 自研方法 |
| [[symline-n1-monotonicity]] | 自研 (会话 52, 2026-08-10) | 定理已证 (STRICT, 10 页零警告; W0 证书 sympy 全过; 数值为 EVIDENCE) | 自研方法 |
| [[tension-ratio-chain]] | 自研 (会话 58 续作, 2026-08-12) | 定理已证 (STRICT, 9 页零警告; 精确有理证书 C1-C5 ALL PASS; 数值为 EVIDENCE) | 自研方法 |
| [[good-root-global-lemma]] | 自研 (会话 58 续作 2, 2026-08-12) | 定理已证 (STRICT, 6 页零警告; 数值交叉检验为 EVIDENCE) | 自研方法 |
| [[endpoint-collapse-reduction]] | 自研 (会话 58 续作 7/8, 2026-08-13) | 归约 STRICT (已证, q0=c 框架约定修正); (G2) 已由 [[switch-saturation-k-invariant]] 闭合 STRICT, 约化根不存在为 STRICT | 自研方法 |
| [[phase-param-2d-certificate]] | 自研 (O3a I3, 2026-08-09) | E1 端点闭式 + 2D 叶盒 (J1/J2 证书均已移除, 分别由定理 5.8/5.14 取代) | 自研方法 |
| [[true-curve-region-decomposition]] | 自研 (O3a I3 去证书化, 2026-08-09) | E1 双侧完成: 定理 5.8 (J1, 6499/7500) + 定理 5.14 (J2, W-分解链, mu >= 27921/20000); 67 叶盒移除 | 自研方法 |
| [[interval-dec-directed-rounding]] | 自研 (O3a I3, 2026-08-09) | 已退役历史 (L7/L8/L9); 被有理包络证书 L10/L11/L12 取代 | 自研方法 |
| [[rational-envelope-certificates]] | 自研 (会话 44, 2026-08-09) | E1 证书链 57/57 PASS (L10/L11/L12); 55 项事实全部 E1, 不依赖验证器内核 | 自研方法 |
| [[switch-saturation-k-invariant]] | 自研 (会话 50, 2026-08-10; 更新 会话 58 续作 8, 2026-08-13) | 定理已证 (独立审计 PASS); 2026-08-13 应用: K 恒等式 + 精确零点公式 + 内部零点简单性 闭合 (G2) STRICT | 自研方法 |
| [[ratio-energy-invariant]] | 自研 (R-20260822T220000Z-b3-baseline, 2026-08-22) | 定理已证 (STRICT) | 自研方法 |
| [[secular-chebyshev-jacobi-rootcount]] | 自研 (R-20260822T220000Z-b3-baseline, 2026-08-22) | 定理已证 (STRICT) | 自研方法 |
| [[general-alternating-secular-chebyshev]] | 自研 (R-20260823T060000Z-b3-current, 2026-08-23) | 定理已证 (STRICT; 未独立审计) | 自研方法 |
| [[band-selfconsistency-equivariance]] | 自研 (会话 58 续作 4b, 2026-08-12; 更新 2026-08-13) | 等变恒等式与反对合结构 STRICT; 框架定理已证; (G2) 已闭合 STRICT (2026-08-13); (G1') 开放 | 自研方法 |
| [[green-half-inertia]] | 自研 (R-205, 2026-08-13) | 全局 ε 交错与 Green 惯性 STRICT; 奇偶性否证 (EVIDENCE); (G1') 仍开放 | 自研方法 |
| [[second-variation-weighted-eigenvalues]] | 自研 (R-206, 2026-08-13) | lambda'' 公式 STRICT; P1/P2/P3 EVIDENCE; 交接二阶系数路线否证 (delta' 机制 STRICT) | 自研方法 |
| [[half-problem-regularized-green]] | 自研 (R-207/208, 2026-08-13) | 闭式/扇区/锚点 STRICT: (G1') 于 (1,1+δ) 一切 n, (I1)/(I2) 于 (1,1+δ) n=2; 剩余 (M1)-(M3) 开放 | 自研方法 |
| [[largeR-level-cascade]] | 自研 (会话 105, R-210/R-211 + 审计 R-212, 2026-08-14) | STRICT 结构经独立审计 (INDEPENDENTLY_AUDITED_PROOF, F-NL3 更正); 整数幂分支根开放 (K0->0 负结果 EVIDENCE); M3 总体 RIGOROUS_PARTIAL_RESULT | 自研方法 |
| [[m3-log-correction]] | 自研 (会话 108) | 数值证据 (RMSE 8e-7, 无严格证明) | 自研 |
| [[constrained-denseness-runs]] | 自研 (会话 106, run R-20260814T070000Z-densbc, 2026-08-14) | 定理 A-H STRICT (协调者审计, F-densbc-01 更正); 对角完整分类 (β<=3/2 且无有限游程); 两个包猜想被否证; 开放核 O1-O3 | 自研方法 |
| [[banded-shift-toeplitz-density]] | 自研 (R-20260823T000000Z-o1p-baseline, 2026-08-23) | STRICT: 稳定移位带 Toeplitz 空间 O1' 有限秩判据 (带宽 m>=1); 一般 O1' 仍开放 | 自研方法 |
| [[weighted-shift-beta-lambda-density]] | 自研 (R-20260823T000000Z-o1p-lightreuse, 2026-08-23) | STRICT (审计修复后): H_{beta,lambda} 加权移位 O1' 判据; 一般 O1' 仍开放 | 自研方法 |
| [[leftdef-o1pld-l2-structural]] | 自研 (R-20260823T030000Z-leftdef-o1pld, 2026-08-23) | STRICT: L^2 有限支撑矩刚性/无限游程不可实现/奇偶分解/cofinite-N 稠密; 一般 O1'LD 仍开放 | 自研方法 |
| [[lamplighter-range-translation-tv]] | 自研 (pilot v5 Arms A/C + v1.7 regression, 2026-08-27) | STRICT partial: 可见包络 TV 精确等式, 1/(2sqrt(t)) 下界, (2log(t)+15)/sqrt(t) 上界, one-sided 12/sqrt(t), killed-kernel/coarea; 常数阶 joint 上界 OPEN | 自研方法 |
| [[fp-arm-max-root]] | 自研 (会话 33 续, 2026-08-08) | 数值工具; 已记录伪根缺陷 (F-017) | 数值 |
| [[workflow-divergent-search]] | MMAT searcher (AI4Math V2) | 文献引用 (prompt 已读, 2026-08-12) | 研究工作流 |
| [[workflow-hub-spoke-contract]] | MMAT nl-prover / LeanMarathon | 文献引用 (prompt 已读, 2026-08-12) | 研究工作流 |
| [[workflow-sorrifier-decomposition]] | MechMath-v1 | 文献引用 (repo 描述, 2026-08-12) | 研究工作流 |
| [[workflow-statement-freeze]] | M2F / ReasBook | 文献引用 (README, 2026-08-12) | 研究工作流 |
| [[workflow-blueprint-dag-ci]] | LeanMarathon / Archon-Horizon | 文献引用 (README+docs, 2026-08-12) | 研究工作流 |
| [[workflow-first-error-taxonomy]] | FaithSieve / FormalRx | 文献引用 (repo+OpenAlex 摘要, 2026-08-12) | 研究工作流 |
| [[workflow-kb-hash-wiki]] | MMAT kb-manager | 文献引用 (README+prompts, 2026-08-12) | 研究工作流 |
| [[workflow-eve-coevolution]] | EvE (scaling-group) | 文献引用 (README+arXiv:2605.09018, 2026-08-12) | 研究工作流 |

## 维护日志
- 2026-08-27 (v1.7 closure-first regression): 更新 [[lamplighter-range-translation-tv]]. 新增独立中性审计 `PASS` 的可见包络 TV 精确等式, 完整状态质量有限公式, Route A 显式调和数上界/耦合障碍, 以及 `h_10^4(A,2)=(26,16,26)` 精确反例. 原常数阶 `C/sqrt(t)` 上界保持 OPEN. 工件位于 `runs/three-arm-pilot-v2/pilot-v5-codex-u2/v17-regression/arm-a-plugin-v17/`.
- 2026-08-28 (pilot v6 Arm A): 新增 [[krein-power-domain-polynomial-obstruction]]. STRICT 结论为 `Q_n^(s) in D(K_c^(s/2))` 当且仅当 `n in {0,1}`, 适用于一切 `c>0` 和整数 `s>=4`. 区分代数逆 `L_poly^(-r)` 与真正算子逆 `K_c^(-r)`, 并修正 [[left-definite-orthogonal-systems]] 的算子域解释. 内部与外部独立审计均 `PASS`.
- 2026-08-28 (pilot v6 final): 更新 [[krein-power-domain-polynomial-obstruction]]. Arm C 独立审计 `PASS` 的 STRICT graph-core 定理证明 `C[x] intersect D(K_c^(s/2))` 在算子域中稠密. Posthoc 独立审计进一步将完整次数谱 `{0,1} union {N:N>=2 floor(s/2)+2}` 升级为 STRICT; 此结果不计入任何 arm 分数. 总表在 `runs/three-arm-pilot-v2/pilot-v6-hs-domain/RESULTS.md`.
- 2026-08-26 (pilot v5 Arm A): 新增 [[lamplighter-range-translation-tv]]. 独立审计 PASS 的 STRICT partial theorem 包含 TV 下界 `1/(4sqrt(t))`, 对数损失上界 `(2log(t)+15)/sqrt(t)`, two one-sided `12/sqrt(t)` 界, fixed reflection route 障碍, killed-kernel 和 discrete coarea 归约. 常数阶 joint 上界明确保持 OPEN. 运行工件位于 `runs/three-arm-pilot-v2/pilot-v5-codex-u2/arms/a-plugin/`.
- 2026-08-27 (pilot v5 Arm C): QED 独立导出并经 fresh blind audit 确认 endpoint projection 下界 `1/(2sqrt(t))` for all `t>=1`, 同时确认 `(5+3log(t))/sqrt(t)` 上界. 工具主定理采用 Arm C 的更强下界和 Arm A 的已审计上界. 常数阶上界仍为 OPEN.
- 2026-08-13 (会话 97, R-206): 新增 [[second-variation-weighted-eigenvalues]] -- 加权特征值二阶变分. STRICT 公式 (固定空间广义特征问题 A=-d^2/dx^2, B=×ρ 于 H_0^1, 约束 <u_e,B_e u_e>=1, 四步推导): λ'' = 2λ<dr,u^2>^2 - 2λ^2 Σ_{l≠k} <dr u,u_l>^2/(λ_l-λ), 不加权配对, 两个求和分母同为 λ_l-λ; 移动空间框架 L^2(ρdx) 伪项 4λ<dr^2/ρ,u^2> 已登记为错误陷阱; 宽度路径二阶密度变分 d^2ρ = Σ s_i dw_i^2 δ'(x-x_i) 为 delta' 边界层 (STRICT 机制), 否证交接提议的 "naive 二阶变分 = 宽度 Hessian + 可控余项" (P3 符号级); SUP 切空间负定 (EVIDENCE), INF n=2 R=4 不定 (与 det K -> 0+ 一致); 全局 Kp 恒等式修正版 (ε-mask 内禀, 早前假正核草稿 RETRACTED, 见 scripts/_gapn2_k_global_rank2.py); 文献: Cox-McLaughlin I/II 仅 λ_1, Osmolovskii-Maurer 一般 bang-bang 二阶理论化归同一符号条件; 运行笔记 runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-13c.md; 脚本 scripts/_gapn2_second_variation_probe.py (P1/P2/P3).
- 2026-08-13 (会话 89, R-205): 新增 [[green-half-inertia]] -- 半问题 Green 惯性:
  否证交接摘要的 "回文高度 => 全局特征函数奇偶性" 线索 (奇偶性需要 ρ(1-x)=ρ(x),
  即宽度对称; 随机非对称宽度奇偶性/ f 偶性误差 O(1), 对称支 1e-16), 故镜像扇区/
  括号恒等式只在对称点成立, 不能反证对称性 (循环); 新增全局 ε 交错推论
  ε_j=(-1)^{j+1} (STRICT, 不依赖对称性, W<0 => Q 严格递减的胞腔证明), 是
  K 非对角闭式 (C1)/(C2) 在一切带自洽点成立的正确输入; 半问题谱交错
  (n 偶: λ_n=μ^D_{n/2}, λ_{n+1}=μ^N_{n/2+1}; n 奇: λ_n=μ^N_{(n+1)/2},
   λ_{n+1}=μ^D_{(n+1)/2}) 与 Green 惯性引理 (奇扇区约化预解核 R_n^⊥,
   R_{n+1}^⊥ 在 n 个左半开关上的负指数: n 偶各 n/2, n 奇 (n-1)/2 与 (n+1)/2,
   经典 Gantmacher-Krein), 给出 K_o = diag(d) + (4λ_n/λ_{n+1})diag(u)M diag(u),
   M = λ_{n+1}diag(ε)R_{n+1}^⊥diag(ε) - λ_n R_n^⊥ 的精确化归 (M 惯性混合,
   d 补足定号, 这是
  (G1') 的剩余障碍); 登记 D_n 非整体凹/凸的否证 (EVIDENCE); 脚本
  scripts/_gapn2_parity_global_probe.py, scripts/_gapn2_green_inertia_probe.py,
  _gapn2_bracket_identity_audit.py docstring 修正为对称点限定; 运行笔记
  run_notes_addendum_2026-08-13b.md. 同步更新 [[switch-saturation-k-invariant]]
  (全局 ε 交错推论).
- 2026-08-13 (会话 58 续作 8): (G2) 闭合 STRICT + 端点斜率约定修正. 修正
  [[endpoint-collapse-reduction]] 的 q0 约定 (框架约定 q0 := u'_{n+1}(0)/u'_n(0),
  塌缩条件 a=0 等价 q0=c; 早期 sqrt(lambda) 加权证据行撤回); 新增内部零点简单性
  引理 (f 无 f=f'=0 内点, Cauchy 数据唯一性 + Sturm); 应用 [[switch-saturation-k-invariant]]
  (K==-2D 给 q0*>1, q1*<-1; 精确零点 #Z(f*)=2n) 与带匹配保持矛盾, 闭合 (G2):
  紧 R 区间上带自洽解块宽一致有正下界, 任意塌缩级联均不可能; 脚本
  scripts/_gapn2_kidentity_audit.py 交叉 1e-11; 同步更新 [[switch-saturation-k-invariant]]
  与 [[band-selfconsistency-equivariance]] 状态.
- 2026-08-13 (会话 58 续作 7): 新增 [[endpoint-collapse-reduction]] -- 端点塌缩归约
  (STRICT, 已证): 交替 bang-bang 族带自洽解列若 w1 -> 0 (紧 R 区间), 则极限为带匹配
  的 2n 块约化系统根且满足端点条件 q0 = c, q0 = sqrt(lambda_{n+1})|u_{n+1}'(0)|
  /(sqrt(lambda_n)|u_n'(0)|), c = sqrt(lambda_n/lambda_{n+1}); 证明经特征值/特征函数
  连续依赖 + 带匹配保持 + 端点展开 f(x)=a x^2+O(x^4) 除 x1^2 取极限; 带匹配约化根处
  q0 < 1, 端点条件 q0 = c 需定量分离 (开放). 数值 (EVIDENCE): 完整分支上 q0/c > 1
  (n=2 R<=100, n=3 R<=30, n=4 R<=10, SUP/INF; 二次展开检验 f/(a x^2) -> 1 于 1e-4/1e-3;
  R->1 极限复现常数密度值 ((n+1)/n)^3); 随机与分支定向种子的约化根搜索未发现带匹配根,
  且所有约化根 q0-c > 0. 脚本 _gapn2_slope_ratio.py / _gapn2_reduced_endpoint_hunt.py
  / _gapn2_endpoint_targeted.py; 两处斜率计算 bug 已修 (块起始 M01 系数 + part_a 逐 R
  图案), 交接旧斜率数字全部撤回; 运行笔记
  runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-13.md.
- 2026-08-12 (会话 58 续作 5, 深夜段): 更新 [[band-selfconsistency-equivariance]] -- 新增
  非对角闭式 (C1)/(C2): T_ji = M~_ji/s_i = 2 lam_n u_i u_j Sigma'(x_i,x_j) - 4w_iw_j/D
  (同奇偶), 跨奇偶为 4w_iw_j(lam_{n+1}^2-lam_n lam_{n+1}+lam_n^2)/(lam_n lam_{n+1} D)
  - 2 lam_n u_i u_j Sigma_+(x_i,x_j) (STRICT, 1e-13..1e-15); 镜像扇区分解 (STRICT,
  1e-15..1e-16): K_e = diag(d)+E_e+H_e, K_o = diag(d)+E_o+H_o, E_e = c_e w_h w_h^T > 0,
  E_o = c_o (eps_h.w_h)(eps_h.w_h)^T < 0 (秩1闭式), H_e/H_o 奇偶掩码 + 镜像核闭式;
  eps_j = (-1)^{j+1} 严格交错 (STRICT); Hankel 对称 (P1') 证伪 (rel 0.6..1.2);
  支配不等式扫描 (EVIDENCE): SUP 侧 lammin(H_o-E_o)+mind > 0 与 lammin(H_e+E_e)+mind > 0
  全范围成立 (n=2 R<=100, n=3/4 R<=10); INF 侧朴素界大 R 失败 (n=3 R>=4),
  detK -> 0+ (R->inf) 无一致余量, 需定性论证; Sherman-Morrison 化归; 扇区主元
  SUP 全+/INF 全- (闭式, 全部扫描点); 脚本 _gapn2_mtilde_offdiag_identity.py,
  _gapn2_sector_decomposition.py + _gapn2_sector_scan_*.json; (G1') 仍开放,
  待证引理: 扇区核 R_k^||/R_k^bot 的 Green 估计.
- 2026-08-12 (会话 58 续作 5, 晚段): 更新 [[band-selfconsistency-equivariance]] -- 新增
  STRICT 恒等式 (I1) 部分分式: lambda_{n+1} G~_{n+1} - lambda_n G~_n = Sigma' - 2w_j/D
  - w_j D/(lambda_n lambda_{n+1}), Sigma' > 0; (I2) M~ 对角闭式: M~_{jj}/s_j = 2w_j Sigma'
  - 4w_j^2/D, 故 K_{jj} = sigma*2c|W|/(R-1) + 2w_jSigma'/lambda - 4w_j^2/(D lambda),
  sigma=+1(SUP)/-1(INF) (验证 1e-13..1e-15); (I3) 符号更正: f'(x_j)/s_j 对 SUP 恒正、
  INF 恒负 (早段笔记统一 "< 0" 仅 INF 成立); (I4) |W(x_j)| <= D (Cauchy-Schwarz);
  死路登记: Gershgorin 对角占优与 H-矩阵缩放 (rho(B)<1) 均在大 R 被数值否证
  (阈值见工具文件); 新 EVIDENCE: Sylvester 无换主元符号恒定 (SUP 全正/INF 全负),
  由惯性律等价于 (G1'); 脚本 _gapn2_diag_dominance.py / _gapn2_mtilde_diag_identity.py
  / _gapn2_hmatrix_probe.py; 运行笔记 run_notes_addendum_2026-08-12.md.
- 2026-08-12 (会话 80): 更新 [[band-selfconsistency-equivariance]] -- 首阶变分恒等式
- 2026-08-12 (会话 80): 更新 [[band-selfconsistency-equivariance]] -- 首阶变分恒等式
  符号审计 (STRICT, FD 1e-4..1e-6 级验证): 几何约定 delta_rho = -s_i delta(x-x_i) dx_i,
  dlambda_k/dx_i = +lambda_k s_i u_k(x_i)^2, dD/dx_i = -s_i f(x_i) (更正会话 51 记录的
  FH 跳点符号), Hess(D) = -lambda_{n+1} diag(s) J (更正 A3 记录符号),
  K = diag(1/s) J 对称, (G1') <=> detK > 0; 对称分支 FD 复核余量表 (SUP n=2..4,
  R<=100, detJ 符号恒为 (+1)^n, evK 全正, 最小 |evK| 0.0156..0.0214; INF n=2 R<=100,
  n=3 R<=75, n=4 R<=40, detJ 符号恒为 (-1)^n, evK 全负, 余量指数衰减至 ~1e-5);
  解析谱和 Jacobian 在近简并大 R 区失效 (n=3 R=75 处 rel 误差 1.0, 伪 detJ 符号翻转
  已更正为 FD 值 -1.0125e-5, h 收敛稳定); regularized_green 极点相减消去误差 O(1)
  警示; 修复 scripts/_gapn2_jacobian_analytic.py 符号约定并改用 gtilde_spectral;
  运行笔记 runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_2026-08-12.md.
- 2026-08-12 (会话 58 续作 4b): 新增 [[band-selfconsistency-equivariance]] (带状自洽
  等变性: F(R,x̄)=PF(R,x) 严格恒等式, 对称点反对合 J=-PJP, detJ=(-1)^n detA detB
  交叉块化, 拓扑度同伦唯一性框架 (G1')(G2) 为开放充分条件; R=1 一般 n 的 f_1
  显式分析: 恰 2n 个简单零点 + 符号 (-1)^n, Wronskian W=-2(n+1)pi sin(pi x)<0;
  n=2 闭式 t=(11±2√10)/36; 对称化不等式失败路线登记 118/116 反例, 旧数字
  33/200、57/200 不可复现已更正; 等变 STRICT, 数值为 EVIDENCE).
- 2026-08-12 (会话 58 续作): 新增 [[tension-ratio-chain]] (张力比链: 比值
  上界化到退化极限 rho0 + 一维单峰 G-论证, 闭合缺口 (a') 全 R>1 的 KEY LEMMA;
  STRICT, 9 页零警告, 精确有理证书 C1-C5 ALL PASS, 数值为 EVIDENCE);
  更新 [[symline-n1-monotonicity]] (适用范围不再限于 1 < R <= 3/2, 指向全 R 版本).


- 2026-08-12 (会话 58 续作 3): 更新 [[inf-limit-comparison]] (定理 A 独立复核通过,
  缺口 (c) 解除: T2 符号链 sympy 恒等验证 + T3 区间 + 引理 A'' 175 点零失败 +
  sliver 600 点零失败 + 常数链, 全部 EVIDENCE); 更新 [[phase-ratio-rigidity]]
  (F-210 相位支缺口已闭合, REPAIRABLE-GAP 解除, 40 页零警告).
- 2026-08-12 (会话 58 续作 2): 新增 [[good-root-global-lemma]] (内部临界点 =>
  sign-consistent good root: Wronskian 比值单调 + f 零点唯一性 + FH 跳点公式,
  闭合缺口 (d) 全 R>1 的 INF 全局极值论证; STRICT, 6 页零警告,
  数值交叉检验为 EVIDENCE).
- 2026-08-12 (会话 74): 新增研究工作流方法类 (AI4Math V2 蒸馏, 8 个工具):
  [[workflow-divergent-search]] (发散检索契约: 相关性判断与正确性审计分离, 来源诚实三要素),
  [[workflow-hub-spoke-contract]] (角色契约: orchestrator 只路由, verifier 无记忆独立审稿, 自动 FAIL 清单),
  [[workflow-sorrifier-decomposition]] (失败块 sorry 化 + 子问题递归), [[workflow-statement-freeze]] (两阶段: 陈述冻结防漂移),
  [[workflow-blueprint-dag-ci]] (蓝图 + DAG 状态追踪 + 新鲜上下文收敛检查), [[workflow-first-error-taxonomy]] (首错定位 + SCI 28 类),
  [[workflow-kb-hash-wiki]] (原始源 hash 寻址 + wiki 编译卡片), [[workflow-eve-coevolution]] (可评分变异边际收益演化).
  全部为文献引用级 (来源仓库 2026-08-12 核实可达), 无数值断言; 蒸馏报告见 reports/ai4math_v2_workflow_distillation.md.
- 2026-08-04: 建库, 收录 19 个工具 (会话 1-6 积累).
- 2026-08-13 (会话 98, R-207 第 2 段): 新增 [[half-problem-regularized-green]] -- 半问题约化 Green 闭式. 核心: 无 rho(y) 因子的约化预解核 Gt_k = B - u(x)P(y) (参数变分法 + 三性质唯一性), B/P 闭式与精确 A1/A2 九原函数; 旧稿 rho(y) 因子 bug 与 A1/A2 求积诊断撤回; eps 共轭扇区恒等式与 sector_data Ko 约定更正; n 偶时 K 的两个镜扇区精确半问题闭式 (Kp_odd 与 Ko) 与谱分裂 (Gantmacher-Krein + PD 尾核); 开放核 (I1)/(I2) 及路线 (R→1+ 锚点 / 单调性 / R→∞ 键合-反键合). 运行笔记 run_notes_addendum_2026-08-13d.md; 脚本 scripts/_gapn2_half_problem_probe.py (C0-C3) 与 _gapn2_odd2x2_*.py; EVIDENCE 数值 (C2 闭式 vs Richardson 1e-6 量级, 扇区装配 1e-15/1e-9, R 扫描定号).
- 2026-08-13 (会话 98 续, R-208): [[half-problem-regularized-green]] 追加锚点定理与半隙 Hessian. STRICT 引理 A (W0 在 f0 零点非零, 初等反证 q=-(n+1)^2/n^2) + 定理 B ((R-1)K -> (σ/λ₃⁰)diag(|f₀'(x_j)|), (G1') 对一切 n 于 (1,1+δ) 闭合, n=2 (I1)/(I2) 于 (1,1+δ) 闭合); STRICT 半隙恒等式 ∇²g = -2(R-1)²K = +(2/λ₃)Hess(D_n); 全局凸性路线否证 (EVIDENCE); det 单调递减与链式法则结构 EVIDENCE; 剩余开放核 (M1)-(M3). 运行笔记 run_notes_addendum_2026-08-13e.md; 新脚本 _gapn2_r1_anchor_probe.py / _gapn2_r1_monotonicity_probe.py / _gapn2_gap_convexity_probe.py / _gapn2_r1_det_derivative_probe.py.
- 2026-08-04: 新增 [[moment-jump-completeness]] (会话 9, H^2 解析完备性判据).
- 2026-08-04: 新增 [[left-definite-moment-recurrence]] (会话 10, H^3 与一切 H^s
  完备性判据; 左定矩跳跃机制: 与正交条件同源内积取矩, 边界项吸收, 递推降阶).
- 2026-08-05: 新增 [[left-definite-orthogonal-systems]] (会话 11, 方向 1: H^s 显式完备正交多项式系; 传输算子 K_c^{-r} 闭式; s>=2 根不实现象).
- 2026-08-05: 新增 [[denseness-criteria]] (会话 11, 方向 2: 矩刻画充要条件, 一阶/跳变矩准则, 对角临界指数 3/2, 左定 H^s 一切整数阶完备的正确证明); 修订 [[left-definite-moment-recurrence]] (更正 K_c^{s/2}p_{2m} 三单项式结构对 s>=4 失效, 改为等距传输取矩).
- 2026-08-05: 新增 [[jump-stability]] (会话 11, 方向 3: 增长引理定量形式, 稳定性定理与 omega(log) 门槛, 对角反例尖锐性, Krein 余量) 与 [[third-order-recurrence]] (会话 11, 方向 4: 积分解 beta-分类, mu-闭式, 精确降阶公式 [更正 h3_v56 旧公式], 最小解渐近).
- 2026-08-05: 新增 [[gap-band-extremals]] (会话 13: 带状自洽极值判据, Feynman-Hellmann 对称加倍, R 续延法; 相邻间距极端值数值刻画 R=4 n=1..12, 极限 4pi^2 与 24.9439).
- 2026-08-05: 新增 [[residual-exactness]] (O3a: 残差闭合恒等式 dR1/db = -dR2/da, 由 FH 公式 + Schwarz 定理证明; 残差 Jacobian 结构与临界点斜率分裂; 分支交点唯一性归约).
- 2026-08-05: 新增 [[gap-n1-reduction]] (O1: 两块族归约, Green 算子 L1 连续 + Wronskian 单区间 + bang-bang 七步), [[two-block-gap-bounds]] (O3b: 两块相位间距界, 三区上界 + mpmath 60 位), [[key-lemma-decomposition]] (O2: G2-G1 分解 + 精确角点极限 4pi/(3 sqrt3) + 否证 B-D 的 q-单调性; 交接稿逐项 q-单调闭环作废, 以本条目为准).

| [[gap-n1-reduction]] | 自研 (O1, 2026-08-05) | CANDIDATE_COMPLETE_PROOF (2026-08-06 修复: S_rho 自伴 + 跳点符号 + 平滑论证; 自审 O1a-O1f 全过, 独立复审待办) | 自研 |

- 2026-08-06: key-lemma-decomposition 追加 KEY LEMMA 归约到四引理 (R1/R2/L4box/L5box),
  基座 B1-B5/B7 已证, 审计发现 C1 (LOG 与 FP 形式非等价; 见 run R-20260806T011500Z-keylemma-E58FB1).
- 2026-08-06: 新增 [[fh-hessian-branch-reduction]] 与 [[interval-ad-certificate]] (O3a run R-20260806T011500Z-o3abranch-E8E56F): FH 公式必须带特征值因子; 好根处分支斜率 Hessian 归约; 全局负定性被否证; 区间 AD 证书把 Lemma A 反例 CE-1 严格化 (h'(a*) < 0 at R = 1500/1e4). 同步修订 [[residual-exactness]] 的局限注记 (Lemma A 已证伪).
- 2026-08-06: key-lemma-decomposition 更新为已关闭 (run R-20260806T070000Z-keylemma2b-0A6D8F):
  KEY LEMMA ((LOG)+(FP)) 完成证明, 状态 CANDIDATE_COMPLETE_PROOF. 路线: (q,u) 换元 +
  M2 (dIN/du<0, 证书 + 初等尾部) + CORNER (c=1/2 闭式) + C4 (c=0.4 曲线, 区间证书 +
  T^3 K 精确有理数下界) + L4box/L5box 区间证书 (双引擎独立复验). 审计发现并修复:
  shipped verifier 的 C4 过期区域常数; dM2/dq 证书未覆盖 strip [1,20]x[y1,sqrt(41)]
  (新增 strip 证书); riarith.iv_sqrt 非严格向外舍入 (不承重, 独立引擎全覆盖).
- 2026-08-06: key-lemma-decomposition 状态升级为 INDEPENDENTLY_AUDITED_PROOF (run R-20260806T140000Z-keylemmaaudit-2F83B1, Hypatia): 第二独立实体从零重导全部符号/解析/证书层, 五份证书用独立 80 位定向 Decimal 区间引擎全部复验, IN = A*K(v) 的 caveat 解除 (atan(tan v) = v 后 diff = 0), riarith.iv_sqrt 非严格性确认不承重. 程序级 O2 义务 CLOSED. 经验: 独立审计的价值在于 (i) 不信任自审而逐项重导; (ii) 自建第二引擎避免同源错误; (iii) 符号恒等式必须显式消元验证 (atan(tan v) 简化).

- 2026-08-06: [[gap-n1-reduction]] 修复并自审 (run R-20260806T140000Z-o1revise-2ED02A): 状态 REPAIRABLE_GAP -> CANDIDATE_COMPLETE_PROOF. 修复 R1 (S_rho = M_sqrt(rho) T_0 M_sqrt(rho) 对称核, 自伴 HS, Weyl 可用), R2/R4 (跳点 FH 经平滑逼近, 符号 dD/de = -(c_+ - c_-) f(x_j), 双侧导数处处存在), R3 (u_2 符号约定). 自审发现并修复 F-001 (HS 常数推导一行算术错, 最终界不变); 数值组全部通过且两脚本复跑逐位一致; 独立复审 Lemma 1/3 为关闭义务 O1 的前置步骤.
- 2026-08-06: 新增 [[reflection-branch-reduction]] (run R-20260806T140000Z-o3ac1-42F931, Beauvoir): 残差反射 R1/R2, h 反射公式 R3, 积分恒等式 R4, 好根=零点 R5, C1 归约 R6; C1 归约到 (E1) 端点符号 + (M) M-形; 关键陷阱: secular 根扫描上限 2pi+1e-3 漏重垒高特征值 (R-103), MVT 充分条件 g1'>1 被否证 (CE-3).
- 2026-08-07: 新增 [[lemma-A-doubleprime]] (INF 极限 run R-20260806T200000Z-inflimit-5B2C7D):
  G(R,u) >= Dbar(u) 对 w=u*sqrt(R)>=2, 相位坐标 + def1 下界 + def2 上界 + 比值 0.8256;
  注意 v = u/ell = -t cot t (不是 -cot t; f 关于 v 递减故旧证书仍有效, 但公式已更正),
  三常数 C_z<0.337, f<=9, 比值 0.8256 由脚本 18-19 区间认证.
- 2026-08-07: 新增 [[delta-bracketing]] (会话 30): 对称阱族相位 delta_1, delta_2, z_2, psi_2 的
  初等双端括号 (g'>0, h'>0 符号证明), 引理 A'' 与 T1 上界的必备工具.
- 2026-08-07: 新增 [[cot-series-certificate]] (会话 30): R(z)=1/z-cot z 余项在 (0,pi/8] 的
  线性上界, C_z = 0.33681139899.. < 0.337 (区间认证), 亦用于 tan 余项.
- 2026-08-07: 新增 [[inf-limit-comparison]] (会话 30): INF R->inf 极限的 T1/T2/T3 框架,
  证明 lim_R R*m_R = Dbar(u*) = 24.9438661384324769 < 3*pi^2 (定理 A, 完整证明见
  docs/SL_gap_n1_inf_limit_proof.pdf); 严格证明/计算机认证/数值证据分节标注的规范写入文档.
- 2026-08-09: 更新 [[r1plus-perturbation-sheet]] (会话 34, run R-20260807T163000Z-c1center-9C4E2A):
  手算原函数得 phi(b) 闭式与 phi'(b) 因式分解 (DERIVATION); phi' > 0 于 [a0,1)
  CERTIFIED (mpmath.iv 200 位, 4000 胞, 最坏下界 8.896e-6) + STRICT (初等尾部
  C_tail >= 9.651926); b_top* >= 7/10 > b0 STRICT (隐函数定理结构引理);
  E1/U'/P0 归约到 Gap 1 (显式 O(eps) 界 + b_top(eps) <= 1 - delta_0);
  记录 F-019 (w_k^1 除号误用乘号, 已修). 数值与严格标注分离: 数值交叉检验
  仅作 EVIDENCE, 不构成证明.

- 2026-08-09: 新增 [[phase-ratio-rigidity]] (O3a 完整证明, 会话 34): 传输能量守恒把
  $R_1=R_2=0$ 化为严格单调相位比 $r_\tau$ 的等值, 强制 $a+b=1$; 对称线单变量化 +
  KEY LEMMA ($\widetilde F_e^\prime(c)<0$ 于紧盒) 完成 single crossing. 审计脚本
  scripts/audit_o3a_pdf_part1..4.py 全部通过; 主定理见 docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf.
- 2026-08-09 (会话 36): KEY LEMMA 去证书化第一步 -- $\partial_qM_2<0$ 于 $D$ 的
  84+10 叶盒证书被完全解析证明取代 (引理 5.2--5.4): $q=1$ 基线 $M_2(1,w)=\pi h(w)<0$;
  $\partial_q^2M_2<0$ 两段初等界; $g(w)=\partial_qM_2(1,w)<0$ 凹性+切线链
  (界 $-1054523/114800$); 边界曲线 $w=\sqrt{2q+1}$ 的 $\theta$-参数化闭式
  ($M_2<0$ 由 $2-(\pi/2-\theta)\sin2\theta\ge2-\pi/2$; $\partial_qM_2<0$ 由 $N(z)$
  对 $\beta$ 凸性端点极大 + 有理上界 $R(z)\le-4.4344$, $T(z)\le-27.3646$);
  尾部 $q\ge20$ 解析. 证书仅剩三处紧不等式 (C4 区间段 200 叶盒, $(G_2-G_1)'<0$
  与 $\widetilde F_e''>0$ 各 128 叶盒), 文档五类改三类. 验证脚本
  scripts/verify_o3a_M2_analytic.py (全部有理界复核). 诚实标注: 剩余证书重放内核
  位于 Blueprint 项目 runs/R-20260808T143337Z-o3a-c1/, 非 kernel-checked.
- 2026-08-09 (会话 37): KEY LEMMA 去证书化第二步 -- C4 区间段 $K>0$ 的 200 叶盒
  证书与尾段处理被纯初等解析证明取代: $K=q^2L$, $q\ge1$; $L'=N/(10T^2)$,
  分子 $N$ 在 $[2\pi/7,3\pi/10]$ 有精确有理下界
  $88146367488708279/400000000000000>0$, 在 $[3\pi/10,2\pi/5)$ 为非负项之和
  ($20T^4>0$), 故 $L$ 严格递增, $K\ge L\ge L(2\pi/7)>0$. 常数由 Machin 级数、
  $\sqrt5$ 有理界与 $P(t)=t^6-21t^4+35t^2-7$ 精确核验. 证书仅剩两处紧盒
  ($(G_2-G_1)'<0$, $\widetilde F_e''>0$, 各 128 叶盒). 验证脚本
  scripts/verify_o3a_c4_analytic.py (PART A 精确 15 项全 PASS; PART B 数值
  交叉检验仅作 E3 证据). 文档按 E1 严格解析 / E2 有限证书 / E3 数值扫描三类
  证据显式标注 (O3a tex remark 1.2 与摘要).

- 2026-08-09 (会话 38): O3a KEY LEMMA 去证书化第三步 -- I3 (F̃e''>0 于 Q=[1,2]x[0.4,0.5])
  的三维盒证书 (128 叶盒, 隐式相位根夹取) 被二维相位参数化证书取代:
  沿真实曲线显式反解 c=c1(x,q)=atan(1/(q tan x))/x 与 c=c2(γ,q)=atan(q tan γ)/(π−γ),
  把 F̃e'' = M1J1 − M2J2 化为两个二维显式函数 J1_2d>0 (16 叶盒, 下界 +0.420803280435)
  与 J2_2d<0 (67 叶盒, 上界 −0.062083223779). 盒端点 E1 证明:
  α1(2,1/2)=arccos(2/3), α1(1,2/5)=5π/14, γ(1,1/2)=π/3 (闭式), γ(2,2/5)>0.655
  (有理三角级数界链). 重要更正: 交接摘要盒下界 0.8411/0.6557 均大于真实端点
  (arccos(2/3)=0.8410687, γ(2,2/5)=0.6556493), 原盒漏条, 修正为 0.841/0.655 后重算.
  验证: scripts/verify_o3a_i3_2d.py 独立重放 (叶盒 JSON + 80 位点交叉 415 点 0 失败 +
  叶面积覆盖审计). 文档 docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf 升级为 20 页零警告,
  概述文档同步 17 页零警告. 数值部分与严格证明按 E1/E2/E3 显式标注.

- 2026-08-09 (会话 39): O3a I3 去证书化路线 (真曲线区域分解). 新工具
  [[true-curve-region-decomposition]]: 把证书目标从完整二维盒收缩到真曲线区域
  T1/T2 (c1,c2 in [0.4,0.5]), 裕量大幅放大 (J1 约 [9.0,18.6], J2 约 [-17.7,-6.0]).
  E1 恒等式: G=u(H-A); dG/dx|_q = c1'(x,q)*J1_2d (故 G 的 x 单调性等价于
  J1_2d>0, 解析化只需 q 方向); J1_2d = G^2 + Gc - (x*Phi/D)*Gx.
  E1 单变量闭式 (q=1): J1_2d(x,1) = (2x/pi)^2*N(x) > 0 于 [pi/3,5pi/14];
  J2_2d(gamma,1) = x^2*N(x)/pi^2 < 0 于 [2pi/3,5pi/7], N = 12+16x cot x+2x^2 cot^2 x - 2x^2
  (x = pi - gamma). 角点值: G(pi/3,1) = -2-4pi sqrt3/27 < -2.8; Gc(pi/3,1) > 1.87;
  Gx(x,1) <= 100pi/147 < 2.14; x*Phi/D <= 561/450.
  剩余开放: 单调性引理 (M1) dG/dq<0, (M2) dGc/dq>0, (M3) dGx/dq<0 于 T1;
  (M1')--(M3') 于 T2 + 一维边界估计. 符号已 E3 交叉 (dG/dq in [-1.66,-1.12] 等),
  E1 证明未完成; 当前仍由 E2 叶盒证书覆盖. 导数分子结构: (x,theta) 曲线坐标下为
  六正变量整系数多项式/恒正分母, 无超越区间运算. 文档新增子节
  "证据分层与真曲线区域上的解析化路线" (24 页零警告, E1/E2/E3 逐条标注;
  修复 end-document 位置使结论/符号速查重新入编).

- 2026-08-09 (会话 40): O3a I3 去证书化第四步 -- J1_2d 侧完全解析化 (定理 5.8,
  docs/SL_gap_n1_O3a_phase_rigidity_proof.tex, 25 页零警告): 七步初等链给出
  J1_2d >= G^2 + Gc - uGx >= 4 + 187/100 - ((89/100)^2*8 - 4/3) = 6499/7500
  > 1733/2000 > 0 于 T1 闭包. 步骤: (i) Phi/D >= 2/3; (ii) u >= 2x/3, u_x >= 2/3;
  (iii) G < -2 故 G^2 >= 4; (iv) Gc = t1 + t2 >= 187/100 (t2 >= 0, t1 两段下界:
  x <= pi/3 用 4/3 + 8pi/(27 sqrt3) > 187/100, x >= pi/3 沿曲线 t1(x,q) >= t1(x,1)
  = (2x/pi)^2*W = f(x) 递增); (v) C = 3/x^2 + 2 csc^2 x <= 8; (vi) u <= 89/100
  (sin 2theta >= sin(4x/5) 给出 u <= u_c, u_c <= 89/100 由 F'' >= 3/2 交错级数
  有理包络; 更正: 旧 F'' >= 1.7 有理界方向有误); (vii) 组合
  uGx <= u^2*C - 3uu_x/x. 关键更正: (a) 旧链 J1 >= 4 + 187/100 - 89/12 算术错误
  (结果为负), 正确为 4 + 187/100 - ((89/100)^2*8 - 4/3) = 6499/7500;
  (b) 删除错误恒等式 dG/dx|_q = c1'(x,q)*J1_2d (eq:gcurv), 正确分解为 eq:jdec
  (Gc/Gx 为固定 (q,c) 偏导数). 证书表仅剩 J2_2d<0 (67 叶盒, 上界 -0.062083223779)
  与 (G2-G1)'<0 (128 叶盒). 验证: scripts/verify_o3a_i3_t1_e1.py
  (SHA-256 64e24ace3117772b6cd2ea2ac53986a75cad6c3fd797b61369472ac87ec6ab04,
  5 部分全 PASS). [[true-curve-region-decomposition]] 与
  [[phase-param-2d-certificate]] 状态更新; J1 16 叶盒证书保留为历史产物.
- 2026-08-09 (会话 42): O3a I3 去证书化第五步 -- J2_2d 侧完全解析化
  (定理 5.14, docs/SL_gap_n1_O3a_phase_rigidity_proof.tex, 30 页零警告):
  废弃 (M1')--(M3') 单调性路线, 改用 W-分解链: 沿真实曲线
  J2_2d = N/(16 Delta^4), N = 32 A^2 cg W, W = W1+...+W8 (整系数括号因子
  B1..G5, 符号计算精确验证); 轨迹几何 + 括号符号/单调性 + 26 端点有理界 +
  分段组合 mu = T_A+T_B+T_C-T_D >= 139/100 (角点精确 27921/20000).
  单变量事实由新自研十进制定向舍入区间引擎认证 (misc/rigid_dec.py,
  55 项全过, misc/e1_facts_ledger.json; 哈希 L7/L8/L9), 67 叶盒证书
  与 L4 哈希已从清单移除, J2 侧不再依赖任何证书. 新增
  [[interval-dec-directed-rounding]]; [[true-curve-region-decomposition]]
  与 [[phase-param-2d-certificate]] 状态更新.

- 2026-08-09 (会话 43): key-lemma-decomposition 更新 -- 伴随命题 (LOG)
  (d/dc log(M~f1/M~f2) = G1 - G2 < 0) 完全解析化 (定理 thm:LOG + 引理 lem:G2m2,
  docs/SL_gap_n1_O3a_phase_rigidity_proof.tex 32 页零警告): 恒等式
  G2 = -Phi W0/D - 2P + 三估计 (Phi/D <= 65/66; W0 < 0.582; P < 0.576)
  => G2 > -1.725 > -2; 配合 thm:j1e1(iii) 的 G1 < -2 与 lem:G1 覆盖全部参数.
  旧 128 叶盒证书 (H' < 0 路线) 退役. O3a 文档四族证书全部解析化移除, 全文
  零证书: 证据分层更新为 E1 (严格解析) + E2 (单变量事实验证器) + E3 (数值
  扫描, 仅交叉检验). 验证: scripts/verify_o3a_LOG_analytic.py 全 PASS
  (盒上四界 + 全域 min H = G2 - G1 ≈ 2.472).

- 2026-08-09 (会话 44): O3a I3 去证书化收尾 -- J2_2d < 0 的 55 项单变量事实完全 E1 解析化
  (docs/SL_gap_n1_O3a_phase_rigidity_proof.tex, 38 页零警告): 新证书链把最后一处 E2 依赖
  (lem:brackets / lem:track(iv) / eq:endpoints 的 55 项事实, 原由 rigid_dec.py 认证) 全部
  换成纯解析 E1 证明. 新工具 [[rational-envelope-certificates]]: 交错级数包络 (sin/cos/
  arctan 部分和交替夹逼 + Machin pi) + 精确 Fraction 区间算术 + 二阶泰勒模型, 输出
  misc/e1_certgen.py (L10) -> misc/e1_cert_ledger.json (L11, 57/57 PASS) ->
  misc/e1_cert_tables.py (L12) -> 附录 A 五张证书表. 修复 misc/rigid1d.py 的 I.sqrt
  宽度恒 1.0 bug. 文档证据分层只剩 E1 (严格解析) + E3 (数值扫描, 仅交叉检验); 旧十进制
  区间引擎 (L7-L9) 与二维叶盒全部退役为历史记录. [[interval-dec-directed-rounding]]
  状态改为已退役历史. 编译产物 docs/build/SL_gap_n1_O3a_phase_rigidity_proof.pdf.

- 2026-08-10 (会话 47-48): rational-envelope-certificates 追加独立第三方重放引擎
  (misc/audit_o3a_cert_replay.py, Decimal 80 位定向舍入 vs exact Fraction, 71/71
  PASS); O3a 文档修复 F-210 (相位支选择, 新引理 lem:phasebranch, 纯 E1) 与 F-211
  (thm:j1e1 step (iv) 尾部区间, 精确有理包络), 40 页零警告; 双代理对抗审计通过.
  证书数据未动 (e1_certgen/ledger 哈希不变).

- 2026-08-10 (会话 49): rational-envelope-certificates 内文 F-209 残留表述修正
  ("arctan 22 项在 x <= 3/2 时余项 < 1e-12" 为修复前残留, 已按修正后的 lem:envseries
  更新: 直接级数仅用于 v <= 1, 余项 <= v^45/45; 最差宽度 tau(131/200) ~ 1.8e-10);
  O3a 完成度审计 8 脚本复跑全 PASS (part2b/part2c 网格与 mpmath 精度修正, 纯 E3).


- 2026-08-10 (会话 50): 新增 [[switch-saturation-k-invariant]] -- 开关饱和与块能量
  不变量. 来源: 用户提供两份 n>=2 相邻间距极值证明包 (SL_gap_nge2_finite_reduction_
  proof_zh.pdf, SL_gap_nge2_exact_2n_switches_proof_zh.pdf), 项目忠实转录为
  docs/SL_gap_nge2_finite_reduction_proof.pdf (15 页) 与
  docs/SL_gap_nge2_exact_2n_switches_proof.pdf (16 页), 均零警告. 工具内容:
  FH 完全盒饱和 (最大化/最小化两种指派), Wronskian 严格符号 -> 商严格递减 ->
  精确零点公式 -> 零点=开关双向相等, 块能量接口跳量 = (r+ - r-)F, K = -2D 因子 2,
  端点斜率比 q0>1, q1<-1 收紧为恰 2n 开关. 审计: 解析逐条 PASS; 数值
  scripts/audit_nge2_pdfs.py Part A 40/40 + Part B 16/16, scripts/_hp_nge2.py
  (mpmath 50 位), scripts/_smooth_nge2.py (光滑权 4/4). 文献: 未检索到直接等价
  已发表定理; Willner-Mahar 1979 为明确既有工作风险; 不声称首创.
- 2026-08-10: 新增 [[well-family-rigidity]] (阱族小 R 相位刚性, 会话续作): 定理已证 1<R<=3/2 时阱族任意 sign-consistent good root 必为对称根 a+b=1; 证明链 = 相位范围 + 传输能量守恒 (P(psi) 旋转) + 残差消元 + r~_tau 严格单调 (Psi~'<0 于 (0,pi) 的完全初等证明: 因式分解 W^2 sin^2 x Psi~' = -(q+1)(2N0+qN1)/8, H=4N0+N1>0 引理, tan(u/2) 有理化 N(t)>0 引理); 文档 docs/SL_gap_n1_well_rigidity_R32.pdf (11 页零警告); 缺口 (a) 对称线 1D 分析, (b) R>3/2 阱族刚性, (c) 定理 A 独立复核 均开放/CANDIDATE, 全部 EVIDENCE 登记于 misc/_well_explore_log.md.
- 2026-08-10: 新增 [[symline-n1-monotonicity]] (会话 52, 缺口 (a) 闭合): 阱族对称线上 f(v) 唯一零点与 D(v) 单峰; KEY LEMMA (F~_e 在 (0,inf) 唯一零点 c* in (0,1/2)) 由 G1/G2 分解 + P1/P2 大余量初等界 + W0 引理 (精确有理证书) 闭合; 精确降维恒等式 S_R = -8q~^2(c+q~)^3 F~_e 与 D_c = -8(c+q~)q~(1-q~^2) F~_e (FH + 链式法则); 端点 D(0+)=3pi^2, D(1/2-)=3pi^2/R; 推论: INF 侧 1<R<=3/2 闭合, I(R)=D(v*(R))<3pi^2/R; 文档 docs/SL_gap_n1_symline_proof.pdf (10 页零警告) + summary (4 页); 失败路线 (F~_e' 符号误判, G2 自由区域为负, W0 可负需分情形) 与缺陷脚本 (sym_endpoint.py 因子 t, master_verify.py mode-2 范数) 如实登记.
- 2026-08-10 (会话 56): 更新 [[well-family-rigidity]] 为全 R 版本 (缺口 (b) 闭合, 一切 R>1): 主定理改为 "一切 R>1 时阱族任意 sign-consistent good root 满足 a+b=1", 新五步链 (tau<2 经 alpha-凸性 D=alpha(2x)-2alpha(x)>0; 残差消元 r_tau(A)=r_tau(B) + Sigma2/Sigma1=tau^2 r_tau; r_tau 精确结构: 因子分解/L0/中间区递减/危险区引理/B' 反射分离 x+y>pi; L3 凸包/跨区/P-和通道排除; A=B => a+b=1), 全部 STRICT 初等; 文档 docs/SL_gap_n1_well_rigidity_allR_proof.pdf (14 页零警告) + 总结 docs/SL_gap_n1_well_rigidity_allR_summary.pdf (8 页零警告); 小 R 机制 (Psi~'<0 单调) 保留为特例备查; 交接错误更正与 EVIDENCE 登记于总结第 3/5 节与 misc/_well_explore_log.md 第 16 节; 剩余缺口 (a') R>3/2 对称线 1D, (c) 定理 A, (d) 全局 good-root, 不宣称 INF R>3/2 闭合.
- 2026-08-11 (会话 67): 更正 [[jump-stability]] 源文档定理假设 (F-001):
  `docs/SL_stability_moment_jump.tex` 定理 2.1/2.2 陈述由 `A_m >= B_m` 统一更正为
  `B_m >= 0` 且 `A_m - B_m >= c_0` (与证明实际使用及 Lean 形式化 `SL/StabilityGrowth.lean`
  一致); 新增「假设的强度」注 (弱假设反例: `A_m=B_m=1` 振荡, `A_m-B_m=1/2<c_0` 时
  乘积下界失败) 与审计节 F-001 更正条目; 文档重编译 7 页零警告; lean-proof 状态
  记录同步 (F-001 RESOLVED), `lake build` 复跑通过. 无新数值断言 (纯陈述修正).
- 2026-08-14 (会话 105): 新增 [[largeR-level-cascade]] (大 R 层级级联平衡, P0
  会话, run R-20260812T090000Z-g1prime-g2 R-210/R-211 + 审计 R-212): STRICT
  层级结构 (a0*K0=2; a1=-2K1/K0^2; 归约种子仿射线性; 硬常数 E5_5=K0^3/2+
  线性(K1,C1) 强制奇分量; 分族平移层) 经独立对抗审计 A1-A8 判定
  INDEPENDENTLY_AUDITED_PROOF (F-NL3: level-3 4x4 矩阵奇异, 机制更正);
  决定性负结果 EVIDENCE: 纯整数幂分支至 u^7 无 K0~3.46 零点 (20 组多起点
  全部收敛退化 K0->0), 修正分支种子根开放; 撤回截断幂字典 eq_coeff 丢项
  bug (R-211). M3 总体 RIGOROUS_PARTIAL_RESULT.
- 2026-08-14 (会话 106): 新增 [[constrained-denseness-runs]] (边界约束子空间
  多项式稠密性, run R-20260814T070000Z-densbc-3F8A2C): 定理 A-H STRICT
  (主判据/约束矩刻画/约束恢复稠密性修正版/对角完整分类 (β<=3/2 且无有限
  游程)/一阶矩与跳变判据/边界泛函解释); 两个包猜想被否证 (V=span{x^2,x^3}^⊥
  非全 β 稠密 - 自由参数转移到 M_4/M_5; 判据 "β<=3/2 或杀 M_2=M_3" 为假 -
  R={4} 有限单例游程); 协调者审计 (子代理机制不可用, 独立性限制如实记录),
  F-densbc-01 更正 Lemma 4.1 奇次比值公式为 M_k=(floor(k/2)/floor(L/2))·M_L;
  开放核 O1-O3 (一般非对角精确判据/L_j 展开杀自由参数/分数窗).
- 2026-08-22: 更新 [[third-order-recurrence]] (A6 root-1 高阶有理积分解排除,
  插件性能实验): root-1 分支偶/奇+c>0 的有理乘积比值既约次数<=2; 独立审计
  REPAIRABLE_GAP (0 fatal, 2 小缺口) 已修复; root-0/最小解分支仍开放.
  Artifacts: runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/candidate_proof.md,
  audit runs/plugin-perf-eval/R-20260822T000000Z-a6-audit/audit_report.md.
