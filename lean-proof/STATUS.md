# lean-proof 形式化状态总表

> 结论先行: **没有全部形式化**. 截至目前 (2026-08-13, 会话 91 续作) 已形式化 21 个文件, 覆盖
> H^2 完备性证明线 (矩跳跃 + 增长引理 + K_c 恒等式 + 缩放 + 矩上界 + 湮灭 + Weierstrass 收尾),
> H^3 线代数核心、解析 H1 矩上界与 FTC 胶水 (H1 内积识别/正定核心), 比值上确界证明线的核心三角闭式,
> 稳定性门槛线 (Thm 2.2 泛函核心 + Thm 2.3 尖锐性级数),
> 以及三阶递推线 (一般框架/比值映射等价/精确降阶 + 偶奇族闭式/固定点轨迹/比值恒等式 + 积分解分类方向 + 变差常数/第三解),
> H^s 显式正交系的传输约化 (Q_n=K_c^{-r} P_n/K_n 的正交/次数约化 + Legendre 闭式 + aSeq 递推), Krein c->0 退化极限的多项式级与 n>=4 一般 Θ 增长, 以及比值证明线的平衡相位三角闭式与三段转移矩阵/secular 方程 (sup/inf Dirichlet 条件, 平凡不等式 λ_{n+1}<=λ_{2n}).
> 其余已证定理 (H^3 算符级等距同构 K_c: H^3->H^1, H^s 显式正交系的算符级等距与完备性, MW 重证, 间距线等) 仍有待形式化.

## 1. 已形式化并通过机器验证

