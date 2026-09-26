# 第十二轮证据入口

[修订报告](../../../reports/proof-audit-round12-20260926/REPORT.md)给出结论、当前可用性和证据边界。本目录将原始材料、作者工作、协调器执行和独立检验分别保存。

| 内容 | 入口 | 如何使用 |
| --- | --- | --- |
| 外部审计与清单核对 | [submitted](submitted/)、[intake-verification.json](intake-verification.json) | 输入材料和摘录身份，不自动视为已证结论 |
| 原完整源码与旧卡 | [before](before/) | 追溯漏模、错删极点及扇区标签；不可代替当前可用工具版本 |
| 隔离复现 | [intake-replay](intake-replay/) | 原检查普通/-O，以及完整旧源码行为 |
| 解析修订 | [analytic-repair.md](analytic-repair.md)、[作者交接](analytic-author/author-note.md) | 按明确条件逐项阅读；作者有限自检不是独立批准 |
| 当前独立检验 | [review-summary.json](review-summary.json)、[native-transcripts](native-transcripts/) | 回执分别绑定输入 SHA256、作者与新检验者身份 |
| 软件首轮与复验 | [software-review](software-review/)、[software-review2](software-review2/) | 保留首轮溢出发现和后续实际隔离执行，范围为软件及有限数值 |
| 协调器回归与实际入口 | [coordinator-checks](coordinator-checks/)、[coordinator-runs](coordinator-runs/) | 首次 CLI 失败和修复后的结果并存；复核源码版本和调用参数 |
| Lean 作者证据 | [lean-author](lean-author/) | 原机器结果、契约、失败与导出原样保留；首轮导出有省略缺陷 |
| Lean 导出修补 | [formal-export2](formal-export2/) | 同一数学源码的新目录重编译；完整无省略导出和协调器失败记录 |
| Lean 盲读 | [formal-readback](formal-readback/)、[formal-readback2](formal-readback2/) | 首次 INCOMPLETE 与全新会话完整盲读分开，不把旧回执覆盖成通过 |
| Lean 语义与实际执行 | [formal-comparison](formal-comparison/)、[formal-execution](formal-execution/) | 另一新会话亲自编译、比对类型/定义/公理与正负对照 |
| 工具库与续接 | [integration](integration/)、[实际检索](integration/library-verification.json)、[检查点](integration/checkpoint.json) | 原版纠错模块逐义务放行；核对卡片、摘要、来源、依赖和批注绑定 |

大量 JSON 以无损 gzip 保存时，清单同时记录压缩文件和原字节的 SHA256。不要将解压出的旧绝对路径直接用作覆盖命令。重放应使用新工作目录、冻结源码和原版验证器；原始命令记录保留执行当时的真实路径。

本轮 Lean 只认证有限实矩阵代数及坐标/归一化桥梁。解析 Green 证明、有限浮点测试和全局未完成义务各有边界。canonical、旧冻结研究和现有 52 份 Lean 源没有被本轮验收升级。
