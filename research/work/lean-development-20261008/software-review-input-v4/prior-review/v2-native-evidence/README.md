# 原始 v2 审查证据保全

本目录仅保存 /root/plugin_review_v2 已发出的首次真实 FINAL_ANSWER 及该审查期间已执行的三项新复现的可恢复记录. 本次没有重新运行实验, 没有重新评价、检查或更改原报告结论, 没有修改研究工作树、冻结输入或插件工作树. 此次补充 FINAL 仅报告保全路径, 不构成修补批准.

- report.json 是已发出的完整 JSON 报告的逐值副本; verdict 保持 CHANGES_REQUIRED. 保存格式为 UTF-8 JSON, 不声称等同于聊天服务内部未公开的原始序列化字节.
- reproductions/declared-tool-coverage/ 保全临时工具字节变更的两个实际根实验.
- reproductions/output-root-verify/ 保全输出等于根目录时的嵌套目标实验.
- reproductions/output-root-save/ 保全同输出布局下嵌套依赖变化后的保存实验.
- 各目录 reproduce.py 保留原 PowerShell here-string 中实际传给 Python -c 的代码; exec-command-call.json 保留已有 native 调用参数; native-record.json 保留已恢复的 session/chunk 身份、原 wait 参数和结果、原 exit code; original-output.txt 保留先前 native 工具返回的完整 JSON summary.
- manifest.json 记录这些保全文件的当前 SHA-256/字节长度. 这些是保全文件身份, 不是缺失临时运行工件的替代身份.

原三个程序已用 TemporaryDirectory 清理原临时源、Lean stdout/stderr/job logs、manifests 等工件. 它们在清理前没有被另存, 原 split logs 现在不可恢复. 原顶层进程 PID 和明确的运行开始/结束 UTC 时间也未在可恢复输出中采集; 只保留真实 native session_id/chunk_id 与返回的 wait wall_time_seconds. 没有补造 PID、原日志、原时间、hash 或新的运行结果. 原输出中保留的临时绝对路径和 run IDs 是当时观察, 不代表当前仍有相应文件.

三项程序的原 exit code 均为 0; 这表示复现程序执行完成. 保留的输出仍包含当时观察到的失配结果. 本说明没有将 exit 0 解释为修补通过. 原冻结 packet 身份为 5e98a16d78949e397e42b429a05b03ab0c475b54818140b9c03a55ab42483ede.
