# 第十六轮复核包

先读 REPORT.md。三个新增反例的可重放脚本为 checks.py；完整新证明在 proofs/。审计基线仍与第十五轮相同，没有远端修改。

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B checks.py --output /tmp/sl-r16-normal.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O -B checks.py --output /tmp/sl-r16-optimized.json
```

需要 numpy、scipy、sympy。输出确认基线缺陷和有限代数，不代表这些行为是修复后应当保留的结果。执行器应另写修后测试。`results/initial_failed.*`保留了审稿自身的一次过强正对照预测及其失败。

无完整仓库克隆、无完整CLI/全测试运行、无Lean或第二位审稿人。本包不含旧讲义PDF，不修改模型或账号设置。后续执行提示词面向6.1sol max，但不依赖任何未经核实的模型专属能力。
