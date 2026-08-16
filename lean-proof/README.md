# lean-proof

Sturm-Liouville 理论研究项目的 Lean 4 + mathlib 形式化工程.
每个文件在文件头注释中标明其形式化的源文档 (docs/SL_*.tex).

**形式化总览与诚实状态**: 见 [STATUS.md](STATUS.md) (完整状态矩阵: 每个已证结果 -> 形式化状态).
结论: 目前只形式化了已证结果的一部分 (H^2 完备性证明线完整, H^3 代数核心与解析 H1 矩上界 + FTC 胶水/H1 内积识别已绿, H^s 传输算子闭式与传输约化已绿, 稳定性门槛线 Thm 2.2/2.3 核心已绿, 三阶递推线闭式/固定点/比值/分类/变差常数(第三解)已绿, Krein c->0 退化极限多项式级与 n>=4 一般 Θ 增长已绿, 比值证明线平衡相位三角闭式 + 三段转移矩阵/secular 方程已绿, 固定 n 交替配置反射对称 (J-共轭) 已绿, 稠密性准则矩刻画代数核心 (DensenessCriteria) 已绿, 间距线 n=1 对称线代数核心 (SymlineTensionRatio: P1/P2 比较引理 + FeEquiv/ρ 等价 + 张力比链 rho<=rho0, 含 gamma_0* 存在性/位置与 Lemma ys2 证书自由形式化, SymlineKeyLemma (P1/P2 对数导数界与 W0 引理证书自由代数核心) 与 SymlineUniqueZero (KEY LEMMA 装配核心: 唯一零点/符号结论, 端点符号/相位分支/导数恒等式为分析钩子) 已绿, 其余已证定理未开始).
义务级审计 (会话 66-69): [audit_report.md](audit_report.md) + [verification.json](verification.json) (O1-O24).

## 目录结构

```
lean-proof/
├── README.md         本文件 (入口)
├── STATUS.md         形式化状态总表 + 路线图
├── audit_report.md   义务级审计报告 (lean-verify, 会话 66-69)
├── verification.json 结构化验证裁决 (lean-verify schema)
├── lakefile.lean     Lake 工程文件 (globs := #[`SL.+])
├── lean-toolchain    Lean 4.31.0 / mathlib v4.31.0
├── run-manifest.json 机器验证记录 (lean-verify 扫描 + lake build)
└── SL/
    ├── Basic.lean            命名空间骨架
    ├── MomentGrowth.lean     增长引理 (H^2 证明线)
    ├── KcPolynomial.lean     K_c 多项式系数恒等式 (H^2 证明线)
    ├── StabilityGrowth.lean  定量增长引理, 一般系数, 任意线性有序域 (稳定性证明线)
    ├── Stability.lean       稳定性定理 Thm 2.2 泛函核心 + 尖锐性 Thm 2.3 级数 (稳定性证明线)
    ├── MomentRecurrence.lean 线性泛函矩递推 + 缩放引理, Q 上 (H^2 证明线)
    ├── MomentBound.lean      L2 矩上界 |mu_k| <= ||g||_2 sqrt(2/(2k+1)) (H^2 证明线)
    ├── Completeness.lean     H^2 完备性收尾: 湮灭 + Weierstrass 结论 (H^2 证明线)
    ├── H3Completeness.lean   H^3 矩跳变/缩放/增长/湮灭代数核心 + 上界实例化 (H^3 证明线)
    ├── H3MomentBound.lean    H^3 解析 H1 矩上界 (Cauchy-Schwarz, 积分形式) (H^3 证明线)
    ├── H1Isometry.lean       FTC 胶水 + H1 内积识别 + 正定核心 (H^3 证明线)
    ├── TransferOperator.lean K_c^{-r} x^k 传输算子闭式 + K_c 双射 (H^s 证明线)
    ├── HsOrthogonalSystems.lean 传输约化: Q_n=K_c^{-r} P_n/K_n 正交与次数约化 + Legendre 闭式 + aSeq (H^s 证明线)
    ├── BalancedPhase.lean    平衡相位三角闭式 (比值证明线)
    ├── TransferMatrix.lean   三段转移矩阵乘积/secular 方程 + 平凡不等式 (比值证明线)
    ├── ReflectionSymmetry.lean 固定 n 交替配置 J-共轭反射对称 F_n(pi-y)=F_n(y) (固定 n 比值线)
    ├── DensenessCriteria.lean   稠密性准则矩刻画: 稀疏基正交性 <-> 矩条件 (稠密性准则线)

    ├── ProjectionDensity.lean    DensBC O1 Theorem 1 抽象核: 连续满射把稠密集映到像中稠密集 + 正交投影密度 (DensBC O1)
    ├── DensBCEmpty.lean       DensBC O1 Lemma 6.1 抽象核: 空候选族闭包张成空间为 {0}, 稠密则 V={0} (DensBC O1)    ├── SymlineTensionRatio.lean  对称线张力比代数核心: P1/P2 比较引理 + FeEquiv/ρ 等价 + 张力比链 + gamma_0*/Lemma ys2 (间距线 n=1)

    ├── DensBC_O1_Scaffold.lean       DensBC O1 Theorems 2-5 + O1′ placeholder scaffold (-- SCAFFOLD, sorry)
    ├── LeftDefDensity_Scaffold.lean  left-definite density L1′-L5 + O1′LD scaffold (-- SCAFFOLD, sorry)
    ├── MinDirectionAudit_Scaffold.lean  min-direction audit scaffold (-- SCAFFOLD, sorry)
    ├── formalization_progress.md      scaffold register    ├── SymlineKeyLemma.lean     对称线 KEY LEMMA 代数核心: P1/P2 对数导数界 + W0 引理 + gamma_0(q) 单调 (间距线 n=1)
    ├── SymlineUniqueZero.lean    对称线 KEY LEMMA 装配核心: 唯一零点/符号结论 + 端点代数核心 (间距线 n=1)
    ├── ThirdOrder.lean       三阶递推一般框架: 固定点等价 + 精确降阶 (三阶递推线)
    ├── ThirdOrderClosedForms.lean  偶/奇闭式验证 + 固定点轨迹 + 比值恒等式 (三阶递推线)
    ├── ThirdOrderClassification.lean  Theorem 1 反向分类: 轨迹 => beta in {1,-1}/{3,1} (三阶递推线)
    ├── ThirdOrderMinimal.lean   变差常数/第三解: W/sumW/sInd + 定理 5 代数核心 + 定理 3 反向 (三阶递推线)
    ├── KreinDegenerateLimit.lean  Krein c->0 退化极限 (多项式级): radical/低模范数/发散/span 分解 (Krein 极限线)
    └── KreinHighGrowth.lean       Krein n>=4 一般 Θ 增长: aSeq 上下界 + ||K_n||^2 -> +infinity (Krein 极限线)
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
StabilityGrowth / Stability / MomentRecurrence / MomentBound / Completeness /
H3Completeness / H3MomentBound / H1Isometry / Transfer / HsOrthogonalSystems / BalancedPhase / ThirdOrder /
ThirdOrderClosedForms / ThirdOrderClassification / ThirdOrderMinimal / TransferMatrix /
ReflectionSymmetry / DensenessCriteria / ProjectionDensity / DensBCEmpty /  SymlineTensionRatio / SymlineKeyLemma / SymlineUniqueZero / KreinDegenerateLimit / KreinHighGrowth).
新文件保持同名命名空间, 更新 STATUS.md 状态矩阵.

## 规则

- 只形式化源文档中严格证明的结果; 数值证据/猜想不得作为定理声明.
- 每个文件头注明源文档与覆盖范围; 修改文件后重跑 verify + 更新 STATUS.md.
- 不引入 `sorry`/`admit`/`axiom`; 引入外部定理 (文献结果) 需在注释中登记来源与依赖.
- 泛型引理 (如 StabilityGrowth) 使用 mathlib v4.31 的非捆绑有序域组合
  `[Field K] [LinearOrder K] [IsStrictOrderedRing K]` (LinearOrderedField 已弃用).
- Windows 下避免 PowerShell `Set-Content -Encoding UTF8` 写入文件 (会加 BOM, lean 报
  "expected token"); 用 Python `write_text(..., encoding='utf-8')` 或
  `[System.IO.File]::WriteAllText(..., UTF8Encoding($false))`.

## Scaffolds

- Partial/structural results have `-- SCAFFOLD` Lean files with `sorry`; they are NOT formally verified.
- See `formalization_progress.md`.
