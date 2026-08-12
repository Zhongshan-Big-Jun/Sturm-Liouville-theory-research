---
canonical_key: band-selfconsistency-equivariance (n>=2 gap-extremal reflection symmetry)
title: 带状自洽等变性: F(R,x̄)=PF(R,x) 与反对合 Jacobi 结构 J=-PJP
tags: [mathtool, self-developed, equivariance, jacobian, gap-extremals, nge2, reflection-symmetry]
source: 自研 (会话 58 续作 4b, 2026-08-12; 文档 docs/SL_gap_nge2_symmetry_local_proof.pdf 与 docs/SL_gap_nge2_symmetry_recon.pdf)
status: 等变恒等式与反对合结构为 STRICT; 以 (G1')(G2) 为充分条件的全局唯一性/对称性为已证框架定理, 两条件本身为开放 (数值 EVIDENCE 支持)
created: 2026-08-12
updated: 2026-08-12
---

# 带状自洽等变性 (反射等变 + 反对合 Jacobi 结构)

## 解析

对 Dirichlet 弦 $-y''=\lambda\rho y$, 块密度 $\rho=\sum_{i=1}^{2n+1}R^{\sigma_i}\mathbf1_{[w_{i-1},w_i]}$
($\sigma_i\in\{0,1\}$ 记 $\{1,R\}$ 两种块, $w_0=0<w_1<\cdots<w_{2n}=1$),
开关位置向量 $x=(x_1,\dots,x_{2n})$ ($x_i$ 为第 $i$ 个开关), 带自洽系统为
$F_\sigma(R,x)=0$, 其分量是 FH 跳点条件 $f(x_i)=0$ 的归一化残差.

**等变恒等式 (STRICT)**: 设图案回文 $\sigma_i=\sigma_{2n+2-i}$, 边缘反射
$\bar x_i=1-x_{2n+1-i}$, $P$ 为反转置换矩阵, 则对一切 $(R,x)$
\begin{equation*}
  F_\sigma(R,\bar x)=P\,F_\sigma(R,x).
\end{equation*}

**反对合 Jacobi 结构 (STRICT)**: 反射的微分是 $-P$, 故在对称点 $x^*=\bar x^*$ 处
\begin{equation*}
  J=-PJP,\qquad J:=D_xF_\sigma(R,x^*),
\end{equation*}
即在对称/反对称坐标下 $J=\begin{pmatrix}0&A\\B&0\end{pmatrix}$ 为交叉块形式,
$\det J=(-1)^n\det A\det B$. 推论: 对称方向与反对称方向的变分完全解耦;
对称点非退化当且仅当两块 $A,B$ 均可逆.

**拓扑度同伦框架 (STRICT 定理, 条件开放)**: 设
(G1$'$) 对 $R\in(1,R_0]$, 解簇上 $\det D_xF_\sigma(R,x)\ne0$ 且
$\operatorname{sgn}\det D_xF_\sigma(R,x)=(-1)^n$;
(G2) 块宽在紧 $R$ 区间上一致正 (无退化配置).
则: (i) 度 $\deg(F_\sigma(R,\cdot),W,0)$ 同伦不变; (ii) $R=1$ 处唯一解
$x^*$ 非退化且符号 $(-1)^n$, 度 $=(-1)^n$;
(iii) 对 $R\in(1,R_0]$, $(-1)^n=\#\{\text{解}\}\cdot(-1)^n$, 故恰有一解;
(iv) 等变 + 唯一性给出 $x^*(R)$ 对称; (v) 结合有限块约化与带自洽
(弱星紧性 + bang-bang + 恰 $2n$ 有效开关), 全局极值子 $=$ 唯一解, 故极值子
唯一且对称.

**R=1 一般 $n$ 分析 (STRICT, 新工具内容)**: $R=1$ 时带自洽退化为
$f_1(x)=2\pi^2\big(n^2\sin^2(n\pi x)-(n+1)^2\sin^2((n+1)\pi x)\big)=0$.
直接 Wronskian 公式 $W=-2(n+1)\pi\sin(\pi x)<0$ 与商函数胞腔单调性给出:
$f_1$ 恰 $2n$ 个简单零点 $x_1^*<\cdots<x_{2n}^*$, 反射对称
($x_{2n+1-j}^*=1-x_j^*$), 每胞腔 $(w_{i-1},w_i)$ 恰 2 个,
区间符号 $(-,+,-,\dots,-)$ ($f_1(0+)=f_1(1-)=0$, 端点附近为负),
$\operatorname{sgn}f_1'(x_j^*)=(-1)^{j+1}$,
$\operatorname{sgn}\det D_xF(1,x^*)=(-1)^n$. 这是 (G1$'$) 与局部唯一性
(隐函数) 在 $R=1$ 处的初等基座. $n=2$ 闭式:
$t=(11\pm2\sqrt{10})/36$, 零点 $\approx(0.25597364,0.38264716,0.61735284,0.74402636)$,
$\det J\approx1.43180\times10^5$ (数值复算 $\prod f_1'(x_j^*)/(9\pi^2)^4=143179.8687$).

## 适用范围

- **适用**: $n\ge2$ 相邻谱隙 $D_n=\lambda_{n+1}-\lambda_n$ 极值子的反射对称性
  与唯一性论证; 一般具有回文图案与边缘反射等变性的参数化边值问题;
  把 "对称点 Jacobian 交叉块化" 用作降维工具 ($\det$ 化为两块乘积);
  把 "R=1 唯一非退化解 + 拓扑度" 用作全局分支唯一性的充分性框架.
- **边界情形**: $R=1$ (等变平凡化, 退化为显式 $f_1$, 全部初等);
  $R\to\infty$ 极限 (SUP 中心质量钉扎 $D\to4\pi^2$, INF $D\to0$;
  与 (G2) 不矛盾, G2 只约束有限 $R$); 非回文图案无等变性, 本工具不适用.
- **不适用 / 注意**: (G1$'$) 与 (G2) 目前是开放条件, 未证时框架只给
  充分性, 不得宣称全局唯一性/对称性已证; 等变性要求图案回文
  ($\sigma_i=\sigma_{2n+2-i}$), 一般图案需另法; 对称化不等式路线
  (对密度取平均 $\bar\rho$) 已被否证为单调工具: SUP 118/200、
  INF 116/200 个随机例出现 $D(\bar\rho)<D(\rho)$, 无单调性
  (EVIDENCE, 见 recon 文档).

## 验证与备注

- 来源: 自研 (会话 58 续作 4b, 2026-08-12); 主文档
  docs/SL_gap_nge2_symmetry_local_proof.pdf (9 页, 零警告; §2 结构定理,
  §3 R=1 一般 $n$, §4 R$\to$1 局部定理含唯一性边界排除引理 4.2/4.3,
  §5 拓扑度框架); 侦察文档 docs/SL_gap_nge2_symmetry_recon.pdf (5 页,
  零警告; 失败路线登记 6 条, 含旧对称化数字不可复现的更正).
- 数值交叉检验 (EVIDENCE, 不构成证明): scripts/_gapn2_symmetry_recon.py,
  scripts/_gapn2_jacobian_probe.py, scripts/_gapn2_antigrid_search.py;
  R=1 零点结构 n=2..8 全过; 等变恒等式 $D(\bar x)\equiv D(x)$ 数值 1e-16;
  n=2 沿 R 分支 $\det J>0$ (SUP $1.38\times10^5\to330$,
  INF $1.22\times10^5\to0.123$, $R\in[1.05,100]$); 侦察约 2000 次求解
  未发现内部非对称解或边界聚点; n=2, R=4 反对称平面网格无解;
  n=2..5, R$\in\{2,4,10\}$, 两图案, 每图案恰一带自洽驻点, 对称到 1e-11.
- 诚实登记: §5 (G1$'$)/(G2) 为开放条件, 全局闭合是充分性框架非证明;
  §3 谱符号 ($u_k'(0)>0$ 等) 为 1 维经典结果, 自证依赖已标注;
  旧交接记载的对称化反例数字 (33/200, 57/200) 无法复现, 以本会话
  复算数据 (118/116) 为准.
- 相关工具: [[gap-band-extremals]] (带自洽驻点判据), [[switch-saturation-k-invariant]]
  (恰 $2n$ 开关), [[feynman-hellmann]] (跳点公式), [[keller-variational]] (变分归约),
  [[well-family-rigidity]] (n=1 对称刚性, 本工具是 n>=2 对应物).

## 2026-08-12 复核增补: 首阶变分恒等式符号修正 + 对称分支余量表 (run R-20260812T090000Z-g1prime-g2)

### 符号审计 (STRICT, 全部经 FD 在 1e-4..1e-6 级验证; 部分旧记录符号有误, 以此为准)

1. 几何约定: 开关 $x_i$ 右移 $dx_i$ 使 $[x_i, x_i+dx_i)$ 由 $\mathrm{pat}[i+1]$ 变为 $\mathrm{pat}[i]$, 故
   $\delta\rho = (\mathrm{pat}[i]-\mathrm{pat}[i+1])\,\delta(x-x_i)\,dx_i = -s_i\,\delta(x-x_i)\,dx_i$.
2. 特征值一阶变分: $d\lambda_k/dx_i = +\lambda_k s_i u_k(x_i)^2$ (FD: $d\lambda_2/dx_1 = -48.84090526 = +\lambda_2 s_1 u_2(x_1)^2$).
3. FH 跳点: $dD/dx_i = -s_i f(x_i)$, $f = \lambda_n u_n^2 - \lambda_{n+1} u_{n+1}^2$
   (FD: $dD/dx_1 = +21.89540128 = -s_1 f(x_1)$; 会话 51 记录的 $dD/da = -(R-1)f(a)$ 符号相反,
   零集 $f=0$ 不受影响, 但符号型论证须按新约定复核).
4. 带自洽点的 Jacobian: $J = (\tilde D + \tilde M)/\lambda_{n+1}$, 其中
   $\tilde M_{ji} = s_i\big(2w_iw_jD/(\lambda_n\lambda_{n+1}) - 2\lambda_n^2u_n(x_i)u_n(x_j)\tilde G_n + 2\lambda_{n+1}^2u_{n+1}(x_i)u_{n+1}(x_j)\tilde G_{n+1}\big)$, 
   $\tilde G_k = \sum_{l\ne k}u_lu_l/(\lambda_l-\lambda_k)$ (谱和; 中等 R 下与 jac_fd 相对误差 ~1e-6; 旧解析相减版本符号错误).
5. Hess 公式 (A3 修正): 临界点处 $\mathrm{Hess}(D_n) = -\lambda_{n+1}\mathrm{diag}(s)\,J$ (FD 黑塞 h=1e-4 逐元素误差 4.6e-3, 量级 1e3).
6. $K := \mathrm{diag}(1/s)\,J$ 对称 (因 $|s_i|\equiv R-1$; 数值 crossK ~1e-13); 
   $\det J = (R-1)^{2n}(-1)^n\det K$, $\det K = \det K_+\det K_-$;
   **(G1') $\iff$ $\det K > 0$ $\iff$ 每个临界点处 Hess 正定**.
7. 数值警示: regularized_green (δ=1e-9 极点相减) 消去误差 O(1), 不可用于 Jacobian; 近简并大 R 区解析谱和 Jacobian 亦不可靠 (见下).

### 对称分支余量表 (EVIDENCE, FD 复核; evK 为 $K = \mathrm{diag}(1/s)J = -\mathrm{Hess}/(\lambda(R-1)^2)$ 的特征值)

- SUP $n=2..4$, $R\in[1.05,100]$: $\mathrm{sgn}\,\det J = (+1)^n$ 恒成立; evK 全正 (Hess 负定, 局部极大);
  R=100 处最小 $|\mathrm{ev}K|$: n=2: 0.0156, n=3: 0.0185, n=4: 0.0214 (余量 ~1/R 缓降).
- INF $n=2$ (R≤100), $n=3$ (R≤75), $n=4$ (R≤40): $\mathrm{sgn}\,\det J = (-1)^n$ 恒成立; evK 全负 (Hess 正定, 局部极小);
  最小 $|\mathrm{ev}K|$: n=2 R=100: 3.0e-4; n=3 R=75: 2.6e-5; n=4 R=40: ~1e-5 (指数衰减, 无一致下界).
- 伪影更正: 解析扫描在 INF n=3 R=75 报 detJ=+2.39e-7 (符号翻转) 系谱和截断误差 (|J-J_fd|/|J_fd|=1.0); FD 步长收敛检验给出 detJ = -1.0125e-5 (h=1e-5..1e-7 稳定), 无翻转.
- 近简并结构: INF 大 R 时 $(\lambda_n, \lambda_{n+1})$ 键合-反键合简并 (s-间隙 R=75 n=3 为 0.0098, 逼近 roots_of 网格 0.0092); (G2) 在 R→∞ 极限失效 (R 块宽度→0), 紧 R 区间上无碍.
- O-5 现状: det B (反称块) 数值非零且有上述余量; 严格证明仍开放. 候选路线 (符号已按 I3 修正, 见下节): K 对角部分符号每模式内恒定 (SUP: f'(x_j)/s_j = +2c|W(x_j)|/(R-1) > 0; INF: 负), 需控制 Green 核离对角部分.

### 验证与备注 (增补)
- 脚本: scripts/_gapn2_hp_scan_reduced.py (合并驱动), scripts/_gapn2_hess_verify.py, scripts/_gapn2_hess_sign_and_bigR.py;
  数据: scripts/_gapn2_hp_scan_inf_reduced.json (fd_* 字段为 FD 权威值).
- 修复: scripts/_gapn2_jacobian_analytic.py (符号约定, Hess 公式, M~ 符号, regularized_green 警告, 改用 gtilde_spectral).
- 运行笔记: runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_2026-08-12.md.

## 2026-08-12 晚段增补: M~ 对角闭式 (STRICT) + 符号更正 + 死路登记 + Sylvester 主元 (run R-20260812T090000Z-g1prime-g2 续)

### 新 STRICT 恒等式 (数值验证到 1e-13..1e-15, 见 scripts/_gapn2_mtilde_diag_identity.py)

设 w_j = λ_n u_n(x_j)^2 = λ_{n+1} u_{n+1}(x_j)^2 (带自洽点), D = λ_{n+1}−λ_n,
G~_k 为正则化预解核 (谱和, 去掉极点).

(I1) 部分分式恒等式 (逐项精确, 截断不变):
  λ_{n+1} G~_{n+1}(x_j,x_j) − λ_n G~_n(x_j,x_j)
      = Σ'(x_j) − 2 w_j/D − w_j D/(λ_n λ_{n+1}),
  Σ'(x_j) = Σ_{l≠n,n+1} λ_l u_l(x_j)^2 D/((λ_l−λ_{n+1})(λ_l−λ_n)) > 0 (严格).
  证明: λ/(λ_l−λ) = λ_l/(λ_l−λ) − 1; l=n 极点项 −λ_n u_n^2/D = −w_j/D,
  l=n+1 项 −λ_{n+1} u_{n+1}^2/D = −w_j/D; u_{n+1}^2 − u_n^2 = −w_j D/(λ_n λ_{n+1}).

(I2) M~ 对角闭式 (由 (I1)):
  M~_{jj}/s_j = 2 w_j Σ'(x_j) − 4 w_j^2/D.
  因此 K 的对角元:
  K_{jj} = σ·2c|W(x_j)|/(R−1) + 2w_j Σ'(x_j)/λ_{n+1} − 4 w_j^2/(D λ_{n+1}),
  σ = +1 (SUP) / −1 (INF), c = √(λ_n/λ_{n+1}).
  三项符号: 第一项按模式恒定, 第二项恒正, 第三项恒负; 近简并 (D→0) 时
  第三项主导 (INF 侧 K_{jj} < 0; SUP 侧需 2c|W|/(R−1) + 2w_jΣ'/λ > 4w_j^2/(Dλ)).

(I3) 符号更正 (STRICT): f'(x_j) = −2λ_{n+1} ε_j c W(x_j), W < 0, 且
  ε_j = s_j/(R−1) (SUP), ε_j = −s_j/(R−1) (INF), 故
  f'(x_j)/s_j = +2c|W(x_j)|/(R−1) (SUP), −2c|W(x_j)|/(R−1) (INF).
  本 run 早段笔记与上一节 "O-5 候选路线" 中的统一 "f'(x_j)/s_j < 0" 仅对 INF 成立,
  已更正; FD 验证 (n=2,3; R∈{1.2,2,4,10}; 两模式) 零违反.
  对 O-5 候选路线, 重要的是 "每模式内符号恒定" (此性质成立), 不是具体正负.

(I4) STRICT 界: |W(x_j)| ≤ D. 证明: W(x) = −D ∫_0^x ρ u_n u_{n+1} dt (W(0)=0),
  Cauchy–Schwarz + 归一化 ∫ρu_k^2 = 1. 用于近简并区各项量级排序.

### 死路登记 (EVIDENCE, 以明确数值否证)

- Gershgorin 对角占优: |K_jj| > Σ_{i≠j}|K_ji| 仅在小 R 成立
  (n=2 SUP 至 ~R=2, INF 至 ~R=2; n=3 SUP 仅 ~R≤1.2); n=3 INF R=10 时
  余量/min|diag| = −38.1. 故 O-5 候选路线 "对角部分主导" 在全 R 上被否证.
- H-矩阵缩放 (Perron–Frobenius: ρ(B) < 1, B = diag(|K_jj|)^{-1}|K_off|):
  n=2 SUP R≤10 成立 (0.15..0.89), n=2 INF R≤2 (0.17..0.70), n=3 SUP R≤2;
  n=2 INF R=4 失败 (1.31), n=3 SUP R=4 (1.05), n=3 INF R=2 (1.36).
  K 不是全局 H-矩阵, 该路线对大 R 关闭.

### 新 EVIDENCE: Sylvester 主元符号模式

沿对称分支无换主元 LU 的 K 的主元: SUP 全正, INF 全负
(n=2,3; R∈{1.2,2,4,10}; 与 detK > 0 一致). 由 Sylvester 惯性律,
"主元符号恒定" ⟺ (G1'). 符号模式 (n=2 SUP R=4): 对角 +, 非对角 −,
中央 2×2 块 [[+,+],[+,+]]; K+ 与 K− 均 [[+,−],[−,+]] 型 (INF 全负型).
主元符号的严格证明仍开放, 是当前最有希望的结构手柄
(需控制 K 的 Green 离对角部分, (I2) 已把对角部分化为显式三项).

### 脚本与登记
- scripts/_gapn2_diag_dominance.py (f'/s 符号, K 对角占比, Gershgorin, 块谱, detK vs prod diag).
- scripts/_gapn2_mtilde_diag_identity.py (I1/I2 验证, 一次预计算谱和 N=800; 曾试错两个错误闭式, 均被同一脚本拒绝).
- scripts/_gapn2_hmatrix_probe.py (H-矩阵/Perron–Frobenius 探针 + K/K+/K− 符号模式);
  scripts/_gapn2_pivots_bigR.py (大 R 主元扩展; n=3 SUP R≥30 阶梯续延伪根警告, 该点以
  hp_scan fd_* 字段为准).
- 运行笔记: runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-12.md.
- 诚实登记: 以上不关闭 (G1')/(G2); (I1)-(I4) 为 STRICT; 其余为 EVIDENCE.

## 2026-08-12 深夜段增补: 非对角闭式 (C1)/(C2) + 镜像扇区分解 (STRICT) + 支配不等式扫描 (EVIDENCE)

### (C1)/(C2): M~ 非对角闭式 (STRICT, 机器精度验证 1e-13..1e-15)

T_ji := M~_ji/s_i (带自洽点), D = λ_{n+1}−λ_n, w_j = λ_n u_n(x_j)^2,
ε_j = u_{n+1}(x_j)/(c u_n(x_j)), c = √(λ_n/λ_{n+1}):
- (C1) ε_i = ε_j (同奇偶): T_ji = 2λ_n u_n(x_i)u_n(x_j) Σ'(x_i,x_j) − 4w_iw_j/D
- (C2) ε_i = −ε_j (跨奇偶):
  T_ji = 4w_iw_j(λ_{n+1}^2−λ_nλ_{n+1}+λ_n^2)/(λ_nλ_{n+1}D) − 2λ_n u_n(x_i)u_n(x_j) Σ_+(x_i,x_j)
- Σ'(x_i,x_j) = Σ_{l≠n,n+1} a_l u_l(x_i)u_l(x_j), a_l = λ_l D/((λ_l−λ_{n+1})(λ_l−λ_n)) > 0
  (正权 Gram 核, 任意点集上半正定);
  Σ_+(x_i,x_j) = Σ_{l≠n,n+1} b_l u_l(x_i)u_l(x_j), b_l = λ_n/(λ_l−λ_n) + λ_{n+1}/(λ_l−λ_{n+1}).
- 推导: 逐模部分分式 λ_{n+1}/(λ_l−λ_{n+1}) − λ_n/(λ_l−λ_n) = λ_l D/prod,
  带自洽关系 u_{n+1}(x_j)=ε_j c u_n(x_j), 同奇偶 u_{n+1}u_{n+1} = c^2u_nu_n,
  跨奇偶 u_{n+1}(x_i)u_{n+1}(x_j) = −(λ_n/λ_{n+1})u_n(x_i)u_n(x_j).
- 推论: Σ'(x,y) = λ_{n+1}G~_{n+1}(x,y) − λ_nG~_n(x,y);
  预解恒等式 G~_{n+1} − G~_n = D(G~_{n+1}∘G~_n) − (u_nu_n + u_{n+1}u_{n+1})/D
  (算子复合用每块解析 Gram 精确计算; 梯形求积对高模振荡 O(1) 失败).

### ε-结构 (STRICT): ε_j = (−1)^{j+1} 严格交错

n=2..5 两模式 R=4 及全部扫描根验证: w = λ_n u_n^2 镜像偶, ε 镜像奇,
(εw) 镜像奇; ε_j = σ·s_j/(R−1) (σ=+1 SUP/−1 INF) 编码开关方向.

### 镜像扇区分解 (STRICT, 机器精度验证 1e-15..1e-16)

左半坐标 j=1..n (镜像配对 j↔2n+1−j), 扇区基 Be/Bo 下
K_e = Be^T K Be = diag(d_h) + E_e + H_e,  K_o = Bo^T K Bo = diag(d_h) + E_o + H_o,
d_h,j = σ·2c|W(x_j)|/(R−1):
- E_e = c_e w_h w_h^T, c_e = 4D/(λ_nλ_{n+1}^2) > 0 (PSD 秩1)
- E_o = c_o (ε_h∘w_h)(ε_h∘w_h)^T, c_o = −4(λ_n^2+λ_{n+1}^2)/(λ_nλ_{n+1}Dλ_{n+1}) < 0 (NSD 秩1)
- (H_e)_ij = (2λ_n/λ_{n+1}) u_i u_j [Σ'(x_i,x_j) − p_n Σ_+(x_i,x̄_j)] (i≡j 奇偶),
  否则 [−Σ_+(x_i,x_j) + p_n Σ'(x_i,x̄_j)]
- (H_o)_ij = (2λ_n/λ_{n+1}) u_i u_j [Σ'(x_i,x_j) + p_n Σ_+(x_i,x̄_j)] (i≡j),
  否则 [−Σ_+(x_i,x_j) − p_n Σ'(x_i,x̄_j)]
  p_n = (−1)^{n−1} (u_n 奇偶), x̄_j = 1−x_j.
- 扇区核的模式展开: Σ' ± p_nΣ_+(·,x̄) = Σ_l (a_l ± p_np_l b_l)u_l u_l; 按奇偶类
  拆分后化为同扇区/异扇区 (约化) 预解核 R_k^∥, R_k^⊥ 的组合 (Green 估计路线入口).
- (G1') SUP ⟺ K_e, K_o 正定; INF ⟺ K_e, K_o 负定 (K = K_e ⊕ K_o 为镜像块对角化).

### 证伪 (EVIDENCE)

- (P1) K~ 逐元全正: 否 (n=3 有负元).
- (P1') K~ Hankel 对称 (仅依赖 i+j): 否 (n=2..4 R=4 相对误差 0.6..1.2; 早期探针误导, 撤销).

### 支配不等式扫描 (EVIDENCE, scripts/_gapn2_sector_decomposition.py + _gapn2_sector_scan_*.json)

R 阶梯续延 (根残差 <1e-8), 闭式 K, N=121 模:
- SUP (n=2: R 1.05..100; n=3: 1.2..10; n=4: 1.2..10): K_e, K_o 每点正定,
  充分不等式 λmin(H_o − E_o) + min d > 0 与 λmin(H_e + E_e) + min d > 0 每点成立
  (例: n=2 R=100: +0.091/+0.017; n=3 R=10: +0.568/+0.645).
- INF (n=2: R 1.05..100; n=3: 1.2..30): K_e, K_o 每点负定, 但朴素界
  λmax(H+E) − min|d| < 0 在大 R 失败 (n=2 R=100 边界 0.0000; n=3 R=4: +0.08;
  R=30: +0.0009): 负定性依赖非均匀对角; detK → 0⁺ (n=2 R=100 ~8e-11):
  INF 无一致定量余量, 只能定性 (符号) 论证.
- D-缩放收缩范数 ||D^{-1/2}H_{e/o}D^{-1/2}|| 大 R 超 1 (至 3.4): H 单独非 D-收缩.
- Sherman–Morrison 化归 (精确): K_o = A_o − |c_o|(εw)(εw)^T 正定 ⟺ A_o = diag(d)+H_o
  正定且 |c_o|(εw)^T A_o^{-1}(εw) < 1; K_e 与 −K (INF) 同构. (G1') 化为预解二次型引理.
- 扇区 Sylvester 主元: SUP 全 +, INF 全 − (闭式 K, 全部扫描点; 等价于扇区定性);
  FD 直接续延在 R≥30 仍会落入伪根 (n=3 sup R=10 FD 探针 detK~1e-35 混合主元,
  已按闭式续延真支撤销).

### 诚实登记

- (G1') 仍开放. 本段新增 STRICT: (C1)/(C2), 扇区闭式, E 秩1结构, ε-奇偶代数,
  预解恒等式. 待证引理 (SUP): λmin(H_o − E_o) > −min d (奇扇区二次型界);
  (INF): 非均匀对角下的 K_e 负定性. 两者化归为带自洽点处扇区核 R_k^∥, R_k^⊥
  的 Green 函数估计, 尚未证明.
- 脚本: scripts/_gapn2_mtilde_offdiag_identity.py (C1/C2+预解), 
  scripts/_gapn2_sector_decomposition.py + _gapn2_sector_scan_*.json (扫描),
  scripts/_gapn2_ktilde_positivity.py (早段探针, 保留).
