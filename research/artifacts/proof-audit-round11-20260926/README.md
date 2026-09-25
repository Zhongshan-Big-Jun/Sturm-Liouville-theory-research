# 第十一轮证据入口

本目录将作者推导、实际程序执行、独立审查和工具库集成分开保存. 当前结论与范围见[最终报告](../../../reports/proof-audit-round11-20260926/REPORT.md).

| 内容 | 入口 |
| --- | --- |
| 用户提交的审计与补证 | [submitted](submitted/), [清单/源码身份核实](intake-verification.json) |
| Jacobian与差分的数学契约 | [jacobian-repair.md](jacobian-repair.md), [实际调用清单](caller-inventory.json) |
| 全阶余有限证明 | [冻结作者稿](cofinite-author/cofinite-all-orders.md), [可读PDF](../../../docs/SL_cofinite_all_orders.pdf) |
| 原错误与作者程序检查 | [before](before/), [software-author](software-author/) |
| 独立软件执行 | [software-execution](software-execution/) |
| 独立解析审查的辅助检查 | [cofinite-execution](cofinite-execution/) |
| Lean作者自检 | [lean-author](lean-author/), [无损档案清单](lean-author-archive-manifest.json) |
| 独立Lean执行与比对 | [formal-execution](formal-execution/), [无损档案清单](formal-execution-archive-manifest.json) |
| 六份最终独立审查 | [review-summary.json](review-summary.json) |
| 工具纠错、版本批注及实际检索 | [integration](integration/) |
| PDF构建与视觉核对 | [pdf-build](pdf-build/) |

`cofinite-review`, `software-review`, `formal-readback`, `formal-comparison`各有独立最小项目和冻结审查包. 数学纠错与未变卡续审使用主项目原版库; 对应完整路径在审查汇总中. 原生spawn/wait记录和接收回执保留各自身份, 信任层为协调器保存的实际工具调用记录, 不是平台签名.

作者稿和作者Lean摘要保留交稿时的候选状态. 当前独立验收以精确回执为准; 不改写历史标签来伪装作者已经独立验收. 大型JSON/log采用无损gzip时, 清单同时保存原始与编码后的SHA256. 编译产物和完整Mathlib树留在外部执行目录, 由源、环境身份和真实命令支持复现.

已读外部论文的新增整篇原文保存在私有来源缓存, 本目录只新发布原创推导、来源位置及哈希指针. 解析证明不以未供应的外部结论替代必要论证. 本轮不接收canonical, 不把有限样本或局部实矩阵Lean证明扩大为完整分析定理的形式化.
