# 第十五轮复核包

审查基线：`ec45bf99ae746b0a3699557e06700a3c00c5a831`。报告日期2026-10-05。

先阅读 REPORT.md。新解析结果在 `proofs/full_window_deletions_and_finite_constraints.md`；一个当前遗留扫描器的反例在 analytic_notes.md。交给后续执行者的任务是 repair_prompt_sol_max.md（6.1sol max）。

## 重放

需要 Python 3 和 numpy、scipy、sympy、mpmath。实际版本见 environment.json。此包自含有限检查所用来源与摘录，不需要网络或写入原仓库：

```bash
python -B checks.py --output results/replay-normal.json
python -O -B checks.py --output results/replay-optimized.json
```

结果中的44项包含确认基线错误，并不代表修复代码应继续保持错误输出。普通/-O原执行记录在results/。精确有理括根、有限数值诊断和符号恒等式分别记录；全窗口删项及有限约束定理依靠解析证明。

`source/scripts` 中仅两份模块核对为完整上游字节，其余是明确标注的摘录/导入适配。详见 source_manifest.json。独立物理参考没有导入仓库函数，但属于审查者自己的实现复用，不是另一位审稿人的回执。

本轮没有修改远端，没有执行原作者完整CLI/全部测试、Lean或57项证书完整生成；新证明尚未独立验收或合并。

包内 manifest.json 给出其他交付文件的SHA-256，不包含它自身，避免自引用。旧第十四轮大包、编译缓存、无关候选不在此包内。
