# lean-proof

Sturm-Liouville 理论研究项目的 Lean 4 + mathlib 形式化工程.
每个文件在文件头注释中标明其形式化的源文档 (docs/SL_*.tex).

**形式化总览与诚实状态**: 见 [STATUS.md](STATUS.md) (完整状态矩阵: 每个已证结果 -> 形式化状态).
结论: 目前只形式化了已证结果的极小部分, 远未完成.

## 目录结构

```
lean-proof/
├── README.md         本文件 (入口)
├── STATUS.md         形式化状态总表 + 路线图
├── lakefile.lean     Lake 工程文件 (globs := #[`SL.+])
├── lean-toolchain    Lean 4.31.0 / mathlib v4.31.0
├── run-manifest.json 机器验证记录 (lean-verify 扫描 + lake build)
└── SL/
    ├── Basic.lean            命名空间骨架
    ├── MomentGrowth.lean     增长引理 (H^2 证明线)
    ├── BalancedPhase.lean    平衡相位三角闭式 (比值证明线)
    └── KcPolynomial.lean     K_c 多项式系数恒等式 (H^2 证明线)
```

## 构建与验证

```text
lake build                          # 构建整个包 (首跑需编译 mathlib)
lake env lean SL/<File>.lean        # 单文件检查
python <lean-verify>/scripts/verify_lean_project.py --project . --build
                                    # sorry/axiom 扫描 + 构建 (输出 run-manifest.json)
```

## 命名空间

所有文件位于 `SL` 命名空间, 子命名空间按主题 (MomentGrowth / BalancedPhase /
KcPolynomial). 新文件保持同名命名空间, 更新 STATUS.md 状态矩阵.

## 规则

- 只形式化源文档中严格证明的结果; 数值证据/猜想不得作为定理声明.
- 每个文件头注明源文档与覆盖范围; 修改文件后重跑 verify + 更新 STATUS.md.
- 不引入 `sorry`/`admit`/`axiom`; 引入外部定理 (文献结果) 需在注释中登记来源与依赖.
