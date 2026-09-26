# Round 12 audit package

固定仓库提交：`be7c0912849a50a46869773eab4b3a2ec655ce88`。

- `proof_audit_round12_20260926.md`：中文审计报告与适用范围。
- `analytic_repairs.md`：半区间谱的解析反例、提升相位修复条件、原Ko与共轭K奇块的推导。
- `checks.py`：34个具名检查，确认结果包含确认错误。
- `source_excerpts/`：当前GitHub源函数摘录，不是整份原文件的下载副本。
- `green_sector_check.py`：独立65位传递、隐式求导及Green有限部实现。
- `primitive_check.py`：九个原函数的符号表示。
- `evidence/`：实际普通模式/优化模式日志、JSON、环境与反例输出。

需 Python、NumPy、SymPy、mpmath。执行：

```
python checks.py
python -O checks.py
```

不联网、不写仓库。执行会更新本目录evidence，不会认证任何无穷维定理。所附本轮分析没有独立审稿人验收或Lean形式化。
