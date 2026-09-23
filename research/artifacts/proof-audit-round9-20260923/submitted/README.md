# 第九轮独立审计附件

固定版本 `2a81b608d53e3decee04c46716a8d8f8c2d9b1b4`，审计日期 2026-09-23。

- `proof_audit_round9_20260923.md`：审计报告。
- `analytic_repairs.md`：反例、最小修复、平衡候选单调极限的完整解析补证。
- `checks.py`：独立检查程序，不导入仓库源码。
- `results*.json`、`execution*.log`：本轮实际普通模式与优化模式输出。
- `source_manifest.json`：读取来源及 Git blob 身份。
- `artifact_hashes.json`：当前附件文件 SHA-256。

运行需要 Python 3、mpmath、NumPy、SymPy：

```sh
python checks.py results.json
python -O checks.py results_optimized.json
```

20 个检查组涵盖精确有理包络、符号恒等式、错误候选拒绝和有限高精度/浮点交叉检验。不是作者整套程序或 Lean 的重跑，不是全部仓库定理的自动认证。

无穷维论证与全部指标结论由解析补证承担。审计未改变远程仓库。没有将新的补证伪称为仓库已经接受或发表的结果。
