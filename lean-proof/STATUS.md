# lean-proof 形式化状态总表

> 结论先行: **没有全部形式化**. 截至目前 (2026-08-12, 会话 75) 已形式化 10 个文件, 覆盖
> H^2 完备性证明线 (矩跳跃 + 增长引理 + K_c 恒等式 + 缩放 + 矩上界 + 湮灭 + Weierstrass 收尾)
> 与比值上确界证明线的核心三角闭式. 其余 ~15 个已证定理 (H^3/H^s, 稳定性门槛, MW 重证, 间距线等)
> 仍未开始.

## 1. 已形式化并通过机器验证

| 文件 | 覆盖内容 | 源文档 | 验证 |
| --- | --- | --- | --- |
| `SL/MomentGrowth.lean` | 矩跳跃增长引理: 对 c>0, 递推 c u_j = A_j u_{j-1} - B_j u_{j-2} (A_j=2j(2j-1)+cj/(j-1), B_j=2j(2j-3)) 的解满足 u_j>0, u_j<=u_{j+1}, u_j >= (4/c)^(j-1) j! | `docs/SL_h2_completeness_proof.tex` (增长引理) | lake build 绿; sorry/axiom 0 |
| `SL/BalancedPhase.lean` | 平衡相位闭式核心: theta=arccos(s/(s+1)) 满足 sup 配置 secular 方程; arccos(-s/(s+1))=pi-theta; nu(R) 闭式; (0,pi) 内 secular 根恰为 theta/pi-theta; tan^2 phi=s(s+2) (Keller inf); lambda1/lambda2 相位恒等式 | `docs/SL_ratio_proof.tex` 第 3 节, `tools/balanced-phase.md` | lake build 绿; sorry/axiom 0 |
| `SL/KcPolynomial.lean` | K_c 作用在 H^2 多项式基的系数恒等式: K_c p_{2n}=c x^{2n}-A_n x^{2n-2}+B_n x^{2n-4}, 奇次同理; A_n-B_n=4n+cn/(n-1) | `docs/SL_h2_completeness_proof.tex` 引理 4.1 | lake build 绿; sorry/axiom 0 |
| `SL/StabilityGrowth.lean` | 定量增长引理 (一般系数): 对任意 `[Field K] [LinearOrder K] [IsStrictOrderedRing K]` (含 R, Q), B_m>=0 且 A_m-B_m>=c_0 时递推解 u_m 单调且 u_m >= prod_{k=2..m}(A_k-B_k)/c_0 = prod (1+eps_k), eps_k=(A_k-B_k-c_0)/c_0>=0 | `docs/SL_stability_moment_jump.tex` 定理 2.1 (定量增长引理) | lake build 绿; sorry/axiom 0; 审计见 audit_report.md (O1-O5) |
| `SL/MomentRecurrence.lean` | 线性泛函矩递推 + 缩放引理 (Q 上): M(K_c p_n)=0 => mu_0=mu_1=0, 偶/奇矩跳变递推 c mu_{2n}=A_n mu_{2n-2}-B_n mu_{2n-4} (奇次用 A'_n,B'_n), 且 mu_{2m}=mu_2 u_m, mu_{2m+1}=mu_3 u'_m (自由参数仅 mu_2/mu_3) | `docs/SL_h2_completeness_proof.tex` 第 3.2 节, `tools/left-definite-moment-recurrence.md` | lake build 绿; sorry/axiom 0; 审计见 audit_report.md (O6-O12) |
| `SL/MomentBound.lean` | L2 矩上界: |mu_k| <= ||g||_2 * sqrt(2/(2k+1)) (Cauchy-Schwarz 二次型技巧, C = integral x^(2k) > 0 无退化情形); integral_{-1}^1 x^(2k) = 2/(2k+1) | `docs/SL_h2_completeness_proof.tex` 3.3 节 (矩为零) | lake build 通过, sorry/axiom 0; 审计 audit_report.md (O13-O16) |
| `SL/Completeness.lean` | H^2 完备性收尾 (R 上): 线性泛函 M(p)=∫g·p, 偶/奇矩递推, mu_0=mu_1=0, 缩放 mu_{2m}=mu_2 u_m, sqrt(2/(4m+1))->0 湮灭 mu_2=mu_3=0, 全矩为零, Weierstrass 稠密 => ∫g^2=0 => g=0 a.e. | `docs/SL_h2_completeness_proof.tex` 3.3-3.4 节 | lake build 通过 (8566 jobs), sorry/axiom 0; 审计 audit_report.md (O17-O24) |
| `SL/TransferOperator.lean` | H^s 线第一步: 传输算子闭式. transferPoly c r k = K_c^{-r} x^k 的闭式 (系数 transferCoeff = binom(r+j-1,j) k!/(k-2j)!/c^(r+j)); KcR_transferPoly (K_c T_{r+1,k} = T_{r,k} 递推), transferPoly_zero, transferPoly_eq_split, coeff_transferPoly/natDegree_transferPoly, KcR_inj (c≠0 时 K_c 多项式空间单射), KcR_inv_left/right (K_c 双射, 逆 = KcR_inv), KcR_inv_iter_X_pow ((KcR_inv)^[r] X^k = T_{r,k}) | `docs/SL_hs_orthogonal_systems_proof.tex` 第 3 节 | lake build 绿 (8561 jobs), sorry/axiom 0 |
| `SL/H3Completeness.lean` | H^3 线代数核心 (R 上, 复用 Completeness 系数族): M_0=M_1=0, 偶/奇二阶跳变递推 c M_{2m}=A_m M_{2m-2}-B_m M_{2m-4}, 缩放 M_{2m}=M_2 u_m, 超阶乘增长 u_m >= (4/c)^(m-1) m! (StabilityGrowth.product_growth 统一覆盖两组系数), 湮灭 M_2=M_3=0, all_moments_zero_of_orthogonal (解析 H1 上界 |M_{2m}|<=C√m 为假设 hbdE/hbdO) | `docs/SL_h3_completeness_proof.tex` 第 3-6 节 | lake env lean 绿, sorry/axiom 0; 分析上界与等距同构未形式化 (登记于文件头与下文) |

