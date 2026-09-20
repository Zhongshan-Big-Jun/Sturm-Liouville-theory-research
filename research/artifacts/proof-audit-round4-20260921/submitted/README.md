# 第四轮审计包

固定仓库提交：`2e9bf3d66fa21a41e16bf779782739ddd9505233`。

- `proof_audit_round4_20260920.md`：审计结论、反例、影响范围、最小修订建议。
- `constructive_repairs.md`：独立推导的修复证明，未写回仓库，未做 Lean 或他人独立验收。
- `check_round4.py`：本轮自足检查；使用 Python、SymPy、mpmath，无网络和仓库写入。
- `round4_results.json`、`check_round4.stdout.txt`：实际结果；PASS 是具名检查得到确认。
- `author_run.json`、`d3_stability_verify.*.txt`：当前一份作者程序的身份和实际运行日志。
- `manifest.json`：交付文件哈希及执行环境。

运行独立检查：

```bash
python check_round4.py
```

运行作者诊断需要自己的固定提交仓库副本：

```bash
python scripts/d3_stability_verify.py
```

该作者程序的预期 Git blob SHA-1 在 `author_run.json` 中。为避免重复打包仓库原文件，压缩包不含这份原程序，只含其运行证据。没有声称运行所有作者脚本、全部历史测试或 Lean。