| 文件 | 覆盖内容 | 源文档 | 验证 |
| --- | --- | --- | --- |
| `SL/MomentGrowth.lean` | 矩跳跃增长引理: 对 c>0, 递推 c u_j = A_j u_{j-1} - B_j u_{j-2} (A_j=2j(2j-1)+cj/(j-1), B_j=2j(2j-3)) 的解满足 u_j>0, u_j<=u_{j+1}, u_j >= (4/c)^(j-1) j! | `docs/SL_h2_completeness_proof.tex` (增长引理) | lake build 绿; sorry/axiom 0 |
| `SL/BalancedPhase.lean` | 平衡相位闭式核心: theta=arccos(s/(s+1)) 满足 sup 配置 secular 方程; arccos(-s/(s+1))=pi-theta; nu(R) 闭式; (0,pi) 内 secular 根恰为 theta/pi-theta; tan^2 phi=s(s+2) (Keller inf); lambda1/lambda2 相位恒等式 | `docs/SL_ratio_proof.tex` 第 3 节, `tools/balanced-phase.md` | lake build 绿; sorry/axiom 0 |
| `SL/TransferMatrix.lean` | 比值证明线转移矩阵/secular 核心: supM1/supM2/supM3 ([1,R,1] 三段矩阵), infM1/infM2/infM3 ([R,1,R] 三段矩阵), sup/inf top-right 乘积闭式与 Dirichlet 条件等价, theta/pi-theta/phi 满足矩阵 Dirichlet 条件, 平凡不等式 λ_{n+1}<=λ_{2n} 的严格单调序列版本 | `docs/SL_ratio_proof.tex` 第 1-3 节 | lake build 绿; sorry/axiom 0; 转移矩阵到特征值的谱论连接未形式化 |
| `SL/KcPolynomial.lean` | K_c 作用在 H^2 多项式基的系数恒等式: K_c p_{2n}=c x^{2n}-A_n x^{2n-2}+B_n x^{2n-4}, 奇次同理; A_n-B_n=4n+cn/(n-1) | `docs/SL_h2_completeness_proof.tex` 引理 4.1 | lake build 绿; sorry/axiom 0 |
| `SL/StabilityGrowth.lean` | 定量增长引理 (一般系数): 对任意 `[Field K] [LinearOrder K] [IsStrictOrderedRing K]` (含 R, Q), B_m>=0 且 A_m-B_m>=c_0 时递推解 u_m 单调且 u_m >= prod_{k=2..m}(A_k-B_k)/c_0 = prod (1+eps_k), eps_k=(A_k-B_k-c_0)/c_0>=0 | `docs/SL_stability_moment_jump.tex` 定理 2.1 (定量增长引理) | lake build 绿; sorry/axiom 0; 审计见 audit_report.md (O1-O5) |
| `SL/MomentRecurrence.lean` | 线性泛函矩递推 + 缩放引理 (Q 上): M(K_c p_n)=0 => mu_0=mu_1=0, 偶/奇矩跳变递推 c mu_{2n}=A_n mu_{2n-2}-B_n mu_{2n-4} (奇次用 A'_n,B'_n), 且 mu_{2m}=mu_2 u_m, mu_{2m+1}=mu_3 u'_m (自由参数仅 mu_2/mu_3) | `docs/SL_h2_completeness_proof.tex` 第 3.2 节, `tools/left-definite-moment-recurrence.md` | lake build 绿; sorry/axiom 0; 审计见 audit_report.md (O6-O12) |
| `SL/MomentBound.lean` | L2 矩上界: |mu_k| <= ||g||_2 * sqrt(2/(2k+1)) (Cauchy-Schwarz 二次型技巧, C = integral x^(2k) > 0 无退化情形); integral_{-1}^1 x^(2k) = 2/(2k+1) | `docs/SL_h2_completeness_proof.tex` 3.3 节 (矩为零) | lake build 通过, sorry/axiom 0; 审计 audit_report.md (O13-O16) |
| `SL/Completeness.lean` | H^2 完备性收尾 (R 上): 线性泛函 M(p)=∫g·p, 偶/奇矩递推, mu_0=mu_1=0, 缩放 mu_{2m}=mu_2 u_m, sqrt(2/(4m+1))->0 湮灭 mu_2=mu_3=0, 全矩为零, Weierstrass 稠密 => ∫g^2=0 => g=0 a.e. | `docs/SL_h2_completeness_proof.tex` 3.3-3.4 节 | lake build 通过 (8566 jobs), sorry/axiom 0; 审计 audit_report.md (O17-O24) |
| `SL/TransferOperator.lean` | H^s 线第一步: 传输算子闭式. transferPoly c r k = K_c^{-r} x^k 的闭式 (系数 transferCoeff = binom(r+j-1,j) k!/(k-2j)!/c^(r+j)); KcR_transferPoly (K_c T_{r+1,k} = T_{r,k} 递推), transferPoly_zero, transferPoly_eq_split, coeff_transferPoly/natDegree_transferPoly, KcR_inj (c≠0 时 K_c 多项式空间单射), KcR_inv_left/right (K_c 双射, 逆 = KcR_inv), KcR_inv_iter_X_pow ((KcR_inv)^[r] X^k = T_{r,k}) | `docs/SL_hs_orthogonal_systems_proof.tex` 第 3 节 | lake build 绿 (8561 jobs), sorry/axiom 0 |
| `SL/HsOrthogonalSystems.lean` | H^s 线第二步: 传输约化 (R 上, 多项式级). Legendre 闭式 legendreClosed (源 (11)) 与 natDegree_legendreClosed (deg P_n = n); Krein-Sobolev 系数序列 aSeq (源 (9), 基值 a_0..a_3=1, a_4=1+15/c); 传输机制 KcR_iter_inv_iter (K_c^r K_c^{-r}=id, Function.LeftInverse.iterate), KcR_inv_zero/KcR_inv_iter_zero, natDegree_KcR/KcR_inv/iter_KcR_inv (deg 保持); 传输配对 hsPairingEven/hsPairingOdd (H^{2r}/H^{2r+1} 配对) 与 qnEven/qnOdd (Q_n^{(2r)}=K_c^{-r} P_n, Q_n^{(2r+1)}=K_c^{-r} K_n); 约化定理 hs_even_pairing/hs_odd_pairing (正交性归约为经典系), hs_even_deg/hs_odd_deg (deg Q_n = n), 组装 hs_even_main/hs_odd_main (以 LegendreFacts/KreinSobolevFacts 为假设) | `docs/SL_hs_orthogonal_systems_proof.tex` 第 3-4 节 | lake build 绿 (8575 jobs), sorry/axiom 0; Legendre 正交性与 Krein-Sobolev 正交性/规范因子为文献事实 (假设接入, 文件头诚实标注); 算符级等距与完备性未形式化 |
| `SL/H3Completeness.lean` | H^3 线代数核心 (R 上, 复用 Completeness 系数族): M_0=M_1=0, 偶/奇二阶跳变递推 c M_{2m}=A_m M_{2m-2}-B_m M_{2m-4}, 缩放 M_{2m}=M_2 u_m, 超阶乘增长 u_m >= (4/c)^(m-1) m! (StabilityGrowth.product_growth 统一覆盖两组系数), 湮灭 M_2=M_3=0, all_moments_zero_of_orthogonal (解析 H1 上界为假设 hbdE/hbdO), h1_moments_zero_of_orthogonal (用 H3MomentBound 的具体上界实例化, 闭合 H^3 矩全零) | `docs/SL_h3_completeness_proof.tex` 第 3-6 节 | lake build 绿, sorry/axiom 0; 等距同构 K_c: H^3->H^1 未形式化 |
| `SL/H3MomentBound.lean` | H^3 线解析 H1 矩上界 (R 上, 积分形式, 源文档第 5 节引理 6): 边界差泛函 delta p=p(1)-p(-1) (delta X^{2m}=0, delta X^{2m+1}=2), h1MomentFunctional M(p)=∫wd·p'+c∫w·p-(1/2)·delta p·∫wd, M(X^{2m})=momentsEven / M(X^{2m+1})=momentsOdd 恒等式, sqrt 初等估计 ((2m)√(2/(4m-1))≤2√m, (2m+1)√(2/(4m+1))≤3√m, √(2/(4m+1))≤√2·√m, √(2/(4m+3))≤√2·√m, √2≤√2·√m), Cauchy-Schwarz 矩上界 |M_{2m}|≤(2‖wd‖₂+c√2‖w‖₂)√m 与 |M_{2m+1}|≤((3+√2)‖wd‖₂+c√2‖w‖₂)√m | `docs/SL_h3_completeness_proof.tex` 第 5 节 (引理 6) | lake build 绿, sorry/axiom 0 |
| `SL/H1Isometry.lean` | H^3 线胶水 (R 上, 具体泛函): FTC 恒等式 ftc_delta (MomentBound.moments wd 0 = w 1 - w (-1), integral_deriv_eq_sub' 接入), H1 内积 h1Inner 与 h1MomentFunctional 的识别 (h1Inner_eq_h1MomentFunctional), 正交传输 h1Inner_moments_zero_of_orthogonal / h1Inner_eq_zero_of_orthogonal (isometry-transport 步骤), 正定核心 moments_zero_sq_le / delta_sq_le_two_int_sq ((Δw)^2<=2∫wd^2) / h1NormSq_nonneg / h1NormSq_eq_zero_imp_sq_int_zero / h1NormSq_eq_zero_imp_ae_zero (w=0 a.e.) | `docs/SL_h3_completeness_proof.tex` 第 2/4/6 节 | lake build 绿, sorry/axiom 0; 算符级等距 (双射/谱) 与 H^1 稠密性未形式化 (文件头诚实标注) |
| `SL/Stability.lean` | 稳定性定理 Thm 2.2 (R 上泛函核心): 发散对数和 (1/2)Σmin(eps_k,1) → 超多项式增长 (superpolynomial_of_divergent_sum/logsum), 多项式界湮灭 (annihilate_of_superpolynomial/divergent_sum), 偶/奇矩递推 + 湮灭 + 多项式上界 → stability_moments_zero (矩全零); 尖锐性 Thm 2.3 (C/k 族): sharp_product_eq (乘积闭式) + sharp_recurrence (递推) + sharp_poly_bound (多项式增长) + sharp_term_bound/sharp_series_summable (β>C+1/2 级数收敛) | `docs/SL_stability_moment_jump.tex` 定理 2.2-2.3 | lake build 绿 (8569 jobs), sorry/axiom 0 |
| `SL/ThirdOrderClassification.lean` | Theorem 1 反向 (分类方向): 若比值轨迹 e_j=1+beta/(2j) 对一切 j>=3 精确, 则偶族 beta in {1,-1}, 奇族 beta in {3,1}; 证明 = 在 j=3,4,5 三指标上通分消分母 + 提取因子 (beta-1)(beta+1) / (beta-3)(beta-1) + 相邻三点消去 | `docs/SL_third_order_recurrence_theory.tex` 定理 1 (反向) | lake build 绿; sorry/axiom 0; TEven/TOdd 分子由符号计算导出并如实声明 (文件头注释) |
| `SL/ThirdOrder.lean` | 三阶递推一般理论 (任意域): IsSolution/ratioMap 框架, Lemma 1 (fixed_point_iff: 序列 E 满足递推 <=> 连续比值 e_j=E_j/E_{j-1} 满足固定点方程 e_j=F_j(e_{j-1},e_{j-2})), Theorem 3 前向 (reduction: 差序列 s_j=r_j-r_{j-1} 满足二阶递推) | `docs/SL_third_order_recurrence_theory.tex` 第 2-4 节 (Lemma 1 + Theorem 3 前向) | lake build 绿; sorry/axiom 0 |
| `SL/ThirdOrderClosedForms.lean` | Theorem 2 闭式验证 (偶族 mu+=(2j+1)!/c^j, mu-=(2j)!/c^j; 奇族 mu+=(2j+3)!/(6(j+1)c^j), mu-=(2j+1)!/c^j 逐项满足三阶递推) + 固定点轨迹充分方向 (e_j=1+beta/(2j), beta in {1,-1}/{3,1}, 乘法与 ratioMap 形式) + 比值恒等式 (偶 mu-/mu+=1/(2n+7), 奇 =3/(2n+9)) | `docs/SL_third_order_recurrence_theory.tex` 定理 1 (充分方向) + 定理 2 | lake build 绿; sorry/axiom 0; 分类方向 (Theorem 1 反向) 由 ThirdOrderClassification.lean 形式化 |
| `SL/ThirdOrderMinimal.lean` | 定理 5 变差常数和式 + 定理 3 反向 (任意域): IsSolution2/Acoef/Bcoef 命名系数, 变差权重 W (w_2=1, w_j=-B_j*s_{j-2}/s_j*w_{j-1}, n+3 下标), sumW/sInd, variation_constant_solution (sInd 满足 (4)), casoratian_sInd/casoratian_prop (离散 Wronskian 闭式 C_j=-s_j*s_{j-1}*w_j 与传播 C_j=-B_j*C_{j-1}), lin_indep_sInd (s_2*s_3*w_3!=0 => s 与 sInd 线性无关), withInitial/reduction_converse (z_j=E_j*(r_1+Σ_{k=2..j} s_k) 满足 (2)), zInd_solution (z^ind 构造); 三解 {E+,E-,z^ind} 的 3x3 Casoratian 非零为源中数值证据, 未形式化 | `docs/SL_third_order_recurrence_theory.tex` 定理 5 + 定理 3 反向 | lake build 绿 (8576 jobs), sorry/axiom 0 |
| `SL/KreinDegenerateLimit.lean` | Krein c->0 退化极限 (多项式级): c=0 配对 pair0 与 radical_pair0 (pair0 f f = 0 <-> f in span{1,x}: 积分非负零 + 开区间点态零 + 无穷根 + 导数为常数 => 仿射), K_0..K_4 低模范数闭式 (kS_norm_zero..four, ||K_4||^2=(2c+240+5040/c+28350/c^2)/9), ||K_4||^2 -> atTop (c->0+, tendsto_norm_four_atTop, 主导 3150/c^2), span 分解 poly_mem_span_quotient (Theorem complete (a): Pi = span{1,x} + span{S_2..S_N}, 强归纳 + 前导项消去) | `docs/SL_krein_c0_limit.tex` (Theorem radical/low/high/complete (a), 多项式版本) | lake build 绿; sorry/axiom 0; 商空间级 (quotient/unit/complete (b)-(d)) 未形式化 (文件头诚实标注) |
| `SL/KreinHighGrowth.lean` | Krein c->0 一般高阶增长 (Theorem "high" 一般部分): aSeq_rec (递推 (19)), aSeq_nonneg_step_ge (逐奇偶类非负/单调), aSeq_lower_step / aSeq_upper_step (一步上下界), lower/upper Even/OddProd (显式乘积常数), aSeq_lower_even/odd 与 aSeq_upper_even/odd (a_n = Theta(c^{-(n-2)/2}) 偶 / Theta(c^{-(n-3)/2}) 奇), norm_even_ge/norm_odd_ge (范数下界), tendsto_norm_even/odd_atTop 与 tendsto_norm_atTop (每个 n>=4 的 ||K_n||^2 -> +infinity) | `docs/SL_krein_c0_limit.tex` (Theorem "high" 一般部分) | lake build 绿; sorry/axiom 0; 商空间级 (quotient/unit/complete (b)-(d)) 仍未形式化 (文件头诚实标注) |

机器验证证据: `run-manifest.json` (lean 4.31.0 / mathlib v4.31.0, 21 个 SL/ 下 .lean 文件
共 22 个扫描 (含 lakefile.lean), sorry/admit/axiom 命中 0, lake build exit 0, 8579 jobs). 义务级审计: `audit_report.md` +
`verification.json` (会话 66-69, 单 agent 自审计, 24 项义务 O1-O24 全部 FAITHFUL 或
MINOR_PARAPHRASE, 无关键错误; 独立第三方复核未执行, 见审计报告独立性说明).

## 2. 完整状态矩阵 (源文档 -> 结果 -> 形式化状态)

源状态标注: 已证 = 项目文档声明严格证明; 部分 = 部分证明/结构结果; 数值 = 数值强猜想; 汇总 = 综述.
形式化状态: 未开始 / 部分 (列出已覆盖片段) / 完整.

| 源文档 | 主要结果 | 源状态 | 形式化状态 |
| --- | --- | --- | --- |
| SL_h2_completeness_proof.tex | {p_n} 在 H^2[-1,1] 解析完备 (等距 K_c + 矩跳跃 + 增长引理 + Weierstrass) | 已证 | 完整 (形式化线): 增长引理 (MomentGrowth/StabilityGrowth) + K_c 恒等式 (KcPolynomial) + 矩递推/缩放 (MomentRecurrence) + 矩上界 (MomentBound) + 湮灭/Weierstrass 收尾 (Completeness); 等距同构 K_c: H^2->L^2 与 L2 稠密扩展未形式化 (O16 记录缺口) |
| SL_h3_completeness_proof.tex | H^3 (及一切整数 s>=1) 完备性 | 已证 | 部分: 矩跳变+缩放+超阶乘增长+湮灭代数核心 (H3Completeness) + 解析 H1 矩上界 (H3MomentBound, Cauchy-Schwarz, 已接入 all_moments_zero_of_orthogonal 的 hbdE/hbdO) + FTC 胶水与 H1 内积识别 (H1Isometry: ftc_delta, h1Inner_eq_h1MomentFunctional, 正交传输, 正定核心); 剩余: 算符级等距同构 K_c: H^3->H^1 (双射/谱) 与多项式在 H^1 稠密性未形式化 |
| SL_hs_orthogonal_systems_proof.tex | 整数阶 H^s 显式完备正交多项式系 + 闭式系数 (传输算子 K_c^{-1}) | 已证 | 部分: 传输算子闭式与 K_c^{-1} 迭代 (TransferOperator) + 传输约化机制与组装 (HsOrthogonalSystems: Q_n=K_c^{-r} P_n / Q_n=K_c^{-r} K_n 的正交与次数约化, Legendre 闭式 deg P_n=n, aSeq 递推; Legendre/Krein-Sobolev 正交性以 LegendreFacts/KreinSobolevFacts 假设接入); 算符级等距与 H^s 完备性未形式化 |
| SL_fractional_left_definite.tex | 实数阶 H^s (含分数窗 3/2<=s<2) 稀疏基解析完备 | 已证 | 未开始 |
| SL_denseness_criteria.tex | 一般稠密性准则: 一阶矩准则 + 临界指数 | 已证 | 未开始 |
| SL_stability_moment_jump.tex | 矩跳跃稳定性: 定量增长引理 (一般系数, B_m>=0 且 A_m-B_m>=c_0), 稳定性定理 (发散对数和 ω(log m) => 完备), 尖锐性 (C/k 族) | 已证 | 部分: 定量增长引理 + eps 形式 (StabilityGrowth); Thm 2.2 泛函核心 + Thm 2.3 尖锐性级数 (Stability); 未形式化: 完备性收尾 w=0 (稠密性, 同 O16 缺口) 与 §4 后门槛分类 (S-门槛/门槛线/Krein 余量) |
| SL_third_order_recurrence_theory.tex | 三阶递推一般理论: 积分解分类/精确降阶/最小解 | 已证 | 部分: 一般框架 + Lemma 1 固定点等价 + Theorem 3 前向降阶 (ThirdOrder); Theorem 2 闭式 + 固定点轨迹充分方向 + 比值恒等式 (ThirdOrderClosedForms); 分类方向 (Theorem 1 反向, ThirdOrderClassification); 变差常数/第三解代数核心 + 定理 3 反向 (ThirdOrderMinimal); 剩余: 三解 Casoratian 非零 (源数值) 与最小解唯一性/渐近 (源数值/符号计算) 未形式化 |
| SL_krein_c0_limit.tex | 移位 Krein 算子 c->0 退化极限的结构稳定性 | 已证 | 部分: 多项式级 radical (c=0 配对 radical = span{1,x}) + 低模范数闭式 (K_0..K_4) + ||K_4||^2 -> atTop + span 分解 (KreinDegenerateLimit) + n>=4 一般 Θ 增长与 ||K_n||^2 -> +infinity (KreinHighGrowth); 商空间级 (H^1/W ≅ L^2_0, quotient/unit, complete (b)-(d)) 未形式化 |
| SL_ratio_proof.tex | sup_{n,rho} lambda_{n+1}/lambda_n = nu(R) (平衡相位 + MW 引理 2) | 已证 | 部分: BalancedPhase (三角闭式核心) + TransferMatrix (三段转移矩阵乘积/secular 方程/平凡不等式); 转移矩阵到特征值的谱论连接与 MW 引理重证仍未形式化 |
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
4. [完成核心: 会话 77] SL_stability_moment_jump.tex 稳定性定理 (sum min(eps_k,1) = omega(log m) => 超多项式)
   与尖锐性定理的形式化: Stability.lean 覆盖 Thm 2.2 泛函核心
   (superpolynomial_of_divergent_sum/logsum, annihilate_of_superpolynomial/divergent_sum,
   stability_moments_zero) 与 Thm 2.3 尖锐性级数 (sharp_product_eq/sharp_recurrence/
   sharp_poly_bound/sharp_term_bound/sharp_series_summable); 11 文件 lake build 绿,
   sorry/axiom 0. 剩余: 完备性收尾 w=0 (稠密性, O16 类缺口) 与 §4 后门槛分类未形式化.
   源文档假设更正见 F-001 (2026-08-11 会话 67 RESOLVED).
5. [部分完成: 会话 91] MW 引理 1-2 与比值上确界定理的代数核心已补全: BalancedPhase (平衡相位三角闭式) + TransferMatrix (三段转移矩阵乘积、sup/inf secular 方程、Dirichlet 条件与平衡相位根、平凡不等式); 剩余: 转移矩阵条件到特征值的谱论等价、MW 周期延拓/零点截断的谱论重证.
6. 间距线 (n=1 定理族, n>=2 开关/约化) 体量大且分析密集, 建议拆义务逐条形式化.
7. [已完成: 会话 70] H^s 显式正交系统线第一步: TransferOperator (K_c^{-r} x^k 闭式 + K_c 双射 + 迭代闭式, 9 文件机器验证通过). 第二步 (会话 85): HsOrthogonalSystems 传输约化 (见第 10 条). 剩余: 算符级等距 K_c^r: H^s -> L^2/H^1 与 H^s 完备性 (谱论/稠密性).
8. [部分: 会话 78+84] H^3 线: H3Completeness.lean (矩跳变/缩放/增长/湮灭代数核心) + H3MomentBound.lean (解析 H1 矩上界, Cauchy-Schwarz + sqrt 初等估计, 已接入 hbdE/hbdO 闭合 h1_moments_zero_of_orthogonal) + H1Isometry.lean (FTC 胶水 ftc_delta, H1 内积识别 h1Inner_eq_h1MomentFunctional, 正交传输 h1Inner_moments_zero_of_orthogonal / h1Inner_eq_zero_of_orthogonal, 正定核心 h1NormSq_nonneg / h1NormSq_eq_zero_imp_ae_zero), 17 文件 lake build 绿 (8575 jobs), sorry/axiom 0. 剩余: 算符级等距同构 K_c: H^3->H^1 (双射/谱, 需谱论) 与多项式稠密性 (p->w 步骤).
9. [已完成: 会话 79-81] 三阶递推线: ThirdOrder.lean (一般框架 IsSolution/ratioMap, Lemma 1 fixed_point_iff, Theorem 3 前向 reduction) + ThirdOrderClosedForms.lean (Theorem 2 偶/奇闭式逐项验证, 固定点轨迹乘法与 ratioMap 形式, 比值恒等式 1/(2n+7) 与 3/(2n+9)) + ThirdOrderClassification.lean (Theorem 1 反向分类: j=3,4,5 通分消分母 + 因子提取, 偶族 beta in {1,-1} / 奇族 beta in {3,1}), 15 文件 lake build 绿 (8573 jobs), sorry/axiom 0. 会话 86: ThirdOrderMinimal.lean (定理 5 变差常数和式 + 定理 3 反向: variation_constant_solution/casoratian 族/lin_indep_sInd/withInitial/reduction_converse/zInd_solution, 19 文件 8576 jobs 绿). 剩余: 三解 Casoratian 非零 (源数值) 与最小解唯一性/渐近 (源数值/符号计算) 未形式化.
10. [已完成: 会话 85] H^s 显式正交系统线第二步: HsOrthogonalSystems.lean (传输约化): Legendre 闭式与 deg P_n = n (natDegree_legendreClosed), aSeq 递推 (源 (9), 基值 a_0..a_3=1, a_4=1+15/c), 传输机制 (KcR_iter_inv_iter 经 Function.LeftInverse.iterate, deg 保持族), 配对/约化定理 (hs_even_pairing/hs_odd_pairing: 正交性归约为经典系) 与组装 (hs_even_main/hs_odd_main); Legendre/Krein-Sobolev 经典正交性以假设接入 (文献事实, 未形式化); 算符级等距与完备性未形式化. 17 文件 lake build 绿 (8575 jobs), sorry/axiom 0.
11. 三阶最小解唯一性的代数核心 (变差常数/第三解) 已由 ThirdOrderMinimal 形式化 (会话 86); 剩余: 三解 Casoratian 非零与最小解渐近 (源数值) 未形式化; 下一块: Krein c->0 极限; MW 重证与间距线体量大, 建议拆义务逐条形式化.
12. [完成多项式级 + 一般增长: 会话 87/88] Krein c->0 退化极限: KreinDegenerateLimit.lean (radical_pair0 / kS_norm_zero..four / tendsto_norm_four_atTop / poly_mem_span_quotient) + KreinHighGrowth.lean (aSeq 上下界 Theta 界与 tendsto_norm_atTop, n>=4), 20 文件 (21 扫描) lake build 绿, sorry/axiom 0. 剩余: 商空间级定理 (H^1/W ≅ L^2_0, 单位归一化解收敛, complete (b)-(d)) 需泛函分析 (稠密性/谱论), 建议专门会话.
