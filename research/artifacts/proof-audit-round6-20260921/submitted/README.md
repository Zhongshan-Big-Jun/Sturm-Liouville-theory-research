# 第六轮审计包

- `proof_audit_round6_20260921.md`：结论、定位与处置建议。
- `projection_and_moment_repairs.md`：投影反例、错误充要判据、旧F/H问题和准确替代条件。
- `fractional_window_completion.md`：原稀疏族0<=s<7/2的解析补证及逐成员精确阈值。
- `check_round6.py`：独立SymPy/Fraction检查，不访问网络或修改仓库。
- `round6_results.json`、`check_round6.log`、`check_round6_optimized.log`：实际执行结果。
- `source_manifest.json`：连接器返回的来源身份；不声称已获得原文件的本地字节副本。

运行环境需要Python和SymPy；本次使用的实际版本记录于JSON。

```bash
python check_round6.py
python -O check_round6.py
```

程序失败会抛出异常。它不是原仓库测试套件，也不是Lean证明。有限测试与全指标解析证明分开提供。
