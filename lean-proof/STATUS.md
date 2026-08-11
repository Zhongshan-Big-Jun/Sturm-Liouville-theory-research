# lean-proof 形式化状态总表

> 结论先行: **没有全部形式化**. 截至目前 (2026-08-11) 只形式化了项目已证结果中的极小部分
> (3 个文件, 覆盖 2 条证明线的核心代数/三角片段). 其余 ~15 个已证定理均未开始.

## 1. 已形式化并通过机器验证

| 文件 | 覆盖内容 | 源文档 | 验证 |
| --- | --- | --- | --- |
| `SL/MomentGrowth.lean` | 矩跳跃增长引理: 对 c>0, 递推 c u_j = A_j u_{j-1} - B_j u_{j-2} (A_j=2j(2j-1)+cj/(j-1), B_j=2j(2j-3)) 的解满足 u_j>0, u_j<=u_{j+1}, u_j >= (4/c)^(j-1) j! | `docs/SL_h2_completeness_proof.tex` (增长引理) | lake build 绿; sorry/axiom 0 |
| `SL/BalancedPhase.lean` | 平衡相位闭式核心: theta=arccos(s/(s+1)) 满足 sup 配置 secular 方程; arccos(-s/(s+1))=pi-theta; nu(R) 闭式; (0,pi) 内 secular 根恰为 theta/pi-theta; tan^2 phi=s(s+2) (Keller inf); lambda1/lambda2 相位恒等式 | `docs/SL_ratio_proof.tex` 第 3 节, `tools/balanced-phase.md` | lake build 绿; sorry/axiom 0 |
| `SL/KcPolynomial.lean` | K_c 作用在 H^2 多项式基的系数恒等式: K_c p_{2n}=c x^{2n}-A_n x^{2n-2}+B_n x^{2n-4}, 奇次同理; A_n-B_n=4n+cn/(n-1) | `docs/SL_h2_completeness_proof.tex` 引理 4.1 | lake build 绿; sorry/axiom 0 |

机器验证证据: `run-manifest.json` (lean 4.31.0 / mathlib v4.31.0, 5 个 .lean 文件扫描,
sorry/admit/axiom 命中 0, lake build exit 0).

## 2. 完整状态矩阵 (源文档 -> 结果 -> 形式化状态)

源状态标注: 已证 = 项目文档声明严格证明; 部分 = 部分证明/结构结果; 数值 = 数值强猜想; 汇总 = 综述.
形式化状态: 未开始 / 部分 (列出已覆盖片段) / 完整.

