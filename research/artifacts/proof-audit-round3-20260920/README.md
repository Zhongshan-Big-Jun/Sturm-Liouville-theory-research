# 第三轮证据包

本目录保留外部审计、修订前原字节、精确检查、两次程序验收对应的执行证据、局部 Lean 机器证据和 PDF 构建记录. 最终结论、失败后的修复及限制见 [报告](../../../reports/proof-audit-round3-20260920/REPORT.md). 独立 agent 的冻结输入与原生回执在 `research/library/reviews/` 中, 由报告逐项链接.

`before/` 与第一次程序材料保留错误原式及当时输出, 仅供溯源. 不把作者 PASS 或历史标签当作最终验收. 程序最终材料在 `script-checks-revision2/`; 回放行为检查时设置 `AUDIT_SOURCE_ROOT` 为含 `scripts/` 的仓库或冻结输入根目录, 建议复制测试 harness 到新临时目录, 避免覆盖原结果. Lean 的回放与排除范围另见 [说明](lean/REPLAY.md).

原始命令中的绝对路径, 日期、stdout/stderr 和 SHA-256 按执行时保留. 它们不是为其它机器改写后的运行说明. 迁移时使用新输出目录与实际工具链, 并产生新的验证记录. 被 hash 绑定的文件以 `.gitattributes` 保留原始换行字节.
