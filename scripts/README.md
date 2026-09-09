# 研究脚本导航

[研究导航](../docs/research-guide.md) | [工具库](../tools/README.md) | [目录与复现](../docs/repository-guide.md)

本目录积累了不同阶段的数学程序. `num_*`, `h3_*`, `op*`, `_gapn2_*` 等名称是历史命名, 不表示统一 API 或严格性等级. 保留研究程序的输入条件, 精度, 输出与证明接口, 才能判断它能支持什么结论.

| 需要做的事 | 先读什么 |
| --- | --- |
| 查找相位, 转移矩阵或谱极值方法 | [研究图的 B 系列](../research_map.md), [谱研究导航](../docs/research-guide.md) |
| 查找矩递推或稠密性程序 | [研究图的 A 系列](../research_map.md), [工具索引](../tools/README.md) |
| 重放精确证书 | 对应 run 的 `repro_manifest.md`, `reproducibility/` 或证明中的程序清单 |
| 理解一次失败尝试 | 原 run 的研究台账, 反例记录与后续修正, 再看 [项目理解](../docs/PROJECT_UNDERSTANDING.md) |
| 维护 Blueprint | 当前安装插件的运行时 gateway, 见 [维护规则](../AGENTS.md) |

数值网格和浮点优化通常提供 EVIDENCE. 符号恒等式或有理数证书可以成为严格论证的一部分, 前提是数学证明说明了覆盖范围, 精确算术和从计算结论到定理的连接. 目录位置不能替代这项判断.

部分程序在 run 中还有相同副本. 例如 `densbc_v1_*` 至 `densbc_v6_*` 被历史台账按当前路径引用, run 副本又承担固定复现包的用途, 因此本轮保留两者. 没有把 scratch, 超时或无返回任务自动判为废弃研究.

本轮移除了经检查无调用或证据引用的一次性维护程序, 清单见 [清理报告](../reports/repository-cleanup-20260909/REPORT.md). 新增可复用数学程序时, 可在工具卡记录用途和指针, 让后续研究找到它, 不需要再复制一份通用执行框架.
