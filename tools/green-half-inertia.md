---
canonical_key: green-half-inertia (n>=2 gap Jacobian Green-kernel inertia reduction)
title: 半问题 Green 惯性: (G1') detK>0 的 Green 函数化归与奇偶性更正
tags: [mathtool, self-developed, green-function, inertia, oscillation, gap-extremals, nge2]
source: 自研 (R-205, 2026-08-13; 依赖 docs/SL_gap_nge2_symmetry_local_proof.tex 的 (G1')/(G2) 框架)
status: 奇偶性更正为否证 (EVIDENCE); 全局 ε 交错与 Green 惯性为 STRICT; (G1') 本身仍开放
created: 2026-08-13
updated: 2026-08-13
---

# 半问题 Green 惯性 (K_o 的 Green 函数化归)

## 解析

### 奇偶性更正 (否证, EVIDENCE)
特征函数的反射奇偶性
$u_k(1-x)=(-1)^{k-1}u_k(x)$ 由 ODE 的反射不变性推出, 等价于
$\rho(1-x)=\rho(x)$ 作为函数成立, 即**宽度**回文
($w_i=w_{2n+2-i}$). 交替 bang-bang 图案只给出**高度**回文
($\sigma_i=\sigma_{2n+2-i}$); 宽度不对称时 $\rho(1-x)\ne\rho(x)$, 奇偶性
不成立. 随机 Dirichlet 宽度数值: 奇偶性与 $f$ 偶性误差 O(1)
(最坏 1.072 / 1.290), 对称支上为 1e-16. 因此镜像扇区分解、括号恒等式与
$H_e/H_o$ 的 Green 闭式**只在对称带自洽点成立**, 不能反过来证明对称性
(循环); 全局对称性结论仍走 (G1')+(G2) 的唯一性路线.

### 全局 ε 交错 (STRICT, 不依赖对称性)
见 [[switch-saturation-k-invariant]] 的 R-205 更新: 在 $f$ 的 $2n$ 个有序
简单零点处 $\varepsilon_j=(-1)^{j+1}$. 这是 $K$ 非对角闭式 (C1)/(C2) 在
一切带自洽点成立的正确全局输入.

### 半问题谱交错与 Green 惯性 (STRICT, 经典 Gantmacher–Krein)
在对称支上把 $[0,1]$ 于 $x=1/2$ 对半: 偶特征函数 ($u'(1/2)=0$) 对应
Neumann 半问题, 奇特征函数 ($u(1/2)=0$) 对应 Dirichlet 半问题. 设
$\mu_k^N<\mu_k^D<\mu_{k+1}^N$ 为两半问题特征值, 则
\begin{equation*}
  n=2m:\ \lambda_n=\mu_m^D,\ \lambda_{n+1}=\mu_{m+1}^N;\qquad
  n=2m-1:\ \lambda_n=\mu_m^N,\ \lambda_{n+1}=\mu_m^D.
\end{equation*}
在 $n$ 个左半开关 $x_1<\cdots<x_n<1/2$ 上定义奇扇区约化预解核 (异奇偶类):
\begin{equation*}
  R_n^\bot=\sum_{l:\ \mathrm{par}(l)\ne\mathrm{par}(n)}
  \frac{u_l(x_i)u_l(x_j)}{\lambda_l-\lambda_n},\qquad
  R_{n+1}^\bot=\sum_{l:\ \mathrm{par}(l)\ne\mathrm{par}(n+1)}
  \frac{u_l(x_i)u_l(x_j)}{\lambda_l-\lambda_{n+1}}.
\end{equation*}
由经典振荡定理 (Gantmacher–Krein): 预解核限制到有序点集的负指数等于谱参数
下方该奇偶类半问题特征值的个数, 故
\begin{equation*}
  n\ \text{偶}:\ \operatorname{neg} R_n^\bot=\operatorname{neg} R_{n+1}^\bot
  =\tfrac n2;\qquad
  n\ \text{奇}:\ \operatorname{neg} R_n^\bot=\tfrac{n-1}{2},\
  \operatorname{neg} R_{n+1}^\bot=\tfrac{n+1}{2}.
\end{equation*}
数值 (n=2: 各 1 负; n=3: $R_n^\bot$ 1 负, $R_{n+1}^\bot$ 2 负) 吻合.

### (G1') 化归 (STRICT, 机器 1e-13..1e-16)
对称带自洽点处括号恒等式与 $E_o$ 的精确抵消给出奇扇区
\begin{equation*}
  K_o=\operatorname{diag}(d)+\frac{4\lambda_n}{\lambda_{n+1}}
  \operatorname{diag}(u)\,M\,\operatorname{diag}(u),
\end{equation*}
\begin{equation*}
  M=\lambda_{n+1}\operatorname{diag}(\varepsilon)\,
  R_{n+1}^\bot\,\operatorname{diag}(\varepsilon)-\lambda_n R_n^\bot,\qquad
  d_j=\sigma\,\frac{2c|W(x_j)|}{R-1},
\end{equation*}
$\sigma=+1$ (SUP) / $-1$ (INF), $u_j=u_n(x_j)\ne0$, $\varepsilon_j=(-1)^{j+1}$.
因 $\operatorname{diag}(u)$ 是合同变换, (G1') 的奇扇区部分等价于
$\operatorname{diag}(d/u^2)+\frac{4\lambda_n}{\lambda_{n+1}}M$ 的定号性.
数值 (n=2,3, R=4, 两模式): $M$ 惯性混合 (n=2: 1+/1-; n=3: 1+/2-), 而 $K_o$
SUP 正定 / INF 负定, 由非均匀对角 $d$ 补齐; 这就是 (G1') 剩余的精确障碍:
$\operatorname{diag}(d)$ 与 Green 组合 $M$ 的惯性比较 (两块约化预解核的负
方向数如上述奇偶分类).

## 适用范围

- **适用**: 对称支上 $n\ge2$ 相邻谱隙极值问题的 Jacobian/Hessian 定号性分析;
  把 (G1') 从 $2n\times 2n$ 降为两个 $n\times n$ 半问题 Green 二次型;
  一般自伴 Sturm–Liouville 预解核在有序点集上的惯性计数 (振荡理论).
- **边界情形**: $x=1/2$ 处恰有一个相邻特征函数为零 (奇偶交错), $f(1/2)\ne0$;
  $R\to\infty$ 时 INF 近简并对使 detK 指数趋于 0, Green 惯性计数不变但无
  一致定量余量 (定性论证); $R=1$ 退化到常数密度, 半问题谱闭式.
- **不适用 / 注意**: 奇偶性与括号恒等式**不**适用于非对称点 (本工具不声称
  全局奇偶性); 全局凹/凸性不成立 ($D_n$ 在随机 bang-bang 宽度处 Hess 惯性
  混合, EVIDENCE), 不能用整体凸性捷径替代 (G1'); 镜像分解要求回文高度且
  宽度对称, 非回文图案需另法.

## 验证与备注

- 来源: 自研 (R-205, 2026-08-13); 运行笔记
  runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/
  run_notes_addendum_2026-08-13b.md; 脚本
  scripts/_gapn2_parity_global_probe.py (奇偶性否证),
  scripts/_gapn2_green_inertia_probe.py (Green 惯性与 K_o 化归),
  scripts/_gapn2_bracket_identity_audit.py (括号恒等式 1e-15, docstring
  已限定为对称点).
- 诚实登记: (G1') 仍开放; Green 惯性引理为经典结果 (Gantmacher–Krein) 的
  本项目应用, 不声称首创; $\operatorname{diag}(d)$ 与 $M$ 的惯性比较是
  当前未证部分; 全局奇偶性为否证 (EVIDENCE).
- 相关: [[band-selfconsistency-equivariance]] (镜像扇区与 (G1')/(G2) 框架),
  [[switch-saturation-k-invariant]] (ε 交错的胞腔来源),
  [[gap-band-extremals]] (带自洽判据), [[transfer-matrix-secular]] (数值
  射击), [[feynman-hellmann]] (一阶变分).
