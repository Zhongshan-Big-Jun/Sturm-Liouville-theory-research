# 按数学问题阅读

[中文首页](../README.md) | [English](../README_EN.md) | [问题地图](../research_map.md) | [项目理解](PROJECT_UNDERSTANDING.md) | [续接](../state/RESUME.md)

本页选择证明和前置材料; 稳定编号与当前范围集中在研究地图. 推荐依据是陈述, 依赖和对应审查版本, 不由文件名或轮次大小决定. 本次只整理导航, 没有重新审计证明. 工具库/Blueprint 接收及 Lean 状态由各自记录承载. 所有源文件与阅读版的关系见 [仓库说明](repository-guide.md#源文件与-pdf-对应).

## 左定空间与正交系

统一模型先固定 $c>0$, 复空间 $\mathcal H_c^s=D(K_c^{s/2})$, $K_c=-d^2/dx^2+c$ 及其 Krein 边界条件. 原族成员窗口, 任意保留集和替代基是三个不同对象.

### 空间与算子域

先读 [真实谱域与成员窗口](SL_fractional_left_definite.tex), 再用 [分数/临界域字典](../tools/krein-fractional-trace-dictionary.md) 和 [奇偶幺正桥](../tools/krein-parity-unitary.md) 定位 A7/A9. [算子域障碍](../tools/krein-power-domain-polynomial-obstruction.md) 及 [pilot-v6 证据](../runs/three-arm-pilot-v2/pilot-v6-hs-domain/RESULTS.md) 解释代数传输多项式为什么不能直接当作高阶真实域中的基. [退化极限](SL_krein_c0_limit.tex) 分开处理普通函数代表与商类, 不给固定 c 结果的一致 $c\downarrow0$ 推广.

### 原族完备性

A1 的当前推荐是 [全成员窗口证明](SL_fractional_left_definite.tex): 原完整命名族在 $0\le s<7/2$ 稠密; 非仿射单个成员在 $s\ge7/2$ 出域, 仿射成员与可抵消边界残差的组合分别处理. [R6 报告](../reports/proof-audit-round6-20260921/REPORT.md) 记录四迹图核心补证及独立审查.

[H2 证明](SL_h2_completeness_proof.tex) 和 [H3 证明](SL_h3_completeness_proof.tex) 保留低阶矩路线与推导. [Hs 正交系旧稿](SL_hs_orthogonal_systems_proof.tex) 须配合 A7 域障碍阅读, 不能由形式传输推断原族成为全阶真实域的基. [投影/有限矩修复](SL_projection_moment_repairs.tex) 替代旧稀疏投影和 F/G/H 的过强推论; 原全多项式投影与对角分类保留原范围.

### 删项闭包

| 问题 | 推荐证明与前置 | 当前范围与历史关系 |
| --- | --- | --- |
| 余有限 A8/A12 | [A12 全阶证明](SL_cofinite_all_orders.tex), [已有 PDF](SL_cofinite_all_orders.pdf); 前置 A1 与连续中心迹 | 固定 c, $0\le s<7/2$. 保留的关键列按区间为 {}, {0}, {0,1}, {0,1,4}; 三个临界等号取较少迹侧. [R11 审查](../reports/proof-audit-round11-20260926/REPORT.md). 原族非 Schauder/Riesz 结论不涉及替代系 |
| 任意保留集 A11 | [完整全窗口证明](SL_full_window_deletions_and_finite_constraints.md) 第 1--6 节; 必要前置 A1, A12, 真实平方域边界提升和全纯唯一性桥 | 同一 c/s 窗口. 两奇偶倒数和均发散时闭包是遗漏的连续中心迹核交; 任一收敛则无限余维; 稠密 iff 两和发散且关键列保留. [R15 最终审查](../reports/proof-audit-round15-20261005/REPORT.md) |
| s=2 的原始完整删项补证 | [Hc2 任意删项证明](SL_H2_arbitrary_deletion_proof.md), [R14](../reports/proof-audit-round14-20261004/REPORT.md) | 保留为 s=2 的独立推导, R15 通过新范数/全纯桥推广到整个成员窗口; 不能仅把 Hc2 闭包传到更强范数 |

收敛侧全部闭包元素的描述仍开放. [s=2 余有限旧证明](SL_cofinite_left_definite.tex) 和 [s=3 三迹证明](../literature/absorption-20260923/domains/proofs/03-s3-cofinite-closure.md) 可用于理解低阶机制; A12 覆盖其同模型余有限范围, A11 扩展保留集量词. 第五轮已反证旧 O1'LD 尾部刚性/无条件余有限稠密候选, 原失败和 [R5 报告](../reports/proof-audit-round5-20260921/REPORT.md) 保留.

### 有限约束

A3-KREIN-FINITE 当前读 [全窗口证明第 7 节](SL_full_window_deletions_and_finite_constraints.md#7-任意有限个连续约束下的逐项筛选分类), 前置 A11 的发散闭包与收敛侧无限余维. 固定 c 和同一窗口, 对有限连续复线性约束共同核 V 逐个筛选 $p_n\in V$: 稠密 iff V 是当前连续中心迹的部分坐标核交, 分别有 1/2/4/8 个不同子空间. 这不处理先投影, 先重组或无限约束.

一般非对角 H 的 A3/A4 仍分开读取 [修后投影准则](SL_projection_moment_repairs.tex), [已有受约束稿](SL_denseness_criteria.tex), [结构化子类报告](../reports/plugin-performance-o1p-ab.md) 与 [工具卡](../tools/constrained-denseness-runs.md); 本 Krein 子类的完成不关闭一般问题.

### 替代系

A10 当前推荐 [全部整数阶 Hermite-Legendre 证明](SL_integer_left_definite_riesz_systems.md), [R16 最终解析审查](../reports/proof-audit-round16-20261006/REPORT.md). 每个固定 c>0 和整数 r>=1 有 $2\lceil r/2\rceil$ 个低提升及积分 Legendre 高列; r=0 用标准 L2 Legendre 系. 图范数等价, 次数一致 Riesz 界和精确多项式张成由该稿直接证明. 速率式另要求 t>=0, N>=2r-1 及加权系数条件.

[原 s=2/4 卡及版本入口](../tools/krein-integrated-legendre-riesz.md) 和 [文献吸收来源](../literature/absorption-20260923/README.md) 解释构造起点. 当前一般整数证明扩展的是替代系, 保留原稀疏族的非基结论. 非整数阶, c趋零及阶数趋无穷的一致界另计.

### 一般开放问题

除上述精确合同外, 收敛删项侧全部元素, 一般 A3/A4, 无限约束和无附加条件的速率均未关闭. [矩跳跃稳定性](SL_stability_moment_jump.tex) 的一般递推只有乘积下界, B=0 子类另有精确分类, 无条件有界基扰动稳健性已否定. [指定双奇偶三阶递推](SL_third_order_recurrence_theory.tex) 与 [K(1)=e/4 锚点](SL_third_order_K1_proof.tex) 保留已证系数族范围; 非齐次源项和更一般系数族仍开放.

## 特征值比值与谱隙

模型为 $-y''=\lambda\rho y$, Dirichlet 边界. 早期比值文稿中的分段连续类和后续谱隙的可测盒类按原陈述使用. 特征值 lambda 与频率 omega=sqrt(lambda) 明确区分.

### 全序列谱比

B1/B2 读 [上确界证明](SL_ratio_proof.tex), [Mahar-Willner 引理重证](SL_mw_lemma_reproof.tex) 与 [下确界证明](SL_inf_ratio_proof.tex). 上确界用平衡相位闭式; 下确界 1 不达到, 全序列下确界用常密度高模态足够. 首对全局变分证明与候选矩阵计算分别承担作用.

### 固定指标候选与全局问题

B3 当前读 [候选谱证明](SL_fixed_n_supremum.tex), 前置转移矩阵/世俗方程, [一般交替 Chebyshev 表示](../reports/plugin-performance-b3-o1o2-current.md) 和 [R9 解析修订](../reports/proof-audit-round9-20260923/REPORT.md). 物理世俗函数反射带频率因子, 归一化后才严格对称. 已证全部 2n 简单根及固定 R>1 的平衡候选 $c_n$ 严格递减至 $((\pi-\phi)/\phi)^2$, $\phi=\arccos((\sqrt R-1)/(\sqrt R+1))$. 与真实固定指标上确界相等的 O1/O2 仍开放; [历史对比](../reports/plugin-performance-b3-ab.md) 不替代该缺口.

### n=1 谱隙

归一化盒类 $1\le\rho\le R$ 内全部 R>1 的 SUP/INF 证明链已有闭合记录, B4 整体仍因 n>=2 问题而 PARTIAL. 按 [主证明](SL_gap_n1_proof.tex) 的归约, [O3a 相位刚性](SL_gap_n1_O3a_phase_rigidity_proof.tex), [阱族全 R 刚性](SL_gap_n1_well_rigidity_allR_proof.tex), [对称线](SL_gap_n1_symline_allR_proof.tex) 和 [全局 good-root](SL_gap_n1_global_goodroot_proof.tex) 阅读; [R2](../reports/proof-audit-round2-20260920/REPORT.md) 与 [R13](../reports/proof-audit-round13-20260927/REPORT.md) 给出后续修补/证书范围. 单篇早期待办不重开整条路线, 也不把旧证书自动用到新版本.

B4-INF-LIMIT 另读 [连续 INF 极限证明](SL_gap_n1_inf_limit_proof.tex), [R8](../reports/proof-audit-round8-20260922/REPORT.md): 对称 [R,1,R] 阱族 $Rm_R\to M\approx24.9438661384$, 非负 O(1/R) 误差; 近极小化子需 $R\eta_R\to0$. 连续相位覆盖薄层域, 初等比较处理大 w; T1 的解析收敛与 T3 的数值定位分开. 精确最优系数和参数收敛率未在该稿证明, 旧 05/16/19 证书由新论证替代相应职责.

### n>=2 局部及全局问题

先读 [有限块约化](SL_gap_nge2_finite_reduction_proof.tex), [精确 2n 开关](SL_gap_nge2_exact_2n_switches_proof.tex), 再读 [局部对称性与全局框架](SL_gap_nge2_symmetry_local_proof.tex). [R7](../reports/proof-audit-round7-20260921/REPORT.md) 修复弱反差局部唯一性, 并给每个固定 n>=1 的 SUP 极限 $(n+1)^2\pi^2$; 有限 R 的全局最优值/唯一性分别开放.

**G2 当前推荐**是 [全部零点紧性完整证明](SL_G2_compactness_proof.md) 与 [R14 最终解析审查](../reports/proof-audit-round14-20261004/REPORT.md). 固定 n>=2, 两图案, 全部精确 F=0, 每个有限 Rmax>1 的 $1\le R\le Rmax$ 上有统一正块宽, 包括 R趋1. F=0 先给 K=-2D 和自动符号相容, 再排除接口碰撞. 这补齐此前仅限符号相容/R0>1 的桥; 第十三轮“连接尚未完成”的登记属于历史. G2 加全部零点 ND 才给条件化续接/唯一分支, ND/G1 和无条件全局唯一性仍开放.

[最小方向合作者进展](SL_gap_nge2_min_direction_progress.tex), [独立审计](../runs/rigorous-open-math-research/R-20260816T174722Z-min-direction-audit/) 及 [核验包](../collaborator_min_direction_verification/) 按原 n, mu 和弱反差条件阅读, 不扩大为全部参数结论.

### 相关计算工具

B7 的 [有限移动界面二阶公式](../tools/finite-interface-second-derivative.md) 限固定正块值, 非碰撞内部界面与简单固定模态, 保留几何加速度. B8/B9/B10 的谱指标, 一般 Jacobian, DD/DN 去极点核与 raw K/SKS 语义见 [脚本导航](../scripts/README.md); 当前数值诊断不认证全参数符号.

B11 读 [有界真实方向谱尾证明](SL_bounded_direction_spectral_tail.md), 前置真实 DD 完整模态与归一化二阶变分, 审查见 [R16](../reports/proof-audit-round16-20261006/REPORT.md). 对正有界 rho 和实 L-infinity h, Parseval 剩余给精确 Q-Q_N 两侧界. 符号认证另需有限配对/J/特征值/Q_N 的可靠包络; 当前浮点输出是数值评估/误差估计, 不是这种包络. 此结果不覆盖界面 delta/delta-prime 方向, 也不关闭 ND/G1.

### 局部 chart 与外部结果

| 结果 | 证据入口 | 保留的边界 |
| --- | --- | --- |
| M3 | [卡与证明链](../tools/m3-largeR-closure.md), [接受包](../blueprint/submissions/SUB-20260825-B4M3-FINAL-003/) | n=2 对称 INF, large-R, 有限非零内部 chart; canonical 接收仅对应明确 target |
| KP-DET | [sequence-26][kp-whiteboard], [分支包][kp-branch], [求积包][kp-quadrature] | 完整约束下 0<c<=2/3 分支与 P20-P21 求积; 主 run Q9 保留 OPEN 记录, P1-P4 接收与后续 run 分开 |
| 外部 Q9 benchmark | [三臂结论][q9] | 插件另有证明/匿名外审记录; 未接入本 canonical/Lean, 不升级为本项目全局闭合 |

## 历史与证据

[工具入口](../tools/README.md) 区分卡片版本保存, 默认检索, 独立审查与自动接收. [Lean 状态](../lean-proof/STATUS.md), [义务审计](../lean-proof/audit_report.md) 和 [脚手架登记](../lean-proof/formalization_progress.md) 须结合确切声明与版本读取. 本轮没有新数学验收或形式化.

逐轮过程保存在 [会话日志](../state/AGENTS_SESSION_LOG.md), 各报告及 [整理前原字节快照](history/entry-snapshots-20261008.json). [最早中文首页](history/README.pre-v2.zh.txt) 和 [英文首页](history/README.pre-v2.en.txt) 继续保留. 历史中的路径按原文件位置解释, 未提交/未上传/旧 HEAD 按当时语境阅读; 后续实际发布见 [续接入口](../state/RESUME.md).

[kp-whiteboard]: ../research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/whiteboard-26.md
[kp-branch]: ../research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/route-09-acute-threshold/accepted_package.md
[kp-quadrature]: ../research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/route-10-psi-quadrature/accepted_package.md
[q9]: https://github.com/xsoc1/rigorous-open-math-research/blob/f95627ca1b44aeb75692a5814e20050b0e6a40cb/benchmarks/codex-20260908-q9/CONCLUSIONS.md
