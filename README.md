# Sturm-Liouville 边值问题研究

[English](README_EN.md) | [按问题阅读](docs/research-guide.md) | [问题与剩余缺口](research_map.md) | [接续研究](state/RESUME.md)

本仓库保存 Sturm-Liouville 理论的人机合作研究: 证明, 反例, 失败路线, 计算工具和部分 Lean 形式化. 数学来源包括既有文献, 合作者工作和项目推导, 归属与证据以原文和研究包为准. 项目使用 [数学研究插件](https://github.com/xsoc1/rigorous-open-math-research) 支持长期研究与验证.

## 两条研究主线

- **左定空间与正交系.** 研究 Krein 模型中的算子幂域, 原稀疏多项式族的完备性, 删项闭包, 有限约束及稳定替代系. 区分代数多项式传输, 抽象完备化和真实自伴算子域.
- **特征值比值与谱隙.** 研究 Dirichlet 问题 $-y''=\lambda\rho y$ 的相邻比值与间距极值, 开关结构, 对称性及唯一性. 各证明的权重类与参数范围分别保留.

## 代表成果与适用范围

| 问题 | 已有成果 | 推荐证明 |
| --- | --- | --- |
| 全序列相邻比值 B1/B2 | 在原文权重类中有上确界闭式; 下确界为 1 且不达到 | [上确界](docs/SL_ratio_proof.tex), [下确界](docs/SL_inf_ratio_proof.tex) |
| 固定指标候选 B3 | 平衡候选的 2n 简单根计数, 候选比值严格递减及其极限; 与全局最优值相等仍开放 | [候选谱证明](docs/SL_fixed_n_supremum.tex) |
| n=1 谱隙 B4 | 归一化盒类 $1\le\rho\le R$ 中全部 $R>1$ 的 SUP/INF 证明链 | [主证明及前置材料](docs/research-guide.md#n1-谱隙) |
| n>=2 谱隙 B4 | 有限块与精确开关结构, 弱反差局部唯一性; G2 对全部精确零点在 $1\le R\le R_{max}$ 上给统一正块宽 | [局部证明](docs/SL_gap_nge2_symmetry_local_proof.tex), [完整 G2 补证](docs/SL_G2_compactness_proof.md) |
| 原族与删项 A1/A11/A12 | 固定 $c>0$, 真实复 $\mathcal H_c^s$, $0\le s<7/2$: 原族稠密; 任意保留集的稠密充要判据, 两奇偶倒数和发散时的精确缺迹闭包, 任一收敛时无限余维 | [成员窗口](docs/SL_fractional_left_definite.tex), [全窗口删项](docs/SL_full_window_deletions_and_finite_constraints.md) |
| 有限约束 A3-KREIN-FINITE | 同一模型及窗口内, 逐个成员筛选的完备性恰对应连续中心迹的部分坐标核交 | [完整证明第 7 节](docs/SL_full_window_deletions_and_finite_constraints.md#7-任意有限个连续约束下的逐项筛选分类) |
| 整数阶替代系 A10 | 每个固定 $c>0$ 和非负整数阶的 Hermite-Legendre Riesz 替代基; 次数一致界, 速率另需加权系数条件 | [完整整数阶证明](docs/SL_integer_left_definite_riesz_systems.md) |
| 有界方向谱尾 B11 | 正有界密度及实 $L^\infty$ 方向的 Parseval 剩余与两侧谱尾界; 符号认证需可靠有限输入包络 | [完整谱尾证明](docs/SL_bounded_direction_spectral_tail.md) |

这些条目分别指向具体数学合同. G2 不证明 ND/G1 或无条件全局唯一性; Riesz 结论针对新替代系, 不改变原族非基结论; 谱尾结论不覆盖 delta/delta-prime 界面方向. [研究地图](research_map.md) 保留全部稳定编号及依赖, [研究导航](docs/research-guide.md) 说明前置材料和历史替代关系.

## 主要开放问题

- 固定 n 比值的全局最优性 O1/O2; n>=2 谱隙的 ND/G1, 无条件全局唯一性与最优值.
- 收敛删项侧闭包全部元素的描述, 一般非对角 A3/A4, 无限约束, 非整数阶稳定替代系及 $c\downarrow0$ 一致性.
- 一般递推的非齐次源项控制和更广系数族. M3/KP-DET 的已有局部或 chart 结果与剩余全局问题分别见 [导航](docs/research-guide.md#局部-chart-与外部结果).

## 阅读与接手

| 需要什么 | 入口 |
| --- | --- |
| 数学理解, 直觉, 失败路线与人的批注 | [项目理解](docs/PROJECT_UNDERSTANDING.md) |
| 当前计算接口, 精确证书和历史实现 | [脚本导航](scripts/README.md) |
| 工具卡, 检索门禁和版本证据 | [工具入口](tools/README.md) |
| 目录职责, 源文件与 PDF 对应, 复现 | [仓库说明](docs/repository-guide.md) |
| 长期工作规则与本次维护 | [AGENTS.md](AGENTS.md) |
| 最新完成工作, 未完成事项及历史发布证据 | [RESUME](state/RESUME.md) |

数学证明, 独立审查, 软件测试, 工具库接收, Blueprint 接收, Lean 与远端发布分别登记. [Lean 状态](lean-proof/STATUS.md) 和对应声明的代码/日志界定形式化范围. [R14](reports/proof-audit-round14-20261004/REPORT.md), [R15](reports/proof-audit-round15-20261005/REPORT.md), [R16](reports/proof-audit-round16-20261006/REPORT.md) 保留各轮真实结果和失败回执; 整理前的入口原文在 [历史快照清单](docs/history/entry-snapshots-20261008.json), 完整对话在 [会话日志](state/AGENTS_SESSION_LOG.md).
