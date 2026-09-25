# 第十轮复核包

对应仓库提交：`5bb6b2605122d2daf472863b4bec0f35a9c192e1`。
审计日期：2026-09-25。

## 文件

- `proof_audit_round10_20260925.md`：完整中文审计报告和来源路径。
- `analytic_notes.md`：匹配函数、精确括根与反射扇区说明。
- `checks.py`：23组独立检查。
- `probe_roots.py`：有意保留故障的求根逻辑语义复现，用于重现问题；不是建议的正确求根器，也不是完整作者源文件。
- `root_bracket_certificates.json`：精确有理包络（大分子、分母以字符串保存）。
- `check_results.normal.json`、`check_results.optimized.json`：两个模式的独立执行结果。
- `run_normal.log`、`run_optimized.log`：成功执行的输出。
- `manifest.json`：源身份、运行环境及交付文件SHA256。

## 运行

需要 Python3，以及 numpy、sympy、mpmath。实际检查环境为 Python3.13.5、NumPy2.3.5、Sympy1.14.0、mpmath1.3.0。

在本目录运行：

```bash
python checks.py
python -O checks.py
```

程序使用显式异常而非可被`-O`移除的assert。运行会覆盖当前目录的`check_results.json`与`root_bracket_certificates.json`，不会访问或改写GitHub仓库。预期输出23组得到确认，并返回退出码0。

`root_bracket_certificates.json`的有理数字符串超过Python默认整数字符串位数限制，检查程序仅为本地受控证书计算放开该限制。不要将此设置不加审查地用于接收不可信大整数输入的服务。

## 范围

执行的是本轮独立程序，不是原仓库整个测试套件，不是Lean。解析无限维结论依据原证明的阅读与推导检查，而不由有限样本认证。确认结果包括确认反例与源程序故障。

首次扩充二进制有理包络时曾因Python序列化限制中止；修正后已重新完成普通和优化两种执行。本包只将最终成功的两个运行记录作为结果，不把开发失败算作仓库问题。
