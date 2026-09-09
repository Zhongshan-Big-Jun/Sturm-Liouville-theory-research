# Sturm-Liouville 边值问题研究

[English](README_EN.md) | [研究导航](docs/research-guide.md) | [项目理解](docs/PROJECT_UNDERSTANDING.md) | [工具库](tools/README.md) | [Lean 状态](lean-proof/STATUS.md)

本仓库是使用 [rigorous-open-math-research 研究插件](https://github.com/xsoc1/rigorous-open-math-research) 开展长期数学研究的成果仓库. 保存人机合作形成的证明, 反例, 成功与失败路线, 可复用工具和部分 Lean 形式化.

数学内容包括既有文献, 合作者工作与项目中的推导. 插件帮助检索, 整理思路, 记录研究与组织验证; 具体归属和证据以原文及各研究包为准.

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

下表概括已有证明及经审计研究包的状态, 核对至 2026-09-09. `STRICT` 只适用于来源给出的陈述与假设, 不表示整个项目已经解决或全部形式化.

| 研究线 | 已有成果 | 范围与证据 |
| --- | --- | --- |
| 全序列相邻比值 | 上确界的平衡相位闭式, 下确界为 1 且不达到 | [上确界](docs/SL_ratio_proof.tex), [下确界](docs/SL_inf_ratio_proof.tex); 按原文权重类使用 |
| n=1 相邻间距 | SUP/INF 的归约, 刚性, 对称线与极值证明链 | [证明导航](docs/research-guide.md); 归一化盒类的全 R>1 结果 |
| n>=2 间距结构 | 有限块约化与精确 2n 开关定理 | [有限块](docs/SL_gap_nge2_finite_reduction_proof.tex), [开关定理](docs/SL_gap_nge2_exact_2n_switches_proof.tex); 全局唯一性仍开放 |
| 左定空间与算子域 | 矩方法完备性证明, 并识别代数传输多项式的幂域障碍 | [H2 证明](docs/SL_h2_completeness_proof.tex), [幂域障碍的精确范围](tools/krein-power-domain-polynomial-obstruction.md) |
| B4/P1 M3 | STRICT 渐近与两个扇区行列式符号 | [工具与证明链](tools/m3-largeR-closure.md); n=2 对称 INF, large-R, 有限非零内部 chart |
| KP-DET | 完整约束下 0<c<=2/3 的分支闭合, P20-P21 精确求积约化 | [sequence-26][kp-whiteboard]; 经审计的部分结果, 本地主 run 的 Q9 仍为 OPEN |

插件仓库另有 [Q9 三臂完整证明与匿名外审][q9], 尚未接入本仓库 canonical, 也未做 Lean 形式化. 这与主项目当前状态分开登记, 不据此宣称全局 G1', KO-DET 或完整 n>=2 极值问题已解决.

## 仍在研究

- n>=2 间距极值的全局非退化, 对称性, 唯一性及最优值.
- 固定 n 比值的全局最优值与剩余单调性问题. 后续研究已经证明的 2n 根计数见 [导航](docs/research-guide.md).
- 一般非对角空间的稠密性判据 O1'/O1'LD, 分数阶剩余窗与门槛分类.
- 三阶递推的一般 K(c), 源项控制与更一般系数族. [K(1)=e/4](docs/SL_third_order_K1_proof.tex) 是已严格证明的特定锚点.

问题地图和早期综述含不同时间的记录. 接续研究时以具体证明, 审计, 范围说明及最新 run 为依据; 导航列出了尚待对齐的 G2 状态差异.

## 形式化状态

[lean-proof/](lean-proof/) 固定 Lean/mathlib v4.31.0, 包含已经机器检查的引理和证明片段, 也包含带 `sorry` 的研究脚手架及条件化的分析接口. 历史构建成功只覆盖对应文件与版本.

查看 [状态表](lean-proof/STATUS.md), [义务审计](lean-proof/audit_report.md) 和 [脚手架登记](lean-proof/formalization_progress.md), 再核对具体根定理与依赖. 仓库没有宣称全部数学结果已经通过 Lean 验证.

## 维护与协作

本项目欢迎围绕问题, 证明和研究理解进行合作. 进入仓库先读 [AGENTS.md](AGENTS.md); 人的直觉和 agent 的自由批注可以写入 [项目理解](docs/PROJECT_UNDERSTANDING.md) 或相关工具卡, 并注明证据状态.

[主仓库](https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research) 与 [fork](https://github.com/xsoc1/Sturm-Liouville-theory-research) 按项目规则同步. [本轮清理报告](reports/repository-cleanup-20260909/REPORT.md) 记录目录整理, 删除理由和证据保护; 旧首页保存在研究导航的历史入口.

[kp-whiteboard]: research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/whiteboard-26.md
[q9]: https://github.com/xsoc1/rigorous-open-math-research/blob/f95627ca1b44aeb75692a5814e20050b0e6a40cb/benchmarks/codex-20260908-q9/CONCLUSIONS.md