机器验证证据: `run-manifest.json` (lean 4.31.0 / mathlib v4.31.0, 9 个 .lean 文件扫描,
sorry/admit/axiom 命中 0, lake build exit 0, 8566 jobs). 义务级审计: `audit_report.md` +
`verification.json` (会话 66-69, 单 agent 自审计, 24 项义务 O1-O24 全部 FAITHFUL 或
MINOR_PARAPHRASE, 无关键错误; 独立第三方复核未执行, 见审计报告独立性说明).

## 2. 完整状态矩阵 (源文档 -> 结果 -> 形式化状态)

源状态标注: 已证 = 项目文档声明严格证明; 部分 = 部分证明/结构结果; 数值 = 数值强猜想; 汇总 = 综述.
形式化状态: 未开始 / 部分 (列出已覆盖片段) / 完整.

| 源文档 | 主要结果 | 源状态 | 形式化状态 |
| --- | --- | --- | --- |
| SL_h2_completeness_proof.tex | {p_n} 在 H^2[-1,1] 解析完备 (等距 K_c + 矩跳跃 + 增长引理 + Weierstrass) | 已证 | 完整 (形式化线): 增长引理 (MomentGrowth/StabilityGrowth) + K_c 恒等式 (KcPolynomial) + 矩递推/缩放 (MomentRecurrence) + 矩上界 (MomentBound) + 湮灭/Weierstrass 收尾 (Completeness); 等距同构 K_c: H^2->L^2 与 L2 稠密扩展未形式化 (O16 记录缺口) |
| SL_h3_completeness_proof.tex | H^3 (及一切整数 s>=1) 完备性 | 已证 | 部分: 矩跳变+缩放+超阶乘增长+湮灭代数核心 (H3Completeness); 解析 H1 矩上界 (Cauchy-Schwarz) 与等距同构 K_c: H^3->H^1 未形式化 (all_moments_zero_of_orthogonal 以 hbdE/hbdO 假设声明) |
| SL_hs_orthogonal_systems_proof.tex | 整数阶 H^s 显式完备正交多项式系 + 闭式系数 (传输算子 K_c^{-1}) | 已证 | 部分: 传输算子闭式与 K_c^{-1} 迭代 (TransferOperator); 显式正交系统构造与 H^s 完备性未形式化 |
| SL_fractional_left_definite.tex | 实数阶 H^s (含分数窗 3/2<=s<2) 稀疏基解析完备 | 已证 | 未开始 |
| SL_denseness_criteria.tex | 一般稠密性准则: 一阶矩准则 + 临界指数 | 已证 | 未开始 |
| SL_stability_moment_jump.tex | 矩跳跃稳定性: 定量增长引理 (一般系数, B_m>=0 且 A_m-B_m>=c_0) | 已证 | 部分: 定量增长引理 + eps 形式 (StabilityGrowth); 稳定性定理 (超多项式门槛) 与尖锐性定理未形式化 |
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
- 会话 66 审计发现 F-001 (源文档非形式化缺陷): SL_stability_moment_jump.tex 定理 2.1
  陈述的假设 A_m>=B_m 弱于其证明实际使用的 A_m-B_m>=c_0; 形式化采用证明所需假设.
  2026-08-11 (会话 67) 已更正: 源文档定理 2.1/2.2 假设统一改为 B_m>=0 且
  A_m-B_m>=c_0, 与形式化一致 (F-001 RESOLVED).