| 源文档 | 主要结果 | 源状态 | 形式化状态 |
| --- | --- | --- | --- |
| SL_h2_completeness_proof.tex | {p_n} 在 H^2[-1,1] 解析完备 (等距 K_c + 矩跳跃 + 增长引理 + Weierstrass) | 已证 | 部分: 增长引理 (MomentGrowth) + K_c 恒等式 (KcPolynomial); 等距同构/矩递推/完备性收尾未形式化 |
| SL_h3_completeness_proof.tex | H^3 (及一切整数 s>=1) 完备性 | 已证 | 未开始 |
| SL_hs_orthogonal_systems_proof.tex | 整数阶 H^s 显式完备正交多项式系 + 闭式系数 (传输算子 K_c^{-1}) | 已证 | 未开始 |
| SL_fractional_left_definite.tex | 实数阶 H^s (含分数窗 3/2<=s<2) 稀疏基解析完备 | 已证 | 未开始 |
| SL_denseness_criteria.tex | 一般稠密性准则: 一阶矩准则 + 临界指数 | 已证 | 未开始 |
| SL_stability_moment_jump.tex | 矩跳跃稳定性: 定量增长引理 (一般系数, B_m>=0 且 A_m-B_m>=c_0) | 已证 | 未开始 (直接目标: 把 MomentGrowth 推广到一般系数) |
| SL_third_order_recurrence_theory.tex | 三阶递推一般理论: 积分解分类/精确降阶/最小解 | 已证 | 未开始 |
| SL_krein_c0_limit.tex | 移位 Krein 算子 c->0 退化极限的结构稳定性 | 已证 | 未开始 |
| SL_ratio_proof.tex | sup_{n,rho} lambda_{n+1}/lambda_n = nu(R) (平衡相位 + MW 引理 2) | 已证 | 部分: BalancedPhase (三角闭式核心); 转移矩阵/secar 推导/平凡不等式/MW 引理未形式化 |
| SL_inf_ratio_proof.tex | inf_{n,rho} lambda_{n+1}/lambda_n = 1 (Weyl 渐近) | 已证 | 未开始 (需 Weyl 渐近, 解析重) |
| SL_mw_lemma_reproof.tex | Mahar-Willner 引理 1-2 独立重证 (周期延拓 + 零点截断) | 已证 | 未开始 |
| SL_fixed_n_supremum.tex | 固定 n 上确界: 交替配置平衡相位结构, n=1,2 闭式 | 部分 (全局极值未证) | 未开始 |
| SL_gap_extremals.tex | 相邻间距极端值 (SUP/INF 配置表) | 数值强猜想 (n>=2 未严格) | 未开始 (源未严格证明, 不宣称形式化) |
| SL_gap_n1_proof.tex | n=1 间距极端值定理 | 已证 | 未开始 |
| SL_gap_n1_symline_proof.tex | 缺口 (a): 阱族对称线唯一零点 + D 单峰 | 已证 | 未开始 |
| SL_gap_n1_well_rigidity_allR_proof.tex / _R32.tex | 缺口 (b): 阱族全 R (及 1<R<=3/2) 相位刚性 | 已证 | 未开始 |
| SL_gap_n1_O3a_phase_rigidity_proof.tex | O3a: 势垒族 sign-consistent good root 唯一性 | 已证 | 未开始 |
| SL_gap_n1_inf_limit_proof.tex | R->inf 极限定理 A | 已证 | 未开始 |
| SL_gap_nge2_exact_2n_switches_proof.tex | 相邻谱隙极值子精确 2n 开关定理 | 已证 | 未开始 |
| SL_gap_nge2_finite_reduction_proof.tex | n>=2 有限块约化 | 已证 | 未开始 |
| SL_spectral_topics_summary.tex 等 3 份 summary | 综述/研究总结 | 汇总 | 不适用 |

## 3. 诚实说明

- 上表"源状态"以项目文档与 AGENTS.md 会话记录为准; 若某文档在源中即标注数值/开放,
  此处不宣称形式化 (形式化不能把未证内容变成定理).
- "已形式化"只表示 Lean 内核接受证明, 不代表源文档中引用的文献定理 (如 MW 引理 2,
  Weyl 渐近) 本身已被形式化; 完整定理形式化需把这些外部依赖一并处理.
- 之前会话 31 在 D:\lean4\Projects\MyProject 有独立的增长引理/平衡相位形式化;
  仓库内 lean-proof 为当前规范副本.

## 4. 路线图 (按优先级)

1. 把 MomentGrowth 推广到一般系数 (SL_stability_moment_jump.tex 的定量增长引理:
   B_m>=0 且 A_m-B_m>=c_0 时 u_m >= prod (A_k-B_k)/c_0), 同时覆盖偶/奇两组系数.
2. H^2 矩递推: 由 KcPolynomial 的恒等式导出矩递推 c mu_{2j} = A_j mu_{2j-2} - B_j mu_{2j-4}
   (需 L^2 内积/矩的形式化).
3. H^2 完备性全定理 (等距同构 + 谱 + Weierstrass 稠密).
4. MW 引理 1-2 与比值上确界定理由 BalancePhase 补全 (转移矩阵/谱论).
5. 间距线 (n=1 定理族, n>=2 开关/约化) 体量大且分析密集, 建议拆义务逐条形式化.
