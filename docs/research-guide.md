# 研究导航

[中文首页](../README.md) | [English overview](../README_EN.md) | [项目理解](PROJECT_UNDERSTANDING.md) | [目录与复现](repository-guide.md)

本页按问题寻找证明, 工具和剩余缺口. 状态核对日期为 2026-09-09. `STRICT` 表示所引来源在明确范围内提供严格证明; 独立审计, canonical 接收和 Lean 验证分别查看对应记录. 本次导航整理没有重新审计数学证明.

## 特征值比值与间距

研究模型以 Dirichlet 问题 $-y''=\lambda\rho y$ 为主. 注意每篇证明采用的权重类: 部分早期比值文档写为分段连续类, 后续间距研究采用可测盒类. 复用结论时保留各自的定义与推广论证.

| 问题 | 证明与研究入口 | 当前可使用的范围 |
| --- | --- | --- |
| 全序列相邻比值上确界 | [比值证明](SL_ratio_proof.tex), [PDF](SL_ratio_proof.pdf), [Mahar-Willner 引理重证](SL_mw_lemma_reproof.tex) | 文档所述权重类内的平衡相位闭式; 固定 n 的最优问题另列 |
| 全序列相邻比值下确界 | [下确界证明](SL_inf_ratio_proof.tex) | 下确界为 1, 不达到; 通过 Weyl 渐近处理高指标 |
| n=1 间距极值 | [主证明](SL_gap_n1_proof.tex), [相位刚性](SL_gap_n1_O3a_phase_rigidity_proof.tex), [全 R 阱族刚性](SL_gap_n1_well_rigidity_allR_proof.tex), [对称线](SL_gap_n1_symline_allR_proof.tex), [全局 good-root](SL_gap_n1_global_goodroot_proof.tex), [INF 极限](SL_gap_n1_inf_limit_proof.tex) | SUP/INF 的完整证明链分别核对; 早期单篇文档的待办不代表整条路线的最终状态 |
| n>=2 间距结构 | [有限块约化](SL_gap_nge2_finite_reduction_proof.tex), [精确 2n 开关](SL_gap_nge2_exact_2n_switches_proof.tex), [局部对称性](SL_gap_nge2_symmetry_local_proof.tex) | 有限维结构及弱反差局部结果; 全局唯一性与完整分类仍有缺口 |
| 最小化方向的合作者结果 | [研究进展](SL_gap_nge2_min_direction_progress.tex), [可读 PDF](SL_gap_nge2_min_direction_progress.pdf), [审计](../runs/rigorous-open-math-research/R-20260816T174722Z-min-direction-audit/), [核验包](../collaborator_min_direction_verification/) | 按原文的 n, mu, 弱反差条件区分 Trusted, Reviewed 与 Open |
| 固定 n 比值上确界 B3 | [早期相位文档](SL_fixed_n_supremum.tex), [后续研究对比](../reports/plugin-performance-b3-ab.md), [一般交替 Chebyshev 表示](../reports/plugin-performance-b3-o1o2-current.md) | 极大子的精确 2n 开关结构及平衡世俗函数的 2n 简单根计数已有后续 STRICT 结果; 全局最优值及其余单调性问题仍开放 |
| B4/P1 M3 | [工具说明](../tools/m3-largeR-closure.md), [证明工件](../research/artifacts/blueprint-rigorous-math/R-20260825T100044Z-b4-m3-blueprint/), [接收记录](../blueprint/submissions/SUB-20260825-B4M3-FINAL-003/) | n=2 对称 INF, large-R, 有限非零内部 chart; 存在有限 R0, 对 R>R0 得到规定的渐近与符号结论 |
| KP-DET | [sequence-26 白板][kp-whiteboard], [分支接受包][kp-branch], [求积接受包][kp-quadrature] | 完整约束下 0<c<=2/3 已严格闭合; P20-P21 给出精确求积约化; 本地主 run 的 Q9 仍记录为 OPEN |

### Q9: 主项目记录与插件 benchmark 分开读取

主项目 [sequence-26][kp-whiteboard] 的数学状态是 `RIGOROUS_PARTIAL_RESULT`. P1-P4 的 pivot/phase 部分已进入 canonical; 后续分支和求积结果在经审计的 run 包中, 本轮没有接收新的 canonical proposal.

插件仓库的 [Q9 三臂对照结论][q9] 另保存了 A/B/C 三份完整 Q9 证明及匿名外审 PASS. 该报告明确说明未做 Lean 形式化, 未重新审计主项目全部上游依赖, 也未集成到本仓库. 后续可以对齐原始题面, 参数字典与全部依赖, 再决定如何接入研究主线. 这组结果不能直接升级为全局 G1', KO-DET 或完整 n>=2 极值问题已解决.

