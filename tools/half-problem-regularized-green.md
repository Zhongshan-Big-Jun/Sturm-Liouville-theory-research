---
canonical_key: half-problem-regularized-green (exact reduced resolvent without rho(y) factor + exact A1/A2 primitives + both mirror sectors of K)
title: 半问题约化 Green 闭式: 无 rho(y) 因子的约化预解核与 K 的两个镜扇区闭式
tags: [mathtool, self-developed, green-function, reduced-resolvent, sector-decomposition, gap-extremals, nge2]
source: 自研 (R-207, 2026-08-13; 承接 R-205/R-206 的 (G1') 化归)
status: 闭式与扇区恒等式 STRICT (完整推导); C2/C3 交叉检验与 R 扫描为 EVIDENCE
created: 2026-08-13
updated: 2026-08-13
---

# 半问题约化 Green 闭式

## 解析

### 无 rho(y) 因子的约化预解核 (STRICT)

设定: 半问题 $-u''=\mu\rho u$ 于 $(0,L)$, $u(0)=0$, 右端 $u(L)=0$ (D) 或
$u'(L)=0$ (N), $\rho$ 分段常数. $u$ 为特征值 $\mu_k$ 处按 $\int\rho u^2=1$
归一化的特征函数, $v$ 为第二解, $W(u,v)=uv'-u'v=1$, 规范
$v(0)=-1/u'(0)$. 约化预解核
$Gt_k(x,y)=\sum_{l\ne k}v_l(x)v_l(y)/(\mu_l-\mu_k)$ 的闭式:

\begin{equation*}
  Gt_k(x,y)=B(x,y)-u(x)P(y),
\end{equation*}

\begin{equation*}
  B(x,y)=\bigl(u(x)v(y)-v(x)u(y)\bigr)\mathbf 1_{x>y}
  -u(x)u(y)\,I_1(x)+v(x)u(y)\,I_2(x),
\end{equation*}

\begin{equation*}
  I_1(x)=\int_0^x\rho uv\,dt,\qquad I_2(x)=\int_0^x\rho u^2\,dt,
\end{equation*}

\begin{equation*}
  P(y)=\langle\rho u,B(\cdot,y)\rangle
  =v(y)\bigl(1-I_2(y)\bigr)-u(y)\bigl[A_1-A_2+I_1(L)-I_1(y)\bigr],
\end{equation*}

\begin{equation*}
  A_1=\int_0^L\rho u^2I_1\,dx,\qquad A_2=\int_0^L\rho uv\,I_2\,dx.
\end{equation*}

证明要点 (参数变分法): 对 $L_x=-d^2/dx^2-\mu\rho(x)$ 配源
$h(x)=\delta(x-y)-\rho(x)u(x)u(y)$ 得 $L_xB=h$ ($B_x$ 在 $x=y$ 的跳量为
$u'v-v'u=-W=-1$, 故 $-B_{xx}$ 携带 $+\delta$; 光滑部分由 $u''=-\mu\rho u$,
$I_1'=\rho uv$, $I_2'=\rho u^2$ 直接求导验证). 边界条件成立
($B(0,y)=0$, D: $B(L,y)=0$, N: $B_x(L,y)=0$, 用 $I_2(L)=1$ 与 $u$ 的边界条件),
且 $\langle\rho u,Gt_k(\cdot,y)\rangle=P(y)-P(y)=0$. 三条性质唯一刻画约化预解.

精确 $A_1,A_2$: 每块上 $C^2/S^2/CS$ 乘 $iCC/iCS/iSS$ 的九个闭原函数
(初等三角反导数, scripts/_gapn2_half_problem_probe.py 的
`_prims_9`/`_fold3`/`_a1a2_exact`).

### 已登记的关键更正 (勿重犯)

- 旧稿在 $B$ 与 $P$ 中多乘了 $\rho(y)$: 该稿只解到 delta 的 $\rho(y)$ 因子
  (跳量错误), 且在密度跳点对 $y$ 不连续; 常数密度自检无法发现
  ($\rho(y)=1$ 时一致).
- 对 $A_1/A_2$ 求积精度的旧诊断撤回: 精确值与 20 万点梯形求积仅差约 2e-8,
  真正 bug 是 $\rho(y)$ 因子.

### eps 共轭扇区恒等式与约定 (STRICT)

对称带自洽点处, $\varepsilon_j=(-1)^{j+1}$, 镜基底 Be/Bo (对
$j\leftrightarrow 2n-1-j$, 列 $j=(e_j\pm e_{2n-1-j})/\sqrt2$) 满足
$\varepsilon_{2n-1-j}=-\varepsilon_j$, 故
$\operatorname{diag}(\varepsilon)Bo=Be\operatorname{diag}(\beta)$,
$\beta_j=-(-1)^j$, 于是对 $Kp:=\operatorname{diag}(\varepsilon)
K\operatorname{diag}(\varepsilon)$:

\begin{equation*}
  Bo^TKp\,Bo=\operatorname{diag}(\beta)\,(Be^TKBe)\,\operatorname{diag}(\beta).
\end{equation*}

约定: `sector_data['Ko']` 是原 K 的奇扇区 $Bo^TKBo$, 不是 Kp 的; 恒等式
$\operatorname{diag}(1,-1)Ke\,\operatorname{diag}(1,-1)=Ko$ 不成立
(应为 $=Kp_{\mathrm{odd}}$).

### K 的两个镜扇区精确半问题闭式 (STRICT, n 偶)

$n$ 偶 ($\lambda_n=\mu_{n/2}^D$ 奇全模, $\lambda_{n+1}=\mu_{n/2+1}^N$ 偶全模),
$c^2=\lambda_n/\lambda_{n+1}$, $e=\varepsilon[:n]$, $u=(u_n(x_j))_{j<n}$
取左半开关, $d=\sigma\,2c|W(x_j)|/(R-1)$. 由 R-206 塌缩恒等式
$Kp=\operatorname{diag}(d)+r\,vv^T+2\lambda_n\operatorname{diag}(u_n)
S\operatorname{diag}(u_n)$ ($v_j=u_n(x_j)^2$,
$r=2\lambda_nD/\lambda_{n+1}^2$,
$S=\varepsilon Gt_{n+1}\varepsilon-c^2Gt_n$) 与镜限制恒等式
$Be^T\varepsilon Gt_{n+1}\varepsilon Be=G_D(\mu_2^N)\circ ee^T$,
$Be^TGt_nBe=G_N(\mu_1^D)$, $Bo^Tv=0$,
$Bo^T(\varepsilon v)=\sqrt2(\varepsilon v)[:n]$ 得:

\begin{equation*}
  Kp_{\mathrm{odd}}:=\operatorname{diag}(\beta)Ke\operatorname{diag}(\beta)
  =\operatorname{diag}(d[:n])+2\lambda_n\operatorname{diag}(u)
  \bigl[G_D\circ ee^T-c^2G_N\bigr]\operatorname{diag}(u),
\end{equation*}

\begin{equation*}
  Ko:=Bo^TKBo=\operatorname{diag}(d[:n])+2r(\varepsilon v)(\varepsilon v)^T
  +2\lambda_n\operatorname{diag}(u)\bigl[Gt_N-c^2(Gt_D\circ ee^T)\bigr]
  \operatorname{diag}(u),
\end{equation*}

其中 $G_D=G_D(\mu_2^N)$, $G_N=G_N(\mu_1^D)$ 为交叉特征值处的全 Green,
$Gt_D,Gt_N$ 为自身极点处的约化 Green, 四个核均用第 1 节闭式在两个左半
开关处取值; $\det K=\det(Kp_{\mathrm{odd}})\det(Ko)$.

### 谱分裂与 PD 尾核 (STRICT, n=2)

由经典交错 $\mu_1^N<\mu_1^D<\mu_2^N<\mu_2^D$ (Gantmacher-Krein) 与半归一
特征函数 $v_m$ (D), $w_m$ (N):

\begin{equation*}
  G_D(\mu_2^N)|_2=-\alpha v_1v_1^T+Ph,\qquad \alpha=1/(\mu_2^N-\mu_1^D)>0,
\end{equation*}
\begin{equation*}
  G_N(\mu_1^D)|_2=-\beta w_1w_1^T+Qh,\qquad \beta=1/(\mu_1^D-\mu_1^N)>0,
\end{equation*}
\begin{equation*}
  Gt_D=\sum_{m\ge2}\frac{v_mv_m^T}{\mu_m^D-\mu_1^D}\ (PD),\qquad
  T_D=\sum_{m\ge2}\frac{v_mv_m^T}{(\mu_m^D-\mu_1^D)(\mu_m^D-\mu_2^N)}\ (PD),
\end{equation*}
\begin{equation*}
  Gt_N=-\alpha_N w_1w_1^T+Rh,\qquad \alpha_N=1/(\mu_2^N-\mu_1^N)>0,\qquad
  Rh=\sum_{m\ge3}\frac{w_mw_m^T}{\mu_m^N-\mu_2^N}\ (PD).
\end{equation*}

权重严格正 (交错性), 尾和的两点取值 PD (一维特征空间补在两点上取满
$\mathbb R^2$). 由带恒等式 $w_2(x_j)=\varepsilon_jc\,v_1(x_j)$:

\begin{equation*}
  Kp_{\mathrm{odd}}=B_1+2\lambda_2D\operatorname{diag}(u)\bigl[E\,T_DE\bigr]
  \operatorname{diag}(u),
\end{equation*}
\begin{equation*}
  B_1=\operatorname{diag}(d)+2\lambda_2\operatorname{diag}(u)
  \bigl[E\,Gt_DE-\alpha(Ev_1)(Ev_1)^T+c^2\beta w_1w_1^T-c^2Qh\bigr]
  \operatorname{diag}(u),
\end{equation*}
\begin{equation*}
  Ko=\operatorname{diag}(d)+2\lambda_2\operatorname{diag}(u)
  \bigl[Rh-c^2E\,Gt_DE\bigr]\operatorname{diag}(u)
  +2r(\varepsilon v)(\varepsilon v)^T
  -2\lambda_2\alpha_N\operatorname{diag}(u)w_1w_1^T\operatorname{diag}(u).
\end{equation*}

### 开放核 (G1')

(G1') 在 n=2 对称点等价于对一切 $R>1$: (I1) $Kp_{\mathrm{odd}}$ 负定
(INF) / 正定 (SUP), (I2) $Ko$ 同定号. Cauchy/Binet 展开把两个行列式写成
显式带符号双重和; 其符号对 $R$ 一致严格是剩余证明义务. 计划路线:
(i) R→1+ 常数弦处 $(R-1)K$ 的有限极限 (对角占优, 严格定号); (ii) 沿对称
分支的行列式对 R 单调性 (FH 特征对导数 + 带系统开关导数); (iii) R→∞
键合-反键合渐近 (R-202). 路线 (i) 已在 R-208 完成 (见下), (ii)/(iii) 仍开放.

### R→1+ 锚点定理 (STRICT, R-208, 路线 (i) 完成)

引理 A (一切 n>=1): 常数弦处 $W_0=(u_{n+1}^0)'u_n^0-u_{n+1}^0(u_n^0)'$ 在
$f_0$ 的每个零点处非零. 证明: 设 $t=\pi x$, $p=\cos^2((n+1)t)$,
$q=\cos^2(nt)$, $c_0=n/(n+1)$; $f_0=0$ 给 $1-p=c_0^2(1-q)$; 若同时
$W_0=0$, 平方后代入得 $p=n^4q/(n+1)^4$, 联立得 $q=-(n+1)^2/n^2<0$, 矛盾
($\sin(nt)=0$ 情形由 $\gcd(n,n+1)=1$ 排除). 故 $f_0$ 在 $(0,1)$ 恰有 $2n$ 个
单零点且 $f_0'(x_j)=-2\lambda_{n+1}^0\varepsilon_jc_0W_0(x_j)\ne0$.

定理 B (锚点): 近 $R=1$ 的解集是唯一的光滑对称分支 (解的各坐标必是同一标量
函数 $f(\cdot;R)$ 的 $2n$ 个单零点; 对称子流形上 IFT 给存在性). 沿该分支

\begin{equation*}
  (R-1)K(R)\to\frac{\sigma}{\lambda_{n+1}^0}\operatorname{diag}(|f_0'(x_j)|)
\qquad(R\to1+),
\end{equation*}

严格定号 ($\sigma=+1$ SUP, $-1$ INF; 对角项 $2c|W(x_j)|/(R-1)$ 主导, 非对角
部分 $O(1)$: $r vv^T$ 与 $2\lambda_n\operatorname{diag}(u)S\operatorname{diag}(u)$ 在常数弦处有限).
于是 (G1') 对一切 n 在 $(1,1+\delta)$ 成立 (再现 $\operatorname{sgn}\det J(1,x*)=(-1)^n$),
且 n=2 时 (I1)/(I2) 在 $(1,1+\delta)$ 成立: $(R-1)Kp_{\mathrm{odd}}$ 与
$(R-1)Ko$ 均收敛到 $\operatorname{diag}(\sigma 2c_0|W_0(x_j)|)_{j<n}$.

### 半隙 Hessian 解释 (STRICT, R-208)

对称点处全隙等于半隙 $g(x_1,x_2)=\mu_2^N-\mu_1^D$; 带方程 $f(x_j)=0$ 等价于
$\partial g/\partial x_j=-2s_jf(x_j)=0$. 再求导得 (用 $J=\operatorname{diag}(s)K$ 与 A3
$\operatorname{Hess}(D_n)=-\lambda_3\operatorname{diag}(s)J$):

\begin{equation*}
  \nabla^2g=-2(R-1)^2K=+\frac{2}{\lambda_3}\operatorname{Hess}(D_n),
\end{equation*}

故 (I1)+(I2) 等价于: 对称带自洽点是半隙 $g$ 的严格局部极小 (INF) / 严格局部
极大 (SUP). 注意: $g$ 在开关三角形上整体凸/凹为假 (EVIDENCE, R=4 网格扫描
Hessian 在临界点外不定, 违例 11/15 与 12/15), 定号性只成立于临界点.

### 剩余开放核 (R-208 更新)

(G1') 现只在 $[1+\delta,\infty)$ 开放. n=2 的 (I1)/(I2) 在 $[1+\delta,\infty)$ 归约到:
(M1) 沿对称分支 $\frac{d}{dR}\det Kp_{\mathrm{odd}}<0$ 与 $\frac{d}{dR}\det Ko<0$
(锚点 $+\infty$ 与 $R\to\infty$ 的 $0+$ 极限给出 $\det>0$); (M2) 迹符号
($\operatorname{tr}<0$ INF, $>0$ SUP); (M3) $R\to\infty$ 键合-反键合渐近匹配.
EVIDENCE: $\det$ 在 $[1.05,100]$ 严格递减 (双模式), 迹符号正确但非单调;
链式法则
$\frac{d}{dR}M=\partial M/\partial R|_x+\sum_j(\partial M/\partial x_j)(dx_j/dR)$,
$dx/dR=-J^{-1}\partial F/\partial R$ 在 R=1.5,2,4,10 验证到 4-5 位.

## 适用范围

- **适用**: 分段常数密度半问题 (D/N 边界) 的约化预解核精确求值; 全问题
  二阶变分矩阵 K 在对称带自洽点处的镜扇区化归; n 偶的 (I1)/(I2) 化归.
- **边界情形**: 密度跳点处核连续 (6e-10), 对称性 1e-17; $R\to1+$ 时
  $d_j=O(1/(R-1))$ 对角占优; $R\to\infty$ 时 INF 余量退化
  ($\det K\to0+$), 闭式仍需键合-反键合渐近.
- **不适用 / 注意**: n 奇需另列半问题配对 ($\lambda_n=\mu_{(n+1)/2}^N$,
  $\lambda_{n+1}=\mu_{(n+1)/2}^D$); 非对称点镜恒等式不成立 (奇偶性需要
  $\rho(1-x)=\rho(x)$, 即宽度对称); 数值符号检验仅是 EVIDENCE, 不构成
  (I1)/(I2) 的证明; 本工具不提供全局极值性论证.
  锚点定理对一切 n>=1 有效 ((G1') 于 (1,1+delta)); n=2 的 (I1)/(I2)
  锚点同样成立; $[1+\delta,\infty)$ 仍需 (M1)-(M3).

## 验证与备注

- 来源: 自研 (R-207 第 2 段, 2026-08-13); 运行笔记
  runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/
  run_notes_addendum_2026-08-13d.md; 主脚本
  scripts/_gapn2_half_problem_probe.py (C0-C3, 修正后的
  `green_regularized` + 精确 `_a1a2_exact`), 调试链
  scripts/_gapn2_half_debug2/3/4.py, 分解脚本
  scripts/_gapn2_odd2x2_decompose.py, 原 K 奇扇区闭式脚本
  scripts/_gapn2_rawko_closed.py, R 扫描
  scripts/_gapn2_odd2x2_scan.py.
- 数值验证 (EVIDENCE): C2 闭式 vs Richardson 外推谱和 - INF R=4
  Gt_D 7.7e-6, Gt_N 5.8e-6, 全 GD 7.7e-6, GN 5.8e-6; SUP 2.3e-6/1.3e-6
  (残差为谱尾 $O(1/N^2)$, 闭式精确); 对称性 1.4e-17, 跳点连续性 6e-10,
  T_D 闭式 vs 谱 1.8e-11; C3 R-205 与塌缩装配一致 1.8e-15, Ko 闭式 vs FD
  4.6e-10 (INF) / 3.7e-10 (SUP), Kp_odd vs
  $\operatorname{diag}(1,-1)Ke_{fd}\operatorname{diag}(1,-1)$
  2.3e-9 / 8.6e-10; R 扫描 n=2: Kp_odd 与 Ko 在 R∈[1.05,100] (INF) /
  [1.05,10] (SUP) 全部定号, det J > 0.
- 诚实登记: 第 1-4 节恒等式为 STRICT 自足; 一切数值为 EVIDENCE; (I1)/(I2)
  证明未完成, (G1') 状态为 RIGOROUS_PARTIAL_RESULT.
- R-208 验证 (EVIDENCE): n=2 R=1.00001 续延 (R-1)Kp_odd/Ko 与解析极限
  对角差 1.2e-4 (线性于 R-1), 开关收敛到 f0 零点 (3e-7), D->5pi^2;
  n=3 对角极限检查 3.8e-4/3.1e-3; det 单调递减双模式 [1.05,100];
  链式法则 4-5 位 (R=1.5..10); 全局凸性否证 (11/15, 12/15 违例).
  新脚本 scripts/_gapn2_r1_anchor_probe.py, _gapn2_r1_monotonicity_probe.py,
  _gapn2_gap_convexity_probe.py, _gapn2_r1_det_derivative_probe.py.
- 状态 (R-208): (G1') STRICT 于 (1,1+delta) (一切 n), 开放核 [1+delta,inf);
  n=2 (I1)/(I2) STRICT 于 (1,1+delta), 归约到 (M1)-(M3) 于 [1+delta,inf).
- 相关: [[green-half-inertia]] (半问题 Green 惯性与 (G1') 化归),
  [[second-variation-weighted-eigenvalues]] (K 的全局恒等式),
  [[gap-band-extremals]] (带自洽极值判据), [[switch-saturation-k-invariant]]
  (块能量不变量与 eps 交错), [[feynman-hellmann]] (一阶导数).
