# 2026-09-23 文献吸收

按用户提供的13篇文献与方案，把原文、项目适配和可继续研究的问题接到现有工具库。基线为 `902d2a931`。[交付报告](../../reports/literature-absorption-20260923/REPORT.md)记录独立检验、实际执行和最终接入状态。

## 从这里阅读

| 需要什么 | 入口 |
| --- | --- |
| 13篇来源、版本、原文位置与使用边界 | [来源指针表](SOURCE_TABLE.md)、[机器清单](source-catalog.json)、[书目](selected_references.bib) |
| 原问题与已有极值结果的逐条对照 | [L02/L12/L13](notes/L02-L12-L13-source-to-claim.md) |
| 奇偶幺正分解、分数/临界域、s=3余有限三迹闭包 | [域与闭包](domains/proofs/)、[逐篇阅读](domains/notes/) |
| 有限TSVD、s=2/4的Legendre相容Riesz替代系、无限删项子类 | [近似与删项](approximation/notes/) |
| 移动界面二阶公式、单接口/原子质量校准与适用性限制 | [界面推导](interfaces/derivations/)、[来源对照](interfaces/notes/) |
| 已完成的P0–P4范围与下一步验收目标 | [任务包](tasks/P0-P4.md) |
| 可检索、可批注的正式工具版本 | [工具库](../../tools/README.md)、[指针索引](../../index/tools.json) |

12项取得原PDF并定点阅读；L13只有出版社元数据与不完整预览，S₁/S₂尚未匹配，不能作为证明依赖。取得全文不等于通读或逐式审计。作者稿中的 `PENDING_INDEPENDENT_REVIEW` 保留其提交时状态；当前认可范围由工具卡和报告中的后续独立回执给出。

## 来源与复现

原始用户输入保存在 [submitted](../../research/artifacts/literature-absorption-20260923/submitted/)。原PDF、提取文本和读取记录在独立本机缓存 `F:/tools/sl-literature-absorption-20260923/source-cache`，由已安装2.0.1原版capture/read接口管理。机器清单分别记录URL、版本、原件/文本哈希、阅读范围和缓存source_id。

公开source_id捕获的是自己撰写的阅读笔记，类型明确为secondary；原件source_id属于独立缓存命名空间。跨机器复核可按URL取得同版原件并比对哈希，或使用上述本机缓存。artifacts下的P1–P4私有审查目录导出原生调用、回执、报告和输入映射，新取得的第三方整篇原文未随导出复制；它不是能脱离这些原件直接重跑的完整runtime包。P0原版冻结review包则保留了仓库原有的L02/L12两篇PDF输入。原有仓库PDF保留原名和原字节。

本轮没有接收新结论到Blueprint canonical，没有新增完整Lean形式化。解析审阅、有限精确检查、来源阅读分别标注。人的想法和agent批注可以继续添加，但不能把待证建议升级成已证结论。
