# Sturm-Liouville 边值问题研究 (BVE research)

English: [README_EN.md](README_EN.md)

Sturm-Liouville (SL) 边值问题的前沿数学研究项目, 覆盖两条主线:

1. **特征函数系/多项式系的完备性**: SL 边值问题的解在多大的 Hilbert 空间 (左定空间) 中等价于该空间内的所有正交函数系. 基准论文: Littlejohn-Quintero-Roba, *Krein-Sobolev Orthogonal Polynomials* (Springer 2025, DOI 10.1007/978-3-031-90135-5_7).
2. **特征值间距与比值的最优界**: 对加权 Dirichlet 问题 $-y'' = \lambda \rho y, \quad 0 < a \le \rho \le A$ (可测盒类), 优化相邻谱隙 $D_n = \lambda_{n+1} - \lambda_n$ 与比值 $\lambda_{n+1}/\lambda_n$.

严格性约定: 严格证明与数值证据显式区分, 未完成严格证明的断言不标为 "已解决".

## 主要结果

### 严格证明 (已证, 详见 docs/)

| 结果 | 来源 | 状态 |
| --- | --- | --- |
| $\sup_{n,\rho} \lambda_{n+1}/\lambda_n = \nu(R)$ 闭式 (平衡相位法) | `docs/SL_ratio_proof.tex` | 已证 |
| $\inf_{n,\rho} \lambda_{n+1}/\lambda_n = 1$ (Weyl 渐近, 下确界不达到) | `docs/SL_inf_ratio_proof.tex` | 已证 |
| Mahar-Willner 引理 1-2 独立重证 (周期延拓 + 零点截断) | `docs/SL_mw_lemma_reproof.tex` | 已证 |
| 移位 Krein 算子 $c \to 0$ 退化极限的结构稳定性 | `docs/SL_krein_c0_limit.tex` | 已证 |
| $\{p_n\}$ 在 $H^2$ 解析完备 (矩跳跃判据 + 增长引理) | `docs/SL_h2_completeness_proof.tex` | 已证 |
| $\{p_n\}$ 在一切整数左定空间 $H^s$ ($s \ge 1$) 完备 | `docs/SL_h3_completeness_proof.tex` | 已证 |
| $n=1$ 间距极端值: SUP/INF 由 $[1,R,1]$ / $[R,1,R]$ 达到 | `docs/SL_gap_n1_proof.tex` 等 | 已证 |
| $n \ge 2$ 间距: 有限块约化 (至多 $2n+1$ 块) + 精确 $2n$ 开关定理 | `docs/SL_gap_nge2_finite_reduction_proof.tex`, `SL_gap_nge2_exact_2n_switches_proof.tex` | 已证 |
| $n \ge 2$ 间距 (局部): $R=1$ 反射对称 + $R \to 1$ 局部唯一性; 全局唯一性依赖 $(G1')/(G2)$ (开放) | `docs/SL_gap_nge2_symmetry_local_proof.tex` | 已证 (局部) |

### 部分证明 / 数值强猜想 / 开放问题

- 固定 $n$ 上确界: 对称相位结构已证, $n=1,2$ 闭式; 全局极值性与 $2n$ 根计数未证 (`docs/SL_fixed_n_supremum.tex`).
- $n \ge 2$ 间距全局对称性与块数最小性: $R=1$ 与 $R \to 1$ 局部定理已证, 全局唯一性依赖开放条件 $(G1')/(G2)$, 其余为数值强猜想 (`docs/SL_gap_nge2_symmetry_local_proof.tex`).
- 权威开放问题清单: `docs/SL_spectral_topics_summary.tex` §5.
- 文献检索: 未检索到与 $n \ge 2$ 定理直接等价的已发表结果; 项目不声称首创, Willner-Mahar 1979 等早期文献为既有工作风险.

## 目前关注的未解决问题

权威清单: `docs/SL_spectral_topics_summary.tex` §5 (含各问题的进展与失败路线).

1. **相邻间距极端值结构收尾** ($n\ge2$): 开关位置/块长闭式, 反射对称性与唯一性 (依赖 (G1$'$) $\det K>0$ 的严格证明), 最优值 $\max/\min D_n$ 闭式或锐界, $n=1$ 证书重放内核的形式化.
2. **一般边界/势类推广**: Neumann 情形 (Li-Ao 线), 非负势 $q\ge0$ (Gan-Zheng-Li-Shao 线), 变号权重的比值最优常数与极值结构.
3. **MDE 极值测度统一理论**: Neumann 间距与最大间距的极值测度结构, 及其与节点界 (Chu-Guo-Meng-Zhang) 的统一.
4. **左定空间稠密性一般判据**: 受一般边界条件约束的 Hilbert 空间中多项式稠密的充要条件.
5. **p-Laplacian 等非线性推广**: Wen-Zhou 奇异测度技巧的适用范围.
6. **矩量可表示性的一般刻画**: 一般 Hilbert 空间的闭式判据.
7. **跳变稳定性门槛线分类**: 门槛线上系数族 ($\sum\sim\log m$) 未完全分类; 变系数算子高阶矩跳跃替代机制 (S3).
8. **三阶递推理论**: 最小解 $h^*$ 闭式与渐近常数 $K$, 盒式归纳退化配置排除, 一般系数族积分解分类.
9. **固定 $n$ 上确界收尾**: 全局极值性 (Keller 型归约), $2n$-根计数, $\Lambda_n^{\sup}(R)\downarrow c_\infty(R)$.
## Lean 4 形式化验证 (lean-proof/)

机器可核验的证明工程 (Lean 4.31.0 + mathlib v4.31.0). 权威状态: `lean-proof/STATUS.md` (状态矩阵) + `lean-proof/audit_report.md`/`verification.json` (义务级审计, O1-O24). 当前机器验证: 26 个 `SL/*.lean` 文件, `sorry/admit/axiom` 命中 0, `lake build` exit 0, 8584 jobs.

**已完成 (按证明线)**

- 完备性线: $H^2$ 全链 (StabilityGrowth/MomentRecurrence/MomentBound/Completeness), $H^3$ 代数核心 (H3Completeness/H3MomentBound/H1Isometry), $H^s$ 传输约化 (TransferOperator/HsOrthogonalSystems), 稠密性矩刻画 (DensenessCriteria).
- 比值线: 平衡相位闭式 (BalancedPhase), 三段转移矩阵/secular 方程 (TransferMatrix), 固定 $n$ 交替配置反射对称 (ReflectionSymmetry).
- 其他线: 稳定性门槛核心 (Stability), 三阶递推线 (ThirdOrder/ThirdOrderClosedForms/ThirdOrderClassification/ThirdOrderMinimal), Krein $c\to0$ 多项式级 (KreinDegenerateLimit/KreinHighGrowth), 间距 $n=1$ 对称线代数核心 (SymlineTensionRatio, 含 $\gamma_0^*$/Lemma ys2 证书自由形式化; SymlineKeyLemma 补 P1/P2 对数导数界与 W0 引理; SymlineUniqueZero 补 4.4 节 KEY LEMMA 装配核心 (唯一零点/符号结论, 端点符号/相位分支/导数恒等式为分析钩子)).

**未完成 (按缺口类型, 与 STATUS.md 一致)**

- 谱论/泛函分析依赖: 等距同构 $K_c\colon H^2\to L^2$ (O16) 与 $H^3\to H^1$, $H^s$ 算符级等距与完备性, 稠密性收尾 ($w=0$), Krein 商空间级 ($H^1/W \cong L^2_0$), Weyl 渐近 (inf 比值线), MW 引理重证, 转移矩阵到特征值的谱论连接.
- 已证但未开始: $n=1$ 间距线 (gap_n1_proof/well_rigidity/O3a/inf_limit; symline 代数核心已部分形式化, 见 SymlineKeyLemma/SymlineUniqueZero) 与 $n\ge2$ 开关/约化文档, 分数阶 $H^s$ 稀疏基完备.
- 源中为数值/未严格 (不形式化): $n\ge2$ 间距全局极值性, 固定 $n$ 上确界 $2n$ 根计数, 三阶递推三解 Casoratian 非零.
- 假设接入: HsOrthogonalSystems 的 Legendre/Krein-Sobolev 经典正交性 (文献事实, 未形式化).

## 目录结构

| 目录 | 内容 |
| --- | --- |
| `docs/` | 研究文档与完整证明 (tex/pdf) |
| `lean-proof/` | Lean 4 形式化工程 (状态矩阵/审计/机器验证) |
| `scripts/` | 数值审计与复现脚本 (Python, EVIDENCE 级, 不构成证明) |
| `tools/` | 数学工具库 (Obsidian 兼容 Markdown) |
| `papers/` | 参考文献全文 (版权文献仅个人研究使用) |
| `research_cache/`, `images/`, `misc/` | 检索缓存, 扫描图, 失败/测试产物 |
| `runs/` | rigorous-open-math-research 运行目录 (契约/台账/审计) |
| `state/`, `index/`, `agenda/`, `knowledge/`, `literature/`, `reports/`, `archive/` | 项目管理层 (manage-math-research-program) |
| `AGENTS.md`, `PROJECT.md` | 项目规则 + 会话记录; MRP 项目入口 |

## 构建与复现

```text
# Lean 形式化 (lean-proof/)
lake build                                     # 构建整个包 (首跑需编译 mathlib)
lake env lean SL/<File>.lean                   # 单文件检查
python <lean-verify>/scripts/verify_lean_project.py --project lean-proof --build
                                               # sorry/axiom 扫描 + 构建 (刷新 run-manifest.json)

# 文档 (docs/, 需 xelatex)
xelatex SL_<name>.tex

# 数值脚本 (scripts/, Python 3.10+, numpy/scipy)
python scripts/<name>.py                       # 各脚本头部注明用途与精度
```

## 仓库结构

- 父仓库: `Zhongshan-Big-Jun/Sturm-Liouville-theory-research` (public)
- 个人 fork: `xsoc1/Sturm-Liouville-theory-research` (public)
- 同步: 内容推送到父仓库后同步 fork 到同一提交 (项目 `project.json` 配置 `git_sync.push_order = ["origin", "fork"]`, 由 manage skill 的 `sync_remotes.py` 执行).

## 工作方法

- 进入项目先读 `AGENTS.md` (代码规则, 严格性标注, 会话记录).
- 数学研究: `$rigorous-open-math-research`; 项目管理: `$manage-math-research-program`; Lean 验证: `$lean-verify`; 全流程编排: `$math-research-workflow` 插件.
- 任何问题如实回答; 数值证据不得作为结果呈现; 未完成严格证明的断言不得称为 "已解决".
