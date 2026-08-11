# lean-proof

Sturm-Liouville 理论研究项目的 Lean 4 + mathlib 形式化工程.
每个文件在文件头注释中标明其形式化的源文档 (docs/SL_*.tex).

**形式化总览与诚实状态**: 见 [STATUS.md](STATUS.md) (完整状态矩阵: 每个已证结果 -> 形式化状态).
结论: 目前只形式化了已证结果的极小部分, 远未完成.
义务级审计 (会话 66, StabilityGrowth + MomentRecurrence): [audit_report.md](audit_report.md) + [verification.json](verification.json).

## 目录结构

```
lean-proof/
├── README.md         本文件 (入口)
├── STATUS.md         形式化状态总表 + 路线图
├── audit_report.md   义务级审计报告 (lean-verify, 会话 66)
├── verification.json 结构化验证裁决 (lean-verify schema)
├── lakefile.lean     Lake 工程文件 (globs := #[`SL.+])
├── lean-toolchain    Lean 4.31.0 / mathlib v4.31.0
├── run-manifest.json 机器验证记录 (lean-verify 扫描 + lake build)
└── SL/
    ├── Basic.lean            命名空间骨架
    ├── MomentGrowth.lean     增长引理 (H^2 证明线)
    ├── KcPolynomial.lean     K_c 多项式系数恒等式 (H^2 证明线)
    ├── StabilityGrowth.lean  定量增长引理, 一般系数, 任意线性有序域 (稳定性证明线)
    ├── MomentRecurrence.lean 线性泛函矩递推 + 缩放引理, Q 上 (H^2 证明线)
    ├── MomentBound.lean      L2 矩上界 |mu_k| <= ||g||_2 sqrt(2/(2k+1)) (H^2 证明线)
    └── BalancedPhase.lean    平衡相位三角闭式 (比值证明线)
```
## 构建与验证

```text
lake build                          # 构建整个包 (首跑需编译 mathlib)
lake env lean SL/<File>.lean        # 单文件检查
python <lean-verify>/scripts/verify_lean_project.py --project . --build
                                    # sorry/axiom 扫描 + 构建 (输出 run-manifest.json)
```

## 命名空间

所有文件位于 `SL` 命名空间, 子命名空间按主题 (MomentGrowth / KcPolynomial /
StabilityGrowth / MomentRecurrence / BalancedPhase). 新文件保持同名命名空间,
更新 STATUS.md 状态矩阵.

## 规则

- 只形式化源文档中严格证明的结果; 数值证据/猜想不得作为定理声明.
- 每个文件头注明源文档与覆盖范围; 修改文件后重跑 verify + 更新 STATUS.md.
- 不引入 `sorry`/`admit`/`axiom`; 引入外部定理 (文献结果) 需在注释中登记来源与依赖.
- 泛型引理 (如 StabilityGrowth) 使用 mathlib v4.31 的非捆绑有序域组合
  `[Field K] [LinearOrder K] [IsStrictOrderedRing K]` (LinearOrderedField 已弃用).
- Windows 下避免 PowerShell `Set-Content -Encoding UTF8` 写入文件 (会加 BOM, lean 报
  "expected token"); 用 Python `write_text(..., encoding='utf-8')` 或
  `[System.IO.File]::WriteAllText(..., UTF8Encoding($false))`.
