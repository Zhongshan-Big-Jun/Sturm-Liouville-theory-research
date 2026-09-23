# Sturm-Liouville 边值问题研究

[English](README_EN.md) | [研究导航](docs/research-guide.md) | [项目理解](docs/PROJECT_UNDERSTANDING.md) | [工具库](tools/README.md) | [Lean 状态](lean-proof/STATUS.md)

本仓库是使用 [rigorous-open-math-research 研究插件](https://github.com/xsoc1/rigorous-open-math-research) 开展长期数学研究的成果仓库. 保存人机合作形成的证明, 反例, 成功与失败路线, 可复用工具和部分 Lean 形式化.

数学内容包括既有文献, 合作者工作与项目中的推导. 插件帮助检索, 整理思路, 记录研究与组织验证; 具体归属和证据以原文及各研究包为准.

2026-09-23 文献吸收：[13项来源与阅读笔记](literature/absorption-20260923/README.md)接入工具库，形成分数/临界域字典、s=3余有限三迹闭包、s=2/4的相容Legendre替代系及有限移动界面公式，并判定两个无限删项子类。[报告](reports/literature-absorption-20260923/REPORT.md)列出独立检验和剩余范围；L13仍缺完整约束，不作为证明依赖。

2026-09-23 第九轮修订: 二阶变分程序改用真实块积分约束, 补齐本征函数导数的归一化核项; 撤回一维 Green 对角发散的错误解释. 物理世俗函数带频率因子, 严格反射对称的是归一化函数. 新的 Jacobi 证明给出平衡候选值随 n 严格递减及其极限, 尚未证明它就是全局最优值. 证据与检验范围见 [第九轮报告](reports/proof-audit-round9-20260923/REPORT.md).

2026-09-22 第八轮修订: 对称阱族 INF 极限改用连续相位下界覆盖整个薄层区域, 初等差量估计修复大 w 比较, T1 不再依赖旧网格或 T3 高精度数值. 固定内部 u 的首项为 C(u)/R; 最优值满足 0≤R m_R−M=O(1/R). 四张工具卡、精确有理证书、局部 Lean 与隔离检验见 [第八轮报告](reports/proof-audit-round8-20260922/REPORT.md).

2026-09-21 第七轮修订: 修正谱隙文稿的常密度公式, 用统一 Volterra 估计补齐端点引理及局部唯一性证明. 一般指标的上确界极限为 $\lim_{R\to\infty}S_n(R)=(n+1)^2\pi^2$; $4\pi^2$ 限于 $n=1$. 五张工具卡同步修正镜像导数、归一化及行列式/惯性边界, 十个诊断脚本修复直接传播问题, 解析与局部 Lean 的隔离检验见 [第七轮报告](reports/proof-audit-round7-20260921/REPORT.md).

2026-09-21 第六轮修订: 修复稀疏投影、有限矩检验与约束表示元的三类问题, 并补齐原完整稀疏族在真正左定空间中的精确非负稠密范围 $0\le s<7/2$. 两份解析证明和工具库传播经新的隔离审查通过; 局部 Lean 的覆盖范围见 [第六轮报告](reports/proof-audit-round6-20260921/REPORT.md).

2026-09-21 第五轮核查: O1'LD 的尾部刚性、无条件余有限稠密性和真闭子空间排除推论已被反证; 单项式有限删除引理的公式已核实修正. s=2 的两条迹替代分类已获独立审查通过, 新工具卡已恢复检索, 详见 [第五轮报告](reports/proof-audit-round5-20260921/REPORT.md).

2026-09-21 第四轮修订: 区分退化极限的普通函数代表与商类, 修复三阶递推程序、降阶前提与参数分类, 补出指定系数族的一般 c 最小解和常数. 解析证明、隔离检验及局部 Lean 的不同范围见 [第四轮报告](reports/proof-audit-round4-20260921/REPORT.md).

2026-09-20 第三轮审计: 修复一般递推与乘积模型的混淆、错误的基扰动稳健性与商空间证明漏洞. 工具卡、程序和局部 Lean 已随之修订; 证据、独立检验及适用边界见 [第三轮报告](reports/proof-audit-round3-20260920/REPORT.md).

2026-09-20 第二轮审计修订: 已补正谱模态、幂域阈值、首对全局极值证明与 K1 终端条件, 并将外部报告接入工具库纠错. 修订、隔离检验、局部 Lean 及剩余边界见 [第二轮报告](reports/proof-audit-round2-20260920/REPORT.md).

## 研究什么

- **正交系与左定空间.** 研究多项式系的完备性, 受约束空间的稠密性, 矩递推与算子幂域. 特别区分代数多项式逆, 抽象完备化和真正的自伴算子逆.
- **特征值比值与间距.** 研究 Dirichlet 问题 $-y''=\lambda\rho y$ 的相邻比值和谱隙极值, 以及极值权重的开关结构, 对称性和唯一性. 每项结果采用的权重类与参数范围见原证明.

## 从这里阅读

| 想了解什么 | 入口 |
| --- | --- |
| 各研究问题的证明与剩余缺口 | [研究导航](docs/research-guide.md) |
| 目前怎样理解问题, 怎样共同研究 | [项目理解与人的批注](docs/PROJECT_UNDERSTANDING.md) |
| 问题编号与依赖关系 | [研究关系图](research_map.md) |
| 文献方法, 自研工具与失败路线 | [工具库及索引](tools/README.md) |
| 目录用途, 文档构建与复现 | [仓库使用说明](docs/repository-guide.md) |

## 主要成果与范围

下表保留2026-09-09整理的总体导航, 左定空间条目已按第六轮修订更新, 谱隙条目按第七、八轮修订更新, 固定 n 候选谱按第九轮修订更新. `STRICT` 只适用于来源给出的陈述与假设, 不表示整个项目已经解决或全部形式化.

| 研究线 | 已有成果 | 范围与证据 |
| --- | --- | --- |
| 全序列相邻比值 | 上确界的平衡相位闭式, 下确界为 1 且不达到 | [上确界](docs/SL_ratio_proof.tex), [下确界](docs/SL_inf_ratio_proof.tex); 按原文权重类使用 |
| 固定 n 平衡候选比值 | 完整 2n 简单根计数; 候选 c_n 严格递减至 ((pi−phi)/phi)² | [当前证明](docs/SL_fixed_n_supremum.tex); phi=arccos((sqrt(R)−1)/(sqrt(R)+1)), R>1; 全局最优性仍开放 |
| n=1 相邻间距 | SUP/INF 的归约, 刚性, 对称线与极值证明链 | [证明导航](docs/research-guide.md); 归一化盒类的全 R>1 结果 |
| 对称阱族 INF 极限 | R m_R→M≈24.9438661384, 非负误差 O(1/R); Rη_R→0 的近极小化子收敛 | [第八轮连续证明](docs/SL_gap_n1_inf_limit_proof.tex); 相位薄层界与大 w 比较覆盖 R≥1500; 非对称族及全盒类须另核对 |
| n>=2 间距结构 | 有限块结构, 弱反差局部对称性; 固定 n>=1 的 SUP 极限为 (n+1)²pi² | [当前局部证明与上确界极限](docs/SL_gap_nge2_symmetry_local_proof.tex); 可测盒类和有限分块类; 有限 R 全局唯一性仍开放 |
| 左定空间与算子域 | 原完整稀疏族在0<=s<7/2稠密, s=2余有限分类, 以及算子幂域障碍 | [完整窗口](docs/SL_fractional_left_definite.tex), [s=2余有限分类](docs/SL_cofinite_left_definite.tex), [幂域障碍](tools/krein-power-domain-polynomial-obstruction.md) |
| B4/P1 M3 | STRICT 渐近与两个扇区行列式符号 | [工具与证明链](tools/m3-largeR-closure.md); n=2 对称 INF, large-R, 有限非零内部 chart |
| KP-DET | 完整约束下 0<c<=2/3 的分支闭合, P20-P21 精确求积约化 | [sequence-26][kp-whiteboard]; 经审计的部分结果, 本地主 run 的 Q9 仍为 OPEN |

插件仓库另有 [Q9 三臂完整证明与匿名外审][q9], 尚未接入本仓库 canonical, 也未做 Lean 形式化. 这与主项目当前状态分开登记, 不据此宣称全局 G1', KO-DET 或完整 n>=2 极值问题已解决.

## 仍在研究

- n>=2 间距极值的全局非退化, 对称性, 唯一性及最优值.
- 固定 n 比值的全局最优值及真正上确界序列的性质. 平衡候选的 2n 根计数、单调性与极限见 [导航](docs/research-guide.md).
- 一般非对角空间的稠密性判据 O1'/O1'LD, 其它阶的删除分类与受约束空间问题. 原完整族的0<=s<7/2窗口已补证.
- 三阶递推的非齐次源项控制与更一般系数族. [指定双奇偶系数族](docs/SL_third_order_recurrence_theory.tex) 的全部 c>0 最小解、常数和有理比值分类见第四轮修订; [K(1)=e/4](docs/SL_third_order_K1_proof.tex) 保留为偶族锚点.

问题地图和早期综述含不同时间的记录. 接续研究时以具体证明, 审计, 范围说明及最新 run 为依据; 导航列出了尚待对齐的 G2 状态差异.

## 形式化状态

[lean-proof/](lean-proof/) 固定 Lean/mathlib v4.31.0, 包含已经机器检查的引理和证明片段, 也包含带 `sorry` 的研究脚手架及条件化的分析接口. 历史构建成功只覆盖对应文件与版本.

查看 [状态表](lean-proof/STATUS.md), [义务审计](lean-proof/audit_report.md) 和 [脚手架登记](lean-proof/formalization_progress.md), 再核对具体根定理与依赖. 仓库没有宣称全部数学结果已经通过 Lean 验证.

## 维护与协作

本项目欢迎围绕问题, 证明和研究理解进行合作. 进入仓库先读 [AGENTS.md](AGENTS.md); 人的直觉和 agent 的自由批注可以写入 [项目理解](docs/PROJECT_UNDERSTANDING.md) 或相关工具卡, 并注明证据状态.

[主仓库](https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research) 与 [fork](https://github.com/xsoc1/Sturm-Liouville-theory-research) 按项目规则同步. [本轮清理报告](reports/repository-cleanup-20260909/REPORT.md) 记录目录整理, 删除理由和证据保护; 旧首页保存在研究导航的历史入口.

[kp-whiteboard]: research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/whiteboard-26.md
[q9]: https://github.com/xsoc1/rigorous-open-math-research/blob/f95627ca1b44aeb75692a5814e20050b0e6a40cb/benchmarks/codex-20260908-q9/CONCLUSIONS.md