- MomentRecurrence 在 Q 上形式化 (匹配 KcPolynomial 的精确有理系数); R 情形为同一
  代数的换基, 未单独形式化 (见 audit_report.md 独立性说明).
- 之前会话 31 在 D:\lean4\Projects\MyProject 有独立的增长引理/平衡相位形式化;
  仓库内 lean-proof 为当前规范副本.

## 4. 路线图 (按优先级)

1. [已完成, 会话 66] 把 MomentGrowth 推广到一般系数 (SL_stability_moment_jump.tex 的
   定量增长引理: B_m>=0 且 A_m-B_m>=c_0 时 u_m >= prod (A_k-B_k)/c_0) ->
   SL/StabilityGrowth.lean, 泛化到任意线性有序域, 覆盖偶/奇两组系数 (A'_m,B'_m 同为
   一般系数情形).
2. [已完成, 会话 66] H^2 矩递推: 由 KcPolynomial 的恒等式导出矩递推
   c mu_{2j} = A_j mu_{2j-2} - B_j mu_{2j-4} 及缩放引理 (自由参数 mu_2/mu_3) ->
   SL/MomentRecurrence.lean (Q 上, 线性泛函抽象).
3. [已完成: 会话 69] H^2 完备性形式化全链: StabilityGrowth + MomentRecurrence +
   MomentBound + Completeness (湮灭 + Weierstrass 收尾), 9 文件机器验证通过;
   剩余缺口: 等距同构 K_c: H^2 -> L^2 与 L2 稠密扩展 (O16), 稳定性门槛定理 Thm 2.2/2.3.
4. SL_stability_moment_jump.tex 稳定性定理 (sum min(eps_k,1) = omega(log m) => 超多项式)
   与尖锐性定理的形式化; 源文档定理 2.1/2.2 假设已更正为 A_m-B_m>=c_0 (F-001,
   2026-08-11 会话 67 RESOLVED; 形式化 StabilityGrowth.lean 无需改动).
5. MW 引理 1-2 与比值上确界定理由 BalancePhase 补全 (转移矩阵/谱论).
6. 间距线 (n=1 定理族, n>=2 开关/约化) 体量大且分析密集, 建议拆义务逐条形式化.
7. [已完成: 会话 70] H^s 显式正交系统线第一步: TransferOperator (K_c^{-r} x^k 闭式 + K_c 双射 + 迭代闭式, 9 文件机器验证通过). 剩余: 由传输算子构造 H^s 显式完备正交多项式系 (承接 Completeness 的矩方法/等距同构), 并处理 H^3 线 (SL_h3_completeness_proof.tex).
8. [部分: 会话 75] H^3 线: H3Completeness.lean (矩跳变/缩放/增长/湮灭代数核心, 10 文件绿). 剩余: 解析 H1 矩上界 |M_{2m}|<=C√m 与等距同构 K_c: H^3->H^1 (然后一切整数 s>=1 由归纳传输).
