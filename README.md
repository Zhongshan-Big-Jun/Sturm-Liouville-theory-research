# Sturm-Liouville 边值问题研究 (BVE research)

English: [README_EN.md](README_EN.md)

Sturm-Liouville (SL) 边值问题的前沿数学研究项目, 覆盖两条主线:

1. **特征函数系/多项式系的完备性**: SL 边值问题的解在多大的 Hilbert 空间 (左定空间)
   中等价于该空间内的所有正交函数系. 基准论文: Littlejohn-Quintero-Roba,
   *Krein-Sobolev Orthogonal Polynomials* (Springer 2025, DOI 10.1007/978-3-031-90135-5_7).
2. **特征值间距与比值的最优界**: 对加权 Dirichlet 问题
   $$
   -y'' = \lambda \rho y, \qquad 0 < a \le \rho \le A \ \text{(可测盒类)},
   $$
   优化相邻谱隙 $D_n = \lambda_{n+1} - \lambda_n$ 与比值 $\lambda_{n+1}/\lambda_n$.

所有研究结论遵循严格性标注: 严格证明与数值证据显式区分, 未完成严格证明的断言不标为 "已解决".

## 主要结果

### 严格证明 (已证, 详见 docs/)

| 结果 | 来源 | 状态 |
| --- | --- | --- |
| $\sup_{n,\rho} \lambda_{n+1}/\lambda_n = \nu(R)$ 闭式 (平衡相位法, 三步证明) | `docs/SL_ratio_proof.tex` | 已证 |
| $\inf_{n,\rho} \lambda_{n+1}/\lambda_n = 1$ (Weyl 渐近, 下确界不达到) | `docs/SL_inf_ratio_proof.tex` | 已证 |
| Mahar-Willner 引理 1-2 独立重证 (周期延拓 + 零点截断) | `docs/SL_mw_lemma_reproof.tex` | 已证 |
| 移位 Krein 算子 $c \to 0$ 退化极限的结构稳定性 | `docs/SL_krein_c0_limit.tex` | 已证 |
| $\{p_n\}$ 在第二左定空间 $H^2$ 解析完备 (矩跳跃判据 + 增长引理) | `docs/SL_h2_completeness_proof.tex` | 已证 |
| $\{p_n\}$ 在一切整数左定空间 $H^s$ ($s \ge 1$) 完备 | `docs/SL_h3_completeness_proof.tex` | 已证 |
| $n=1$ 相邻间距极端值: SUP/INF 由 $[1,R,1]$ / $[R,1,R]$ 达到 (相位比刚性, 义务 O1/O2/O3a/O3b 闭合) | `docs/SL_gap_n1_proof.tex` 等 | 已证 |
| $n \ge 2$ 相邻间距: 有限块约化 (极值子 bang-bang, 至多 $2n+1$ 块) + 精确 $2n$ 开关定理 (合并相邻同值块后恰 $2n$ 个有效内部开关) | `docs/SL_gap_nge2_finite_reduction_proof.tex`, `SL_gap_nge2_exact_2n_switches_proof.tex` | 已证 |
| $n \ge 2$ 相邻间距 (局部): $R=1$ 一般 $n$ 极值子反射对称 (Wronskian 直接公式, $2n$ 个简单零点) + $R \to 1$ 局部唯一性与对称性; 全局唯一性依赖拓扑度条件 $(G1')/(G2)$ (开放) | `docs/SL_gap_nge2_symmetry_local_proof.tex` | 已证 (局部) |

### 部分证明 / 数值强猜想 / 开放问题 (如实标注)

- 固定 $n$ 上确界: 交替配置对称相位结构已证, $n=1,2$ 闭式; 全局极值性与 $2n$ 根计数未证
  (`docs/SL_fixed_n_supremum.tex`, 数值: `docs/SL_ratio_summary.tex`).
- $n \ge 2$ 间距极端值的全局对称性与块数最小性: $R=1$ 与 $R \to 1$ 局部定理已严格证明 (见上表); 全局唯一性依赖开放条件 $(G1')/(G2)$ (`docs/SL_gap_nge2_symmetry_local_proof.tex` 第 5 节), 其余为数值强猜想.
- 完整开放问题清单 (权威): `docs/SL_spectral_topics_summary.tex` §5.
- 文献检索结论: 未检索到与 $n \ge 2$ 定理直接等价的已发表结果; 项目不声称首创,
  Willner-Mahar 1979 等早期文献为既有工作风险 (各证明文档中有核验记录).

## Lean 4 形式化验证 (lean-proof/)

研究结果的形式化验证工程 (Lean 4.31.0 + mathlib v4.31.0), 作为正确性的机器可核验证明材料:

- **状态矩阵**: `lean-proof/STATUS.md` (每个已证结果 -> 形式化状态, 诚实标注未完成部分).
- **机器验证**: `lean-proof/run-manifest.json` (16 个 SL/ 下 .lean 文件扫描,
  sorry/admit/axiom 命中 0, `lake build` exit 0, 8574 jobs).
- **义务级审计**: `lean-proof/audit_report.md` + `verification.json` (24 项义务 O1-O24,
  裁决 FORMALLY_VERIFIED).
- **已完成**:
  - $H^2$ 完备性证明线完整: StabilityGrowth / MomentRecurrence / MomentBound / Completeness
    (增长引理, 矩递推/缩放, $L^2$ 矩上界, 湮灭 + Weierstrass 收尾).
  - $H^3$ 线: H3Completeness (矩跳变/缩放/增长/湮灭代数核心) + H3MomentBound (解析 $H^1$ 矩上界,
    Cauchy-Schwarz, 已接入 hbdE/hbdO 闭合矩全零) + H1Isometry (FTC 胶水 $\Delta w = \int w\,dx$,
    $H^1$ 内积与 h1MomentFunctional 的识别, 正交传输, 正定核心 $N_1(w) = 0 \Rightarrow w = 0$ a.e.).
  - $H^s$ 线第一步: TransferOperator ($K_c^{-r} x^k$ 传输算子闭式 + $K_c$ 双射).
  - 稳定性门槛线核心: Stability (Thm 2.2 泛函核心 + Thm 2.3 尖锐性级数).
  - 比值上确界证明线核心三角闭式: BalancedPhase.
  - 三阶递推线: ThirdOrder (固定点等价 + 精确降阶) + ThirdOrderClosedForms
    (偶/奇闭式验证 + 固定点轨迹 + 比值恒等式 $1/(2n+7)$, $3/(2n+9)$) +
    ThirdOrderClassification (Theorem 1 反向: 轨迹 => $\beta \in \{1,-1\}/\{3,1\}$).
- **未完成 (已登记)**: $H^3$ 算符级等距同构 $K_c\colon H^3 \to H^1$ (双射/谱, 需谱论) 与多项式在 $H^1$
  稠密性; $H^s$ 显式完备正交多项式系构造; MW 引理重证; 间距线 ($n=1$ 定理族, $n \ge 2$ 开关/约化);
  三阶递推最小解唯一性; Krein $c \to 0$ 极限; 分数阶 $H^s$ 与稠密性准则.

## 目录结构

| 目录 | 内容 |
| --- | --- |
| `docs/` | 研究文档与完整证明 (tex/pdf, 含证明包、研究总结与综述) |
| `lean-proof/` | Lean 4 形式化验证工程 (状态矩阵/审计/机器验证) |
| `scripts/` | 数值审计、复现与探索脚本 (Python, EVIDENCE 级, 不构成证明) |
| `tools/` | 数学工具库 (Obsidian 兼容 Markdown: 解析/适用范围/验证状态) |
| `papers/` | 参考文献全文 (含版权文献, 仅个人研究使用) |
| `research_cache/` | 文献检索缓存与元数据 |
| `images/` | 扫描页与测试图 |
| `misc/` | 失败/测试产物、调试工件与归档数据 |
| `runs/` | rigorous-open-math-research 运行目录 (契约/台账/审计, 按 RUN_ID) |
| `state/`, `index/`, `agenda/`, `knowledge/`, `literature/`, `reports/`, `archive/` | 项目管理层 (manage-math-research-program): 状态/索引/议程/知识/文献/报告/归档 |
| `AGENTS.md` | 项目规则 + 逐会话工作记录 (进入项目先读) |
| `PROJECT.md` | MRP 项目入口 (所有权与恢复指引) |

## 构建与复现

```text
# Lean 形式化 (lean-proof/)
lake build                                     # 构建整个包 (首跑需编译 mathlib)
lake env lean SL/<File>.lean                   # 单文件检查
python <lean-verify>/scripts/verify_lean_project.py --project lean-proof --build
                                               # sorry/axiom 扫描 + 构建 (刷新 run-manifest.json)

# 文档 (docs/, 需 xelatex)
xelatex SL_<name>.tex                          # 编译各 tex 文档

# 数值脚本 (scripts/, Python 3.10+, 依赖 numpy/scipy)
python scripts/<name>.py                       # 各脚本头部注明用途与精度
```

## 仓库结构

- 父类仓库: `Zhongshan-Big-Jun/Sturm-Liouville-theory-research` (组织, public)
- 个人 fork: `xsoc1/Sturm-Liouville-theory-research` (个人主页, public)
- 同步方向: 内容推送到父类后, 用 GitHub 的 Sync fork 将 fork 跟进到同一提交.

## 工作方法

- 进入项目先读 `AGENTS.md` (代码规则、严格性标注规则、会话记录).
- 数学研究调用 `$rigorous-open-math-research`; 项目管理调用 `$manage-math-research-program`;
  Lean 形式化验证调用 `$lean-verify`; 全流程编排 (管理-研究-验证) 调用
  `$math-research-workflow` 插件.
- 任何问题如实回答; 数值证据不得作为结果呈现; 未完成严格证明的断言不得称为 "已解决".
