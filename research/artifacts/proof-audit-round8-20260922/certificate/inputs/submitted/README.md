# 第八轮审计包

- `proof_audit_round8_20260922.md`：审计报告。
- `analytic_repairs.md`：精确包络依据、标量常数的初等替换、固定 u 的 1/R 展开。
- `checks.py`：本轮独立检查，不导入仓库代码。
- `results.json`、`results_optimized.json`：普通模式与 -O 的22组最终结果。
- `execution_normal.log`、`execution_optimized.log`：最终日志。
- `initial_symbolic_check_failure.log`：初版的符号化简未完成记录；已改成多项式余式检查。
- `source_manifest.json`：固定提交与连接器报告的源文件身份及阅读范围。

运行环境需要 mpmath 与 sympy。示例：

```bash
python checks.py results.json
python -O checks.py results_optimized.json
```

cot_iv 漏包的具体浮点返回值与操作系统/libm相关；该用例若在其他平台未重现，不能据此认定旧算法自动成为可靠区间扩展。其余有理覆盖反例和错误端点选择不依赖同一 libm 返回值。

没有重新认证整个 deep-sliver 区域，没有运行 Lean，没有修改仓库。不得把22组确认解读为22个仓库定理已被机器证明。