### 旧记录中的状态差异

`SL_spectral_topics_summary.tex` 和部分局部证明增补记有特定框架的 G2 边界生成排除, 而较新的 M3 范围说明仍把 chart 外的 all-R G1'/G2 列为开放. 这些来源尚未在本轮按定义与量词逐项对齐. 首页不合并这些标签, 也不据此宣称完整全局结论已闭合.

## 左定空间, 正交系与矩方法

| 问题 | 入口 | 使用时需要保留的区别 |
| --- | --- | --- |
| H2 完备性 | [完整证明](SL_h2_completeness_proof.tex), [研究总结](SL_h2_research_summary.tex) | 矩递推, 增长引理与湮灭步骤有各自前提 |
| H3 与高阶传输 | [H3 证明](SL_h3_completeness_proof.tex), [H3 总结](SL_h3_research_summary.tex), [Hs 正交系](SL_hs_orthogonal_systems_proof.tex) | 代数多项式逆, 抽象完备化与自伴算子幂域分别处理 |
| 幂域障碍 A7 | [工具与精确定理](../tools/krein-power-domain-polynomial-obstruction.md), [pilot v6 证明与审计](../runs/three-arm-pilot-v2/pilot-v6-hs-domain/RESULTS.md) | 对 c>0, 整数 s>=4, 指定的代数传输多项式属于真正幂域当且仅当 n=0,1; 这不否定经边界修正的真正算子逆 |
| 受约束空间稠密性 | [早期判据](SL_denseness_criteria.tex), [项目问题图](../research_map.md), [非对角子类对比](../reports/plugin-performance-o1p-ab.md) | 对角及若干带状/加权移位子类已有结果; 一般非对角 O1' 与 O1'LD 仍开放 |
| 分数阶与门槛 | [分数阶文档](SL_fractional_left_definite.tex), [矩跳跃稳定性](SL_stability_moment_jump.tex) | 3/2<=s<2 的剩余窗, 门槛线系数族和变系数推广依来源分别标记 |
| 三阶递推 | [递推理论](SL_third_order_recurrence_theory.tex), [K(1)=e/4 证明](SL_third_order_K1_proof.tex) | 偶次 c=1 锚点 STRICT; 一般 K(c), 源项控制与一般系数族仍开放 |
| Krein c->0 | [退化极限](SL_krein_c0_limit.tex) | 多项式级结论与商空间级结论分别核对 |

## 从研究过程找工具

[工具库索引](../tools/README.md) 保存文献工具与自研方法. [研究关系图](../research_map.md) 保留稳定问题编号; [项目理解](PROJECT_UNDERSTANDING.md) 说明目前怎样理解这些结果, 哪些解释仍是假设, 失败路线在什么条件下值得重新检查.

寻找证据时优先跟随具体 run 的证明, 审计和复现清单. `scripts/` 同时包含数值探索与精确符号/有理证书程序, 其性质由实现与证明接口决定. [脚本导航](../scripts/README.md) 说明如何识别它们. 一组数值样本, 一个 `NO_RETURN`, 或一个编译成功记录都不能独自说明数学问题的真伪.

## 形式化与历史首页

Lean 的 [状态表](../lean-proof/STATUS.md), [义务审计](../lean-proof/audit_report.md), [脚手架登记](../lean-proof/formalization_progress.md) 记录不同时间与范围的工作. 阅读时核对所声称的根定理, 实际假设及依赖, 并使用其绑定的代码版本. 本次整理没有重跑 Lean, 也没有赋予新的形式化结论.

旧首页的完整文字按原字节保存在 [中文快照](history/README.pre-v2.zh.txt) 与 [英文快照](history/README.pre-v2.en.txt). 其中路径按原仓库根解释, 旧状态只作历史索引. 本页保留了研究文档入口, 并显式说明了固定 n 根计数, KP-DET 分支和形式化范围的后续变化.

[kp-whiteboard]: ../research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/whiteboard-26.md
[kp-branch]: ../research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/route-09-acute-threshold/accepted_package.md
[kp-quadrature]: ../research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/route-10-psi-quadrature/accepted_package.md
[q9]: https://github.com/xsoc1/rigorous-open-math-research/blob/f95627ca1b44aeb75692a5814e20050b0e6a40cb/benchmarks/codex-20260908-q9/CONCLUSIONS.md
